from django.contrib.auth.models import User
from django.db import models

from parks.models import Park


class Report(models.Model):
    class Category(models.TextChoices):
        LITTERING = "littering", "Littering"
        VANDALISM = "vandalism", "Vandalism"
        BROKEN_PATH = "broken_path", "Broken Path"
        SAFETY = "safety", "Safety Hazard"
        LIGHTING = "lighting", "Lighting"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        IN_PROGRESS = "in_progress", "In Progress"
        RESOLVED = "resolved", "Resolved"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    park = models.ForeignKey(
        Park,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reports",
    )
    category = models.CharField(max_length=30, choices=Category.choices)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="reports/", blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMITTED,
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    ai_priority = models.PositiveSmallIntegerField(null=True, blank=True)
    ai_summary = models.TextField(blank=True)
    ai_raw = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.get_category_display()} @ {self.park or 'unknown'}"
