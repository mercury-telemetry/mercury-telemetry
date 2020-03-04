from django.db import models

# Create your models here.
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
    event_enabled = models.BooleanField(blank=False, default=True)

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
