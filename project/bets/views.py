from django.core.exceptions import ObjectDoesNotExist
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from events.models import Outcomes
from rest_framework import permissions, viewsets
from rest_framework.views import APIView, Response
from users.models import Profile
from utils.serializers import ErrorResponseSerializer

from .models import Bet
from .serializers import (
    BetRequestSerizalizer,
    BetResponseSerializer,
    BetSerializer,
    BetsListResponseSerializer,
)
from .tasks import send_bet_messages


class BetViewSet(viewsets.ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
    permission_classes = [permissions.IsAuthenticated]


class BetView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get active bets",
        responses={200: BetsListResponseSerializer},
    )
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user__id=request.user.id)

        bets = Bet.objects.filter(user=profile, outcome__event__is_finished=False)

        response_serializer = BetsListResponseSerializer(
            data={
                "bets": [
                    {
                        "amount": bet.amount,
                        "cf": bet.cf,
                        "event": bet.outcome.event.name,
                        "outcome": bet.outcome.name,
                    }
                    for bet in bets
                ]
            }
        )
        if not response_serializer.is_valid():
            return Response(status=500)

        return Response(data=response_serializer.validated_data, status=200)

    @swagger_auto_schema(
        operation_description="Make a bet",
        request_body=BetRequestSerizalizer,
        responses={200: BetResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        serializer = BetRequestSerizalizer(data=request.data)
        if not serializer.is_valid():
            return Response(
                ErrorResponseSerializer(
                    {"message": "invalid request", "details": serializer.errors}
                ).data,
                status=400,
            )

        amount = serializer.data["amount"]
        outcome_id = serializer.data["outcome"]

        try:
            outcome = Outcomes.objects.get(id=outcome_id)
        except ObjectDoesNotExist:
            return Response(
                ErrorResponseSerializer(
                    {
                        "message": "selected outcome not found",
                        "details": {
                            "outcome": [
                                "object does not exists",
                            ],
                        },
                    }
                ).data,
                status=404,
            )

        profile = Profile.objects.get(user__id=request.user.id)

        if profile.balance < amount:
            return Response(
                ErrorResponseSerializer(
                    {
                        "message": "invalid request",
                        "details": {
                            "amount": [
                                "bet amount > current profile balance",
                            ],
                        },
                    }
                ).data,
                status=400,
            )

        profile.balance -= amount
        profile.save()

        Bet.objects.create(
            outcome=outcome,
            user=profile,
            cf=outcome.cf,
            amount=amount,
        )

        response_serializer = BetResponseSerializer(
            data={
                "outcome": outcome.name,
                "cf": outcome.cf,
                "event": outcome.event.name,
                "amount": amount,
            }
        )
        if not response_serializer.is_valid():
            return Response(status=500)

        send_bet_messages.delay(bet_id=outcome.id)

        return Response(response_serializer.validated_data, status=201)
