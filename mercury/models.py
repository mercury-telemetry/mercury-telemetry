from django.db import models
from django.contrib.postgres.fields import JSONField
import uuid
from django.utils import timezone


class AGEvent(models.Model):
    """This model stores the information about events. When a new event is created,
    a UUID4-typed event_uuid will be assigned to this event and also store the current
    date for this event. """

    event_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_name = models.CharField(max_length=40, blank=True)
    event_date = models.DateTimeField(default=timezone.now)
    event_description = models.CharField(max_length=100, null=False, blank=True)
    event_location = models.CharField(max_length=100, null=False, blank=True)


class AGSensor(models.Model):
    sensor_id = models.AutoField(primary_key=True)
    sensor_name = models.CharField(max_length=1024, blank=True)
    sensor_processing_formula = models.IntegerField(default=0, null=False)
    sensor_format = JSONField()


class AGMeasurement(models.Model):
    measurement_uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    measurement_timestamp = models.DateTimeField(default=timezone.now, blank=False)
    measurement_event = models.ForeignKey(
        AGEvent, on_delete=models.CASCADE, blank=False, null=False
    )
    measurement_sensor = models.ForeignKey(
        AGSensor, on_delete=models.CASCADE, blank=False, null=False
    )
    measurement_value = JSONField()


class GFConfig(models.Model):
    """
    Grafana configs
    """

    gf_name = models.CharField(max_length=64)
    gf_host = models.CharField(max_length=128)
    gf_token = models.CharField(
        max_length=256
    )  # token only, without the prefix "Bearer "
    gf_current = models.BooleanField(default=False, blank=True)


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


class Events(models.Model):
    """This model stores the information about events. When a new event is created,
    an auto-incremented event_id will be assigned to this event and also store the current
    date and location for this event. """

    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=40, unique=True, null=False, blank=False)
    event_date = models.DateTimeField()
    event_loc_lat = models.FloatField(default=0, blank=True)
    event_loc_lon = models.FloatField(default=0, blank=True)
    event_description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return Events.__name__


class Sensor(models.Model):
    """This model stores the information about sensor. When a new sensor is created,
        an auto-incremented sensor_id will be assigned to this event and also store the name
        and description for this sensor . """

    sensor_id = models.AutoField(primary_key=True)
    sensor_name = models.CharField(max_length=40, unique=True, null=False, blank=False)
    sensor_description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return Sensor.__name__


class Field(models.Model):
    """This model stores the information about fields of sensors. """

    field_id = models.IntegerField(unique=True)
    sensor_id = models.ForeignKey(
        Sensor,
        related_name="sensor_field",
        to_field="sensor_id",
        on_delete=models.CASCADE,
    )
    field_name = models.CharField(max_length=40, null=False, blank=False)

    class Meta:
        unique_together = (("field_id", "sensor_id"),)

    def __str__(self):
        return Field.__name__


class General_data(models.Model):
    event_id = models.OneToOneField(
        Events, related_name="event_data", on_delete=models.CASCADE, to_field="event_id"
    )
    sensor_id = models.OneToOneField(
        Sensor,
        related_name="sensor_data",
        on_delete=models.CASCADE,
        to_field="sensor_id",
    )
    field_id = models.OneToOneField(
        Field, related_name="field_data", on_delete=models.CASCADE, to_field="field_id"
    )
    stored_at_time = models.DateTimeField()  # index
    data_value = models.FloatField(default=0)

    class Meta:
        unique_together = (("event_id", "sensor_id", "field_id"),)

    def __str__(self):
        return General_data.__name__
