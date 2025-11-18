from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.FloatField()





    def __str__(self):
        return self.user.username
