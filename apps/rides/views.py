from datetime import timedelta

from django.db.models import Prefetch
from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from apps.rides.filters import RideFilter
from apps.rides.models import Ride, RideEvent
from apps.rides.serializers import RideSerializer, RideEventSerializer
from apps.rides.ordering import RideOrderingFilter
from apps.users.permissions import IsAdmin


class IsAdminModelViewSet(ModelViewSet):
    permission_classes = (IsAdmin,)


class RideViewSet(IsAdminModelViewSet):
    serializer_class = RideSerializer
    filterset_class = RideFilter
    lookup_field = "id_ride"
    filter_backends = [DjangoFilterBackend, RideOrderingFilter]

    def get_queryset(self):
        time_cutoff = timezone.now() - timedelta(hours=24)
        recent_ride_events = RideEvent.objects.filter(created_at__gte=time_cutoff)
        queryset = (
            Ride.objects.select_related("id_rider", "id_driver")
            .prefetch_related(
                Prefetch(
                    "ride_events",
                    queryset=recent_ride_events,
                    to_attr="todays_ride_event_list",
                )
            )
            .all()
        )
        return queryset


class RideEventViewSet(IsAdminModelViewSet):
    queryset = RideEvent.objects.select_related("id_ride").all()
    serializer_class = RideEventSerializer
    lookup_field = "id_ride_event"
    filterset_fields = ("id_ride",)
