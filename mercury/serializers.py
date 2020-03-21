from rest_framework import serializers

from mercury.models import AGEvent, AGMeasurement, AGSensor


class AGEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = AGEvent
        fields = ["event_name", "event_date", "event_description", "event_location"]


class AGMeasurementSerializer(serializers.ModelSerializer):
    """
    Serializer for the Model AGMeasurement.
    """
    measurement_sensor = serializers.PrimaryKeyRelatedField(read_only=False, queryset=AGSensor.objects.all())
    measurement_event = serializers.PrimaryKeyRelatedField(read_only=False, queryset=AGEvent.objects.all())

    class Meta:
        model = AGMeasurement
        fields = ("measurement_timestamp", "measurement_sensor",
                  "measurement_event", "measurement_value")
