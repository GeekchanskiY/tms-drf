from django.contrib import admin
from .models import Event, Outcomes

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(Outcomes)
class OutcomeAdmin(admin.ModelAdmin):
    pass