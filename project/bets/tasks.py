from celery import shared_task

from .models import Bet


@shared_task(bind=True)
def send_bet_messages(self, bet_id):
    bet = Bet.objects.get(id=bet_id)

    bets = Bet.objects.filter(outcome=bet.outcome).exclude(user__id=bet.user.id)

    if len(bets) == 0:
        print("No other bets to notify")

        return

    for b in bets:
        print(
            f"Sending message to user {b.user.user.username} about bet {b.id}, message id {self.request.id}"
        )

    print("All messages sent")
