from rest_framework import serializers

from .models import Bet


class BetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bet
        fields = ["id", "outcome", "user", "amount", "cf"]
