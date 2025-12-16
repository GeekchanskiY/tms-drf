from datetime import datetime

from django.core.cache import cache
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from project.celery import debug_task
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import BalanceInfoSerializer, ProfileSerializer
from .utils import get_user_cache_key


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]


balance_check_response = openapi.Response(
    "current balance", schema=BalanceInfoSerializer
)


class ProfileBalanceCheck(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get current user balance info",
        responses={200: balance_check_response},
    )
    def get(self, request, *args, **kwargs):
        print("ProfileBalanceCheck called")
        now = datetime.now()

        value = cache.get(get_user_cache_key(request.user.id))
        if value:
            end = datetime.now()
            print(f"Cache hit time taken: {(end - now).total_seconds()}")

            serializer = BalanceInfoSerializer({"balance": value})

            return Response(serializer.data)

        profile = Profile.objects.get(user__id=request.user.id)

        cache.set(get_user_cache_key(request.user.id), profile.balance, timeout=300)

        end = datetime.now()
        print(f"Cache miss time taken: {(end - now).total_seconds()}")

        serializer = BalanceInfoSerializer(
            data={"balance": profile.balance},
        )

        if not serializer.is_valid():
            return Response(status=500)

        debug_task.delay()

        return Response(serializer.validated_data, status=200)
