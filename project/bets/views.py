from rest_framework import permissions, viewsets

from .serializers import BetSerializer
from .models import Bet


class BetViewSet(viewsets.ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
    permission_classes = [permissions.AllowAny]
