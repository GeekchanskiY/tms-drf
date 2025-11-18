from django.db import models

from events.models import Outcomes
from users.models import Profile


class Bet(models.Model):
    outcome = models.ForeignKey(to=Outcomes, on_delete=models.CASCADE)
    user = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    amount = models.FloatField()
    cf = models.FloatField()

    def __str__(self):
        return f"{self.user.user.username} - {self.outcome.event.name}: {self.amount}"
