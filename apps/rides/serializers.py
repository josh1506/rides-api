from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from apps.rides.models import Ride, RideEvent
from apps.users.serializers import UserDetailSerializer


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = (
            "id_ride_event",
            "id_ride",
            "description",
            "created_at",
        )
        read_only_fields = ("id_ride_event",)


class RideSerializer(serializers.ModelSerializer):
    rider = UserDetailSerializer(source="id_rider", read_only=True)
    driver = UserDetailSerializer(source="id_driver", read_only=True)
    todays_ride_events = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = (
            "id_ride",
            "status",
            "id_rider",
            "id_driver",
            "rider",
            "driver",
            "pickup_latitude",
            "pickup_longitude",
            "dropoff_latitude",
            "dropoff_longitude",
            "pickup_time",
            "todays_ride_events",
        )

    @extend_schema_field(RideEventSerializer(many=True))
    def get_todays_ride_events(self, ride):
        events = getattr(ride, "todays_ride_event_list", None)
        if events is None:
            events = ride.ride_events.none()
        return RideEventSerializer(events, many=True).data
