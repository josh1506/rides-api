from django_filters import rest_framework as filters

from apps.rides.models import Ride


class RideFilter(filters.FilterSet):
    rider_email = filters.CharFilter(field_name="id_rider__email", lookup_expr="iexact")

    class Meta:
        model = Ride
        fields = ("status", "rider_email")
