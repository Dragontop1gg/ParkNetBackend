from rest_framework import serializers

from .models import Report


class ReportListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    park_name = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = (
            "id",
            "category",
            "status",
            "description",
            "park",
            "park_name",
            "image_url",
            "latitude",
            "longitude",
            "ai_priority",
            "ai_summary",
            "created_at",
        )

    def get_image_url(self, obj: Report) -> str | None:
        if obj.image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

    def get_park_name(self, obj: Report) -> str | None:
        return obj.park.name if obj.park else None


class ReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = (
            "park",
            "category",
            "description",
            "image",
            "latitude",
            "longitude",
        )
