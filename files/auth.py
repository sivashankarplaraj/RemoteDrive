import os
from typing import Optional, Tuple

import jwt
from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication, exceptions

from django.conf import settings


class JWTAuthentication(authentication.BaseAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request) -> Optional[Tuple[object, None]]:
        auth = authentication.get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None
        if len(auth) == 1:
            raise exceptions.AuthenticationFailed('Invalid Authorization header. No credentials provided.')
        if len(auth) > 2:
            raise exceptions.AuthenticationFailed('Invalid Authorization header.')

        token = auth[1]
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

        # For PoC: attach an AnonymousUser-like principal with id/email from token if present
        user_info = {
            'id': payload.get('sub'),
            'email': payload.get('email'),
            'display_name': payload.get('name') or payload.get('email') or 'user',
        }
        # You may later resolve to files.models.User
        request.user = AnonymousUser()
        request.user.id = user_info['id']
        request.user.email = user_info['email']
        request.user.display_name = user_info['display_name']
        return (request.user, None)
