from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import UserRole

User = get_user_model()


def create_new_user(email, role=UserRole.RIDER, **extra_fields):
    return User.objects.create_user(
        email=email,
        password="password123",
        role=role,
        first_name="Test",
        last_name="User",
        phone_number="09120000000",
        is_active=True,
        **extra_fields
    )


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.admin = create_new_user(
            email="admin@example.com", role=UserRole.ADMIN, is_staff=True
        )
        self.rider = create_new_user(email="rider@example.com")
        self.url = reverse("user-list")

    def test_non_admin_cant_access_users(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.rider)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_get_users(self):
        self.client.force_authenticate(self.admin)

        res = self.client.get(self.url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["count"], 2)

    def test_only_admin_role_can_create_or_update_users(self):
        payload = {
            "email": "new_driver@example.com",
            "password": "password123",
            "role": UserRole.DRIVER,
            "first_name": "New",
            "last_name": "Driver",
            "phone_number": "09170000001",
        }

        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.rider)
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(self.admin)
        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", res.data)

        user = User.objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))

        new_payload = {"first_name": "Update"}

        url = reverse("user-detail", kwargs={"id_user": user.id_user})
        res = self.client.patch(url, new_payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["first_name"], new_payload["first_name"])
