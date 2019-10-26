from django.db import models

# from django.utils import timezone


# Create your models here.
class SimulatedData(models.Model):

    name = models.CharField(max_length=30)
    owner = models.CharField(max_length=30)
    created_at = models.DateTimeField()

    temperature = models.FloatField()

    acceleration_x = models.FloatField()
    acceleration_y = models.FloatField()
    acceleration_z = models.FloatField()

    wheel_speed_fr = models.FloatField()
    wheel_speed_fl = models.FloatField()
    wheel_speed_br = models.FloatField()
    wheel_speed_bl = models.FloatField()

    suspension_fr = models.FloatField()
    suspension_fl = models.FloatField()
    suspension_br = models.FloatField()
    suspension_bl = models.FloatField()

    def __str__(self):
        return self.name


# class Vehicle(models.Model):
#     name = models.CharField(max_length=30)
#     owner = models.CharField(max_length=30)
#     created_at = models.DateTimeField()


# class EngineTemperatureSensor(models.Model):
#     format = "celsius"
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
#     temperature = models.IntegerField()
#     timestamp = models.DateTimeField("date measurement was taken")
#     now = timezone.now()
#
#     def __str__(self):
#         return self.temperature
#
#
# class SuspensionSensor(models.Model):
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
#     compression = models.IntegerField()
#     timestamp = models.DateTimeField("date measurement was taken")
#
#     def __str__(self):
#         return self.compression
