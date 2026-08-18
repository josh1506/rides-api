from rest_framework.routers import DefaultRouter

from apps.users.views import UserViweSet

router = DefaultRouter()
router.register("users", UserViweSet, basename="user")

urlpatterns = router.urls
