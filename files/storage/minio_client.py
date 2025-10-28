import os
from urllib.parse import urlparse
from minio import Minio
from minio.error import S3Error

from django.conf import settings


def get_minio_client() -> Minio:
    endpoint = settings.MINIO_ENDPOINT
    parsed = urlparse(endpoint)
    secure = parsed.scheme == 'https'
    netloc = parsed.netloc
    # If endpoint is http(s)://host:port, minio.Minio expects host:port
    return Minio(
        netloc,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=secure,
    )


def presign_put_url(key: str, expiry_seconds: int = 900) -> str:
    client = get_minio_client()
    return client.presigned_put_object(settings.MINIO_BUCKET, key, expires=expiry_seconds)


def presign_get_url(key: str, expiry_seconds: int = 900) -> str:
    client = get_minio_client()
    return client.presigned_get_object(settings.MINIO_BUCKET, key, expires=expiry_seconds)


def stat_object(key: str):
    """Return object stats or raise if missing."""
    client = get_minio_client()
    return client.stat_object(settings.MINIO_BUCKET, key)
