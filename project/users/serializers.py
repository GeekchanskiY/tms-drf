from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "balance"]


class BalanceInfoSerializer(serializers.Serializer):
    balance = serializers.FloatField(required=True)
