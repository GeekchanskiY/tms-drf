from django.contrib import admin

from .models import Bet


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    pass
