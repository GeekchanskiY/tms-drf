from rest_framework import serializers

from .models import Event, Outcomes


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "date", "description", "is_finished"]


class OutcomeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Outcomes
        fields = ["id", "name", "event", "success", "cf"]
