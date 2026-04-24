from rest_framework import permissions, viewsets

from .models import Park
from .serializers import ParkDetailSerializer, ParkListSerializer


class ParkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Park.objects.prefetch_related("tree_markers", "reports").all()
    lookup_field = "pk"
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ParkDetailSerializer
        return ParkListSerializer
