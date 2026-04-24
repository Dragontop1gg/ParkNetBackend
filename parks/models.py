from django.db import models


class Park(models.Model):
    class Status(models.TextChoices):
        HEALTHY = "healthy", "Healthy"
        OPEN_NOW = "open_now", "Open Now"
        BUSY = "busy", "Busy"

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    city = models.CharField(max_length=120)
    region = models.CharField(max_length=120, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    acreage = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.HEALTHY,
    )
    hero_image = models.ImageField(upload_to="parks/", blank=True, null=True)
    condition_index = models.PositiveSmallIntegerField(default=85)
    total_trees = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class TreeMarker(models.Model):
    park = models.ForeignKey(
        Park,
        on_delete=models.CASCADE,
        related_name="tree_markers",
    )
    lat = models.FloatField()
    lng = models.FloatField()
    label = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return f"{self.park.name} ({self.lat}, {self.lng})"


class ImprovementProject(models.Model):
    title = models.CharField(max_length=200)
    park = models.ForeignKey(
        Park,
        on_delete=models.CASCADE,
        related_name="improvements",
    )
    thumbnail = models.ImageField(upload_to="projects/", blank=True, null=True)
    progress_percent = models.PositiveSmallIntegerField(default=0)
    reward_points = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
