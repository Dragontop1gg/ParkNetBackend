import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Create superuser from env if DJANGO_SUPERUSER_PASSWORD is set and user missing (idempotent)."

    def handle(self, *args, **options):
        password = (os.environ.get("DJANGO_SUPERUSER_PASSWORD") or "").strip()
        if not password:
            self.stdout.write(
                "ensure_admin: skip (set DJANGO_SUPERUSER_PASSWORD in Render to create admin)"
            )
            return

        username = (os.environ.get("DJANGO_SUPERUSER_USERNAME") or "admin").strip()
        email = (os.environ.get("DJANGO_SUPERUSER_EMAIL") or "admin@parknet.local").strip()

        if User.objects.filter(username=username).exists():
            self.stdout.write(f"ensure_admin: user {username!r} already exists")
            return

        User.objects.create_superuser(username, email, password)
        self.stdout.write(self.style.SUCCESS(f"ensure_admin: created superuser {username!r}"))
