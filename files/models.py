import uuid
from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    display_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    filename = models.CharField(max_length=512)
    key_current = models.CharField(max_length=1024, blank=True, null=True)
    content_type = models.CharField(max_length=255)
    size = models.BigIntegerField(default=0)
    checksum = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'files'
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]


class FileVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='versions')
    version = models.IntegerField()
    key = models.CharField(max_length=1024)
    size = models.BigIntegerField(default=0)
    checksum = models.CharField(max_length=128, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'file_versions'
        unique_together = ('file', 'version')
        indexes = [
            models.Index(fields=['file', 'version']),
        ]


class Share(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='shares')
    owner_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares')
    token = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    permissions = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shares'
