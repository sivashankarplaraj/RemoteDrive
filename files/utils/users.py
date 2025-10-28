from typing import Optional

from django.contrib.auth.models import AnonymousUser

from files.models import User as FileUser


def get_or_create_user_from_request(request) -> FileUser:
    # Expect request.user to have email/name fields attached by JWTAuth
    email = getattr(request.user, 'email', None)
    display_name = getattr(request.user, 'display_name', None)
    if not email:
        # Fallback: anonymous with synthetic email
        email = 'anon@example.local'
        display_name = display_name or 'anon'
    user, _ = FileUser.objects.get_or_create(email=email, defaults={'display_name': display_name or email})
    return user
