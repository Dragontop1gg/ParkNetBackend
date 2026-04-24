from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=120, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    points = models.PositiveIntegerField(default=0)
    rank_label = models.CharField(max_length=80, default="Community Member")

    def __str__(self) -> str:
        return self.display_name or self.user.username
