from django.db import models
from django.utils import timezone

# Create your models here.


class EngineTemperatureSensor(models.Model):
    format = "celsius"
    temperature = models.IntegerField()
    timestamp = models.DateTimeField("date measurement was taken")
    now = timezone.now()

    def __str__(self):
        return self.temperature
