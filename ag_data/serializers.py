from rest_framework import serializers

from ag_data.models import AGEvent, AGSensor, AGMeasurement


class AGMeasurementSerializer(serializers.ModelSerializer):
    """
    Serializer for the Model AGMeasurement.
    """

    sensor_id = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=AGSensor.objects.all()
    )
    event_uuid = serializers.PrimaryKeyRelatedField(
        read_only=False, queryset=AGEvent.objects.all()
    )

    class Meta:
        model = AGMeasurement
        fields = (
            "timestamp",
            "sensor_id",
            "event_uuid",
            "value",
        )
