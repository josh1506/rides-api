from rest_framework.routers import DefaultRouter

from apps.rides.views import RideEventViewSet, RideViewSet

router = DefaultRouter()
router.register("events", RideEventViewSet, basename="ride-event")
router.register("", RideViewSet, basename="ride")

urlpatterns = router.urls
