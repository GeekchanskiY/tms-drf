from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import get_user_cache_key


class Profile(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.FloatField()

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=Profile, dispatch_uid="clear_profile_cache")
def delete_balance_cache(sender, instance, **kwargs):
    cache.delete(get_user_cache_key(instance.user.id))
