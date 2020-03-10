from rest_framework import serializers
from .models import AGEvent, AGVenue, AGSensor, AGMeasurement
import uuid


class AGEventSerializer(serializers.ModelSerializer):
    agEventID = serializers.UUIDField(
        source="event_uuid", read_only=True, default=uuid.uuid4
    )
    agEventName = serializers.CharField(source="event_name")
    agEventDate = serializers.DateTimeField(source="event_date")
    agEventDescription = serializers.CharField(source="event_description")
    agEventVenue = serializers.CharField(source="event_venue")

    class Meta:
        model = AGEvent
        fields = [
            "agEventID",
            "agEventName",
            "agEventDate",
            "agEventDescription",
            "agEventVenue",
        ]


class AGVenueSerializer(serializers.ModelSerializer):
    agVenueID = serializers.UUIDField(
        source="venue_uuid", read_only=True, default=uuid.uuid4
    )
    agVenueName = serializers.CharField(source="venue_name")
    agVenueDescription = serializers.CharField(source="venue_description")
    agVenueLatitude = serializers.CharField(source="venue_latitude")
    agVenueLongitude = serializers.CharField(source="venue_longitude")

    class Meta:
        model = AGVenue
        fields = [
            "agVenueID",
            "agVenueName",
            "agVenueDescription",
            "agVenueLatitude",
            "agVenueLongitude",
        ]


class AGSensorSerializer(serializers.ModelSerializer):
    agSensorID = serializers.IntegerField(source="sensor_id", read_only=True)
    agSensorName = serializers.CharField(source="sensor_name")
    agSensorFormula = serializers.IntegerField(source="sensor_processing_formula")
    agSensorFormat = serializers.CharField(source="sensor_format")

    class Meta:
        model = AGSensor
        fields = ["agSensorID", "agSensorName", "agSensorFormula", "agSensorFormat"]


class AGMeasurementSerializer(serializers.ModelSerializer):
    agMeasurementID = serializers.UUIDField(
        source="measurement_uuid", read_only=True, default=uuid.uuid4
    )
    agMeasurementTimestamp = serializers.DateTimeField(source="measurement_timestamp")
    agMeasurementEvent = serializers.UUIDField(source="measurement_event")
    agMeasurementSensor = serializers.UUIDField(source="measurement_sensor")
    agMeasurementValue = serializers.JSONField(source="measurement_value")

    class Meta:
        model = AGMeasurement
        fields = [
            "agMeasurementID",
            "agMeasurementTimestamp",
            "agMeasurementEvent",
            "agMeasurementSensor",
            "agMeasurementValue",
        ]
