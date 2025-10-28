from rest_framework import serializers


class InitUploadRequest(serializers.Serializer):
    filename = serializers.CharField(max_length=512)
    size = serializers.IntegerField(min_value=0)
    content_type = serializers.CharField(max_length=255)


class InitUploadResponse(serializers.Serializer):
    key = serializers.CharField()
    presigned_put_url = serializers.CharField()


class CommitRequest(serializers.Serializer):
    key = serializers.CharField()
    checksum = serializers.CharField()
    size = serializers.IntegerField(min_value=0)


class CommitResponse(serializers.Serializer):
    fileId = serializers.UUIDField()
    version = serializers.IntegerField(min_value=1)
