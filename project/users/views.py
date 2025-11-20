from datetime import datetime

from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

from .models import Profile
from .serializers import ProfileSerializer
from .utils import get_user_cache_key


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]


class ProfileBalanceCheck(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print("ProfileBalanceCheck called")
        now = datetime.now()

        value = cache.get(get_user_cache_key(request.user.id))
        if value:
            end = datetime.now()
            print(f"Cache hit time taken: {(end - now).total_seconds()}")

            return Response({"balance": value})

        profile = Profile.objects.get(user__id=request.user.id)

        cache.set(get_user_cache_key(request.user.id), profile.balance, timeout=300)

        end = datetime.now()
        print(f"Cache miss time taken: {(end - now).total_seconds()}")

        return Response({"balance": profile.balance})
