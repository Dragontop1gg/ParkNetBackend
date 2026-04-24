from django.contrib import admin

from .models import ImprovementProject, Park, TreeMarker


@admin.register(Park)
class ParkAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "status", "condition_index")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TreeMarker)
class TreeMarkerAdmin(admin.ModelAdmin):
    list_display = ("park", "lat", "lng")


@admin.register(ImprovementProject)
class ImprovementProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "park", "progress_percent", "is_active")
