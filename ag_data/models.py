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

    def __str__(self):
        return self.name


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
    event_uuid = models.ForeignKey(
        AGEvent, on_delete=models.CASCADE, blank=False, null=False
    )
    sensor_id = models.ForeignKey(
        AGSensor, on_delete=models.CASCADE, blank=False, null=False
    )
    value = JSONField()


class AGActiveEvent(models.Model):
    agevent = models.ForeignKey(AGEvent, null=True, on_delete=models.SET_NULL)


class ErrorLog(models.Model):
    UNRECOGNIZED_FORMAT = 1001
    MISSING_COLUMN = 1002
    MISSING_FIELD_IN_RAW_READING = 1003
    INVALID_COLUMN = 1004
    INVALID_FIELD_IN_RAW_READING = 1005
    FORMULA_PROCESS_MEASUREMENT_ERROR = 1006
    EXTRANEOUS_KEY_VALUE_PAIR_IN_MEASUREMENT = 1007
    OTHER_ERROR = 1008

    ERROR_CODE_CHOICES = [
        (UNRECOGNIZED_FORMAT, "Unrecognized Format"),
        (MISSING_COLUMN, "Missing Column"),
        (MISSING_FIELD_IN_RAW_READING, "Missing Field In Raw Reading"),
        (INVALID_COLUMN, "Invalid Column"),
        (INVALID_FIELD_IN_RAW_READING, "Invalid Field In Raw Reading"),
        (FORMULA_PROCESS_MEASUREMENT_ERROR, "Error When Formula Processing Measurement"),
        (EXTRANEOUS_KEY_VALUE_PAIR_IN_MEASUREMENT, "Extraneous Key-Value In Measurement")
        (OTHER_ERROR, "Other Error")
    ]

    error_id = models.AutoField(primary_key=True)
    error_timestamp = models.DateTimeField(default=timezone.now)
    error_code = models.IntegerField(choices=ERROR_CODE_CHOICES, null=False)
    error_description = models.CharField(max_length=100, null=False, blank=False)
    error_raw_content = models.CharField(max_length=500, null=False)

    def __str__(self):
        return ErrorLog.__name__