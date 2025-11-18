from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

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

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    path("admin/", admin.site.urls),
]
