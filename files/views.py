from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import InitUploadRequest, InitUploadResponse, CommitRequest, CommitResponse
from .utils.keygen import object_key_for
from .utils.users import get_or_create_user_from_request
from .storage.minio_client import presign_put_url, stat_object
from .models import File, FileVersion


class InitUploadView(APIView):
    def post(self, request):
        serializer = InitUploadRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        filename = serializer.validated_data['filename']
        key = object_key_for(filename)
        url = presign_put_url(key)
        return Response(InitUploadResponse({'key': key, 'presigned_put_url': url}).data, status=status.HTTP_200_OK)


class CommitView(APIView):
    def post(self, request):
        serializer = CommitRequest(data=request.data)
        serializer.is_valid(raise_exception=True)
        key = serializer.validated_data['key']
        checksum = serializer.validated_data['checksum']
        size = serializer.validated_data['size']

        # Verify object exists in MinIO and optionally size matches
        try:
            stat = stat_object(key)
        except Exception:
            return Response({"detail": "Object not found in storage for provided key."}, status=status.HTTP_400_BAD_REQUEST)

        obj_size = getattr(stat, 'size', None)
        if obj_size is not None and size is not None and int(obj_size) != int(size):
            return Response({"detail": f"Size mismatch: provided {size}, object {obj_size}"}, status=status.HTTP_400_BAD_REQUEST)

        # Resolve user and file
        user = get_or_create_user_from_request(request)
        # Derive a filename from key if we don't have one
        filename = key.split('/')[-1]
        content_type = getattr(stat, 'metadata', {}).get('content-type') if hasattr(stat, 'metadata') else ''

        file_obj, created = File.objects.get_or_create(
            user=user,
            filename=filename,
            defaults={
                'content_type': content_type or '',
                'size': size or 0,
                'checksum': checksum or '',
                'key_current': key,
            },
        )

        if not created:
            # Advance version, update metadata and key_current
            file_obj.key_current = key
            file_obj.size = size or file_obj.size
            file_obj.checksum = checksum or file_obj.checksum
            if content_type:
                file_obj.content_type = content_type
            file_obj.save()

        # Determine next version number
        last_version = (
            FileVersion.objects.filter(file=file_obj).order_by('-version').values_list('version', flat=True).first()
        )
        next_version = 1 if not last_version else int(last_version) + 1

        fv = FileVersion.objects.create(
            file=file_obj,
            version=next_version,
            key=key,
            size=size or 0,
            checksum=checksum or '',
        )

        resp = CommitResponse({'fileId': file_obj.id, 'version': next_version})
        return Response(resp.data, status=status.HTTP_201_CREATED)
