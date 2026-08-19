from rest_framework.routers import DefaultRouter

from apps.rides.views import RideViewSet

router = DefaultRouter()
router.register("", RideViewSet, basename="ride")

urlpatterns = router.urls
