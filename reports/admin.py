from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("id", "category", "park", "user", "status", "ai_priority", "created_at")
    list_filter = ("status", "category")
