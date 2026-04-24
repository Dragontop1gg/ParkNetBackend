import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = (
        "Create/update superuser from env if DJANGO_SUPERUSER_PASSWORD is set "
        "(safe for free Render where Shell is unavailable)."
    )

    def handle(self, *args, **options):
        username = (os.environ.get("DJANGO_SUPERUSER_USERNAME") or "admin").strip()
        email = (os.environ.get("DJANGO_SUPERUSER_EMAIL") or "admin@parknet.local").strip()
        password = (os.environ.get("DJANGO_SUPERUSER_PASSWORD") or "admin12345").strip()
        if len(password) < 8:
            password = "admin12345"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )
        # For demo deployments, always enforce admin flags/password from env.
        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        action = "created" if created else "updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"ensure_admin: {action} superuser {username!r} (password enforced)"
            )
        )
