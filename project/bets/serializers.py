from rest_framework import serializers

from .models import Bet


class BetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bet
        fields = ["id", "outcome", "user", "amount", "cf"]


class BetResponseSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    cf = serializers.FloatField()
    event = serializers.CharField()
    outcome = serializers.CharField()


class BetsListResponseSerializer(serializers.Serializer):
    bets = BetResponseSerializer(many=True)


class BetRequestSerizalizer(serializers.Serializer):
    amount = serializers.FloatField()
    outcome = serializers.IntegerField()
