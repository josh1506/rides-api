from django.conf import settings
from django.db import models


class RideStatus(models.TextChoices):
    EN_ROUTE = "en-route", "En Route"
    PICKUP = "pickup", "Pickup"
    DROPOFF = "dropoff", "Dropoff"
    CANCELLED = "cancelled", "Cancelled"


class Ride(models.Model):
    id_ride = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=RideStatus.choices, db_index=True)
    id_rider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="rides_as_rider",
    )
    id_driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="rides_as_driver",
    )
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField(db_index=True)

    class Meta:
        db_table = "ride"
        ordering = ("-pickup_time", "-id_ride")

    def __str__(self):
        return f"Ride {self.id_ride} ({self.status})"


class RideEvent(models.Model):
    id_ride_event = models.BigAutoField(primary_key=True)
    id_ride = models.ForeignKey(
        Ride, on_delete=models.PROTECT, related_name="ride_events"
    )
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "ride_event"
        ordering = ("-created_at", "-id_ride_event")

    def __str__(self):
        return f"RideEvent {self.id_ride_event} ({self.id_ride_id})"
