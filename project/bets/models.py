from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from events.models import Outcomes
from users.models import Profile


class Bet(models.Model):
    outcome = models.ForeignKey(to=Outcomes, on_delete=models.CASCADE)
    user = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    amount = models.FloatField()
    cf = models.FloatField()

    def __str__(self):
        return f"{self.user.user.username} - {self.outcome.event.name}: {self.amount}"


@receiver(post_save, sender=Outcomes, dispatch_uid="pay_all_bets")
def delete_balance_cache(sender, instance: Outcomes, **kwargs):
    if not instance.success:
        return

    bets = Bet.objects.filter(outcome=instance)

    for bet in bets:
        bet.user.balance += bet.amount * bet.cf
        bet.user.save()
