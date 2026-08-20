from datetime import timedelta

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.rides.models import Ride, RideStatus
from apps.users.models import UserRole

User = get_user_model()


def create_new_user(email, role, **extra_fields):
    return User.objects.create_user(email=email, role=role, **extra_fields)


def create_ride(driver, rider, ride_status, minutes):
    return Ride.objects.create(
        status=ride_status,
        id_rider=rider,
        id_driver=driver,
        pickup_latitude=14.5995,
        pickup_longitude=120.9842,
        dropoff_latitude=14.5547,
        dropoff_longitude=121.0244,
        pickup_time=timezone.now() + timedelta(minutes=minutes),
    )


class TestRideAPITestCase(APITestCase):
    def setUp(self):
        self.admin = create_new_user("admin@example.com", UserRole.ADMIN)
        self.driver = create_new_user("driver@example.com", UserRole.DRIVER)
        self.rider = create_new_user("rider@example.com", UserRole.RIDER)
        self.ride = create_ride(self.driver, self.rider, RideStatus.PICKUP, 10)
        self.ride_2 = create_ride(self.driver, self.rider, RideStatus.DROPOFF, 40)
        self.url = reverse("ride-list")

    def test_only_admin_can_access_rides(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.rider)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.driver)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.admin)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_and_filter_rides(self):
        self.client.force_authenticate(self.admin)

        res = self.client.get(
            self.url,
            {"status": RideStatus.PICKUP, "rider_email": self.rider.email},
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 1)
        self.assertEqual(res.data["results"][0]["id_ride"], self.ride.id_ride)
        self.assertEqual(res.data["results"][0]["rider"]["email"], self.rider.email)
        self.assertEqual(res.data["results"][0]["driver"]["email"], self.driver.email)
        self.assertIn("rider", res.data["results"][0])
        self.assertIn("driver", res.data["results"][0])
        self.assertIn("todays_ride_events", res.data["results"][0])

    def test_only_admin_can_create_rides(self):
        payload = {
            "status": RideStatus.EN_ROUTE,
            "id_rider": self.rider.id_user,
            "id_driver": self.driver.id_user,
            "pickup_latitude": 14.61,
            "pickup_longitude": 120.99,
            "dropoff_latitude": 14.62,
            "dropoff_longitude": 121.0,
            "pickup_time": (timezone.now() + timedelta(days=1)).isoformat(),
        }

        self.client.force_authenticate(self.rider)
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.driver)
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.admin)

        res = self.client.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data["rider"]["email"], self.rider.email)
        self.assertEqual(res.data["driver"]["email"], self.driver.email)
        self.assertEqual(res.data["status"], payload["status"])
        self.assertEqual(res.data["pickup_latitude"], payload["pickup_latitude"])
        self.assertEqual(res.data["pickup_longitude"], payload["pickup_longitude"])

    def test_sorting_using_distance(self):
        self.client.force_authenticate(self.admin)

        res = self.client.get(self.url, {"ordering": "distance"})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        res = self.client.get(
            self.url,
            {
                "ordering": "distance",
                "pickup_lat": 14.61,
                "pickup_lng": 120.99,
            },
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
