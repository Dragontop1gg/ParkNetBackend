from rest_framework import serializers

from reports.serializers import ReportListSerializer

from .models import ImprovementProject, Park, TreeMarker


class TreeMarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeMarker
        fields = ("id", "lat", "lng", "label")


class ParkListSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    tree_markers = TreeMarkerSerializer(many=True, read_only=True)

    class Meta:
        model = Park
        fields = (
            "id",
            "name",
            "slug",
            "city",
            "region",
            "latitude",
            "longitude",
            "acreage",
            "status",
            "condition_index",
            "total_trees",
            "description",
            "thumbnail_url",
            "tree_markers",
        )

    def get_thumbnail_url(self, obj: Park) -> str | None:
        if obj.hero_image:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.hero_image.url)
            return obj.hero_image.url
        return None


class ParkDetailSerializer(ParkListSerializer):
    recent_reports = serializers.SerializerMethodField()
    tree_markers = TreeMarkerSerializer(many=True, read_only=True)

    class Meta(ParkListSerializer.Meta):
        fields = ParkListSerializer.Meta.fields + (
            "hero_image",
            "recent_reports",
            "tree_markers",
            "created_at",
        )

    def get_recent_reports(self, obj: Park):
        qs = obj.reports.all()[:10]
        return ReportListSerializer(qs, many=True, context=self.context).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")
        if instance.hero_image and request:
            data["hero_image"] = request.build_absolute_uri(instance.hero_image.url)
        elif instance.hero_image:
            data["hero_image"] = instance.hero_image.url
        else:
            data["hero_image"] = None
        return data


class ImprovementProjectSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = ImprovementProject
        fields = (
            "id",
            "title",
            "park",
            "progress_percent",
            "reward_points",
            "thumbnail_url",
        )

    def get_thumbnail_url(self, obj: ImprovementProject) -> str | None:
        if obj.thumbnail:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.thumbnail.url)
            return obj.thumbnail.url
        return None
