from rest_framework import serializers

from mercury.models import AGEvent, AGMeasurement


class AGEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AGEvent
        fields = ["event_uuid", "event_name", "event_date", "event_description", "event_location"]


class AGMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AGMeasurement
        fields = ["measurement_uuid", "measurement_timestamp", "measurement_event",
                  "measurement_sensor", "measurement_value"]
