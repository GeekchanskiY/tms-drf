from django.core.cache import cache
from datetime import datetime

from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Profile
from .serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]


class ProfileBalanceCheck(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        now = datetime.now()

        # BAD PRACTICE: data may be overwritten without updating the cache
        value = cache.get(request.user.id)
        if value:
            end = datetime.now()
            print(f"Cache hit time taken: {(end - now).total_seconds()} ms")

            return Response({"balance": value})

        profile = Profile.objects.get(user__id=request.user.id)

        cache.set(request.user.id, profile.balance, timeout=300)

        end = datetime.now()
        print(f"Cache hit time taken: {(end - now).total_seconds()} ms")
        return Response({"balance": profile.balance})
