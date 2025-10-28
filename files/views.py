from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import InitUploadRequest, InitUploadResponse, CommitRequest, CommitResponse
from .utils.keygen import object_key_for
from .storage.minio_client import presign_put_url


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
        # TODO: validate object exists, create/advance FILE and FILE_VERSIONS, update FILES.key_current
        # Placeholder response to keep route live
        resp = CommitResponse({'fileId': '00000000-0000-0000-0000-000000000000', 'version': 1})
        return Response(resp.data, status=status.HTTP_201_CREATED)
