from rest_framework import permissions, viewsets

from .models import Event, Outcomes
from .serializers import EventSerializer, OutcomeSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAdminUser]


class OutcomeViewSet(viewsets.ModelViewSet):
    queryset = Outcomes.objects.all()
    serializer_class = OutcomeSerializer
    permission_classes = [permissions.IsAdminUser]
