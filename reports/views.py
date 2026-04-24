from django.db.models import Count, Q
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Report
from .serializers import ReportCreateSerializer, ReportListSerializer
from .services.openrouter import analyze_report


class ReportViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Report.objects.select_related("park", "user").all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == "create":
            return ReportCreateSerializer
        return ReportListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report = serializer.save(user=request.user)

        profile = request.user.profile
        profile.points += 10
        profile.save(update_fields=["points"])

        ai = analyze_report(report.category, report.description)
        if ai and not ai.get("parse_error"):
            report.ai_priority = ai.get("priority")
            report.ai_summary = ai.get("summary", "")
            report.ai_raw = ai
            report.save(update_fields=["ai_priority", "ai_summary", "ai_raw"])
        elif ai and ai.get("parse_error"):
            report.ai_raw = ai
            report.save(update_fields=["ai_raw"])

        headers = self.get_success_headers(serializer.data)
        out = ReportListSerializer(report, context={"request": request}).data
        return Response(out, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        qs = super().get_queryset()
        park = self.request.query_params.get("park")
        if park:
            qs = qs.filter(park_id=park)
        return qs

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def mine(self, request):
        qs = self.get_queryset().filter(user=request.user)
        ser = ReportListSerializer(qs, many=True, context={"request": request})
        return Response(ser.data)


class InsightsAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from parks.models import ImprovementProject
        from parks.serializers import ImprovementProjectSerializer

        resolved = Report.objects.filter(status=Report.Status.RESOLVED).count()
        active_stewards = (
            Report.objects.values("user")
            .annotate(c=Count("id"))
            .filter(c__gte=1)
            .count()
        )
        trees_protected = (
            Report.objects.filter(
                Q(status=Report.Status.RESOLVED) | Q(status=Report.Status.IN_PROGRESS)
            ).count()
            * 12
            + 1000
        )

        weekly = ImprovementProject.objects.filter(is_active=True).select_related("park")[:5]
        return Response(
            {
                "community_impact": {
                    "trees_protected_count": trees_protected,
                    "weekly_growth_pct": 12,
                },
                "summary": {
                    "reports_resolved": resolved,
                    "active_stewards": active_stewards,
                },
                "weekly_improvements": ImprovementProjectSerializer(
                    weekly, many=True, context={"request": request}
                ).data,
            }
        )
