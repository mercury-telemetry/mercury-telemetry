from django.db import models

# from django.utils import timezone


# Create your models here.
class SimulatedData(models.Model):

    name = models.CharField(max_length=30)
    owner = models.CharField(max_length=30)
    created_at = models.DateTimeField()

    temperature = models.IntegerField()

    acceleration_x = models.IntegerField()
    acceleration_y = models.IntegerField()
    acceleration_z = models.IntegerField()

    wheel_speed_fr = models.IntegerField()
    wheel_speed_fl = models.IntegerField()
    wheel_speed_br = models.IntegerField()
    wheel_speed_bl = models.IntegerField()

    suspension_fr = models.IntegerField()
    suspension_fl = models.IntegerField()
    suspension_br = models.IntegerField()
    suspension_bl = models.IntegerField()

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
