from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    description = models.TextField()

    is_finished = models.BooleanField()

    def __str__(self):
        return self.name


class Outcomes(models.Model):
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE)
    cf = models.FloatField()
    name = models.CharField(max_length=255, default="")

    success = models.BooleanField()

    def is_success(self):
        return self.success is True

    def __str__(self):
        return f"{self.event.name} - {self.name}"
