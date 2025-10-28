from django.core.management.base import BaseCommand
from django.conf import settings
import jwt
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Mint a development JWT token'

    def add_arguments(self, parser):
        parser.add_argument('--sub', type=str, default='00000000-0000-0000-0000-000000000000')
        parser.add_argument('--email', type=str, default='dev@example.local')
        parser.add_argument('--name', type=str, default='dev user')
        parser.add_argument('--ttl', type=int, default=3600, help='Token TTL in seconds (default 3600)')

    def handle(self, *args, **options):
        now = datetime.utcnow()
        payload = {
            'sub': options['sub'],
            'email': options['email'],
            'name': options['name'],
            'iat': int(now.timestamp()),
            'exp': int((now + timedelta(seconds=options['ttl'])).timestamp()),
        }
        token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        self.stdout.write(token)
