from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from events.views import EventViewSet, OutcomeViewSet
from bets.views import BetViewSet
from users.views import ProfileViewSet

router = routers.DefaultRouter()
router.register(r"events", EventViewSet)
router.register(r"outcomes", OutcomeViewSet)
router.register(r"bets", BetViewSet)
router.register(r"profile", ProfileViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("admin/", admin.site.urls),
]
