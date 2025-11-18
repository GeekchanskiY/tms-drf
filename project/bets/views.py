from rest_framework import permissions, viewsets

from .models import Bet
from .serializers import BetSerializer


class BetViewSet(viewsets.ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
    permission_classes = [permissions.AllowAny]
