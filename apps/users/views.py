from rest_framework.viewsets import ModelViewSet

from apps.users.models import User
from apps.users.permissions import IsAdmin
from apps.users.serializers import UserSeriaizer


class IsAdminModelViewSet(ModelViewSet):
    permission_classes = (IsAdmin,)


class UserViweSet(IsAdminModelViewSet):
    queryset = User.objects.all().order_by("id_user")
    serializer_class = UserSeriaizer
    lookup_field = "id_user"
    search_fields = ("email", "first_name", "last_name")
