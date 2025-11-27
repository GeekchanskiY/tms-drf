from bets.views import BetView, BetViewSet
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from events.views import EventViewSet, OutcomeViewSet
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from users.views import ProfileBalanceCheck, ProfileViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Betting API",
        default_version="v1",
        description="Sample api for betting system",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@mail.ru"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)


router = routers.DefaultRouter()
router.register(r"events", EventViewSet)
router.register(r"outcomes", OutcomeViewSet)
router.register(r"bets", BetViewSet)
router.register(r"profile", ProfileViewSet)

urlpatterns = [
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/v1/", include(router.urls)),
    path("api/v1/balance/", ProfileBalanceCheck.as_view(), name="profile-balance"),
    path("api/v1/bet/", BetView.as_view(), name="bet"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("admin/", admin.site.urls),
]
