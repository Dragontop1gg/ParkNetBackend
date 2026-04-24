from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import MeView, RegisterView
from parks.views import ParkViewSet
from reports.views import InsightsAPIView, ReportViewSet

router = DefaultRouter()
router.register(r"parks", ParkViewSet, basename="park")
router.register(r"reports", ReportViewSet, basename="report")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/register/", RegisterView.as_view(), name="register"),
    path("api/me/", MeView.as_view(), name="me"),
    path("api/insights/", InsightsAPIView.as_view(), name="insights"),
]

# Render deployment has no separate media server by default.
# Keep media files accessible directly from Django.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
