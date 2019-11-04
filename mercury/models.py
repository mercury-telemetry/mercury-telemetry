from django.db import models


class SimulatedData(models.Model):

    # basic information about the user
    name = models.CharField(max_length=30)
    owner = models.CharField(max_length=30)
    created_at = models.DateTimeField()

    # temperature panel
    temperature = models.FloatField(default=0)

    # Acceleration Panel
    acceleration_x = models.FloatField(default=0)
    acceleration_y = models.FloatField(default=0)
    acceleration_z = models.FloatField(default=0)

    # Wheel Speed Panel for each of the four wheels
    wheel_speed_fr = models.FloatField(default=0)
    wheel_speed_fl = models.FloatField(default=0)
    wheel_speed_br = models.FloatField(default=0)
    wheel_speed_bl = models.FloatField(default=0)

    # Suspension/Compression Panel for each of the four wheels
    suspension_fr = models.FloatField(default=0)
    suspension_fl = models.FloatField(default=0)
    suspension_br = models.FloatField(default=0)
    suspension_bl = models.FloatField(default=0)

    # Fuel Supply Panel
    initial_fuel = models.FloatField(default=0)
    fuel_decrease_rate = models.FloatField(default=0)

    # Oil Supply/Level Panel
    initial_oil = models.FloatField(default=0)
    oil_decrease_rate = models.FloatField(default=0)

    def __str__(self):  # pragma: no cover
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
