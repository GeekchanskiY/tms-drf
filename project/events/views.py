from rest_framework import permissions, viewsets

from .serializers import EventSerializer
from .models import Event


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]