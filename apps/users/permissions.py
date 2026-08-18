from rest_framework.permissions import BasePermission

from apps.users.models import UserRole


class IsAdmin(BasePermission):
    message = "Only with admin role can access this endpoint"

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", None) == UserRole.ADMIN
        )
