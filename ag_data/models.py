from django.db import models
from django.contrib.postgres.fields import JSONField
import uuid
from django.utils import timezone


class AGVenue(models.Model):
    """Store the venue where events happens, including name, description, latitude and
    longtitude.
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, null=False, blank=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True
    )


class AGEvent(models.Model):
    """Stores the information about events including name, date and description. 
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=40, blank=True)
    date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=100, null=False, blank=True)
    venue_uuid = models.ForeignKey(AGVenue, null=True, on_delete=models.SET_NULL)


class AGSensorType(models.Model):
    """Stores the information about sensor types which is used to provide a sensor template
    and related formula for different types of sensors.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024, blank=True)
    processing_formula = models.IntegerField(default=0, null=False)
    format = JSONField()


class AGSensor(models.Model):
    """Stores the information about sensors including name and type id.
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1024, blank=True)
    type_id = models.ForeignKey(AGSensorType, null=False, on_delete=models.PROTECT)


class AGMeasurement(models.Model):
    """Stores the information about sensor measurements, including timestamp, event, sensor
    id and measurement values.
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(default=timezone.now, blank=False)
    measurement_event = models.ForeignKey(
        AGEvent, on_delete=models.CASCADE, blank=False, null=False
    )
    sensor_id = models.ForeignKey(
        AGSensor, on_delete=models.CASCADE, blank=False, null=False
    )
    value = JSONField()
