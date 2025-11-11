from rest_framework import permissions, viewsets

from .serializers import EventSerializer, OutcomeSerializer
from .models import Event, Outcomes


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]


class OutcomeViewSet(viewsets.ModelViewSet):
    queryset = Outcomes.objects.all()
    serializer_class = OutcomeSerializer
    permission_classes = [permissions.AllowAny]