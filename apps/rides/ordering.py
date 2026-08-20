from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import ACos, Cos, Radians, Sin
from rest_framework.exceptions import ValidationError
from rest_framework.filters import BaseFilterBackend


class RideOrderingFilter(BaseFilterBackend):
    PICKUP_ORDERING = ("pickup_time", "-pickup_time")
    DISTANCE_ORDERING = ("distance", "-distance")
    ALLOWED_ORDERING = PICKUP_ORDERING + DISTANCE_ORDERING

    def filter_queryset(self, request, queryset, view):
        ordering = request.query_params.get("ordering")

        if not ordering or ordering not in self.ALLOWED_ORDERING:
            return queryset.order_by("pickup_time", "id_ride")

        if ordering in self.PICKUP_ORDERING:
            return queryset.order_by(ordering, "id_ride")

        if ordering in self.DISTANCE_ORDERING:
            pickup_lat = request.query_params.get("pickup_lat", None)
            pickup_lng = request.query_params.get("pickup_lng", None)

            if pickup_lat is None or pickup_lng is None:
                raise ValidationError(
                    {
                        "detail": "pickup_lat and pickup_lng are required for distance ordering."
                    }
                )

            try:
                pickup_lat = float(pickup_lat)
                pickup_lng = float(pickup_lng)
            except (TypeError, ValueError):
                raise ValidationError({"detail": "Invalid pickup coordinates."})

            # Spherical law of cosines - https://www.movable-type.co.uk/scripts/latlong.html
            # Formula: ACOS( SIN(lat1)*SIN(lat2) + COS(lat1)*COS(lat2)*COS(lon2-lon1) ) * 6371000
            lat1 = Radians(pickup_lat)
            lat2 = Radians(F("pickup_latitude"))
            lng_diff = Radians(F("pickup_longitude")) - Radians(pickup_lng)

            distance_expression = ExpressionWrapper(
                ACos(Sin(lat1) * Sin(lat2) + Cos(lat1) * Cos(lat2) * Cos(lng_diff))
                * 6371000,
                output_field=FloatField(),
            )

            return queryset.annotate(distance=distance_expression).order_by(
                ordering, "id_ride"
            )

        return queryset
