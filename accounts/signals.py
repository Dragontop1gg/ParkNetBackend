from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User, created: bool, **kwargs) -> None:
    if created:
        Profile.objects.create(
            user=instance,
            display_name=instance.first_name or instance.username,
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance: User, **kwargs) -> None:
    # Be resilient for users created before signals existed or partial data states.
    profile, _ = Profile.objects.get_or_create(
        user=instance,
        defaults={"display_name": instance.first_name or instance.username},
    )
    if not profile.display_name:
        profile.display_name = instance.first_name or instance.username
    profile.save()
