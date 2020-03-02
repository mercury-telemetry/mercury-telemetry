from django.db import models


# Note: the Event will have an ID automatically
class Event(models.Model):
    event_name = models.CharField(max_length=100, null=False, unique=True)
    event_location = models.CharField(max_length=100, null=False, unique=False)
    date = models.DateTimeField(null=False)
    comments = models.TextField(null=True)

    def __str__(self):  # pragma: no cover
        return Event.__name__


class TemperatureSensor(models.Model):
    """This model represents the Temperature sensor that we expect to
    be potentially available in the future in the NYU Motorsports
    Racing vehicle."""

    created_at = models.DateTimeField()
    # Oil temperature panel, measured in fahrenheit degrees
    temperature = models.FloatField(default=0)

    def __str__(self):  # pragma: no cover
        return TemperatureSensor.__name__


class AccelerationSensor(models.Model):
    """This model represents the Acceleration sensors that we expect to
    be potentially available in the future in the NYU Motorsports
    Racing vehicle."""

    created_at = models.DateTimeField()
    # Acceleration Panel, measured in meters/second
    acceleration_x = models.FloatField(default=0)
    acceleration_y = models.FloatField(default=0)
    acceleration_z = models.FloatField(default=0)

    def __str__(self):  # pragma: no cover
        return AccelerationSensor.__name__


class WheelSpeedSensor(models.Model):
    """This model represents the Wheel Speed sensors that we expect to
    be potentially available in the future in the NYU Motorsports
    Racing vehicle."""

    created_at = models.DateTimeField()
    # Wheel Speed Panel for each of the four wheels
    # measured in meters/second
    wheel_speed_fr = models.FloatField(default=0)
    wheel_speed_fl = models.FloatField(default=0)
    wheel_speed_br = models.FloatField(default=0)
    wheel_speed_bl = models.FloatField(default=0)

    def __str__(self):  # pragma: no cover
        return WheelSpeedSensor.__name__


class SuspensionSensor(models.Model):
    """This model represents the Suspension sensors that we expect to
    be potentially available in the future in the NYU Motorsports
    Racing vehicle."""

    created_at = models.DateTimeField()
    # Suspension/Compression Panel for each of the four wheels
    # measured in centimeters
    suspension_fr = models.FloatField(default=0)
    suspension_fl = models.FloatField(default=0)
    suspension_br = models.FloatField(default=0)
    suspension_bl = models.FloatField(default=0)

    def __str__(self):  # pragma: no cover
        return SuspensionSensor.__name__


class FuelLevelSensor(models.Model):
    """This model represents the Fuel Level sensor that we expect to
    be potentially available in the future in the NYU Motorsports
    Racing vehicle."""

    created_at = models.DateTimeField()
    # Fuel Supply Panel
    # measured in liters
    current_fuel_level = models.FloatField(default=0)

    def __str__(self):  # pragma: no cover
        return FuelLevelSensor.__name__


class EventCodeAccess(models.Model):
    """This model stores the information about events. When an event is
    ongoing, if a new event_code is added and the enabled property is
    True, then use of the Telemetry app will be restricted to those
    that know the event_code."""

    event_code = models.CharField(max_length=8)
    enabled = models.BooleanField()

    def __str__(self):  # pragma: no cover
        return EventCodeAccess.__name__
