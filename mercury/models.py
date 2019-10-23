from django.db import models
from django.utils import timezone

# Create your models here.


class Vehicle(models.Model):
    name = models.CharField(max_length=30)
    owner = models.CharField(max_length=30)
    created_at = models.DateTimeField()


class EngineTemperatureSensor(models.Model):
    format = "celsius"
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    temperature = models.IntegerField()
    timestamp = models.DateTimeField("date measurement was taken")
    now = timezone.now()

    def __str__(self):
        return self.temperature
