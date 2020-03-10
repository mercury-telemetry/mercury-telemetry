from django.db import models
from django.contrib.postgres.fields import JSONField
import uuid
from django.utils import timezone


class AGVenue(models.Model):

    venue_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venue_name = models.CharField(max_length=100, blank=True)
    venue_description = models.CharField(max_length=100, null=False, blank=True)
    venue_latitude = models.FloatField()
    venue_longitude = models.FloatField()


class AGEvent(models.Model):
    """This model stores the information about events. When a new event is created,
    a UUID4-typed event_uuid will be assigned to this event and also store the current
    date for this event. """

    event_uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_name = models.CharField(max_length=40, blank=True)
    event_date = models.DateTimeField(default=timezone.now)
    event_description = models.CharField(max_length=100, null=False, blank=True)
    event_venue = models.ForeignKey(AGVenue, null=True, on_delete=models.SET_NULL)


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
