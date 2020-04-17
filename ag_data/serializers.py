import json

from django.core.serializers.json import DjangoJSONEncoder
from rest_framework import serializers

from ag_data.models import AGEvent, AGSensor, AGMeasurement


class AGJSONSerializerField(serializers.JSONField):
    """
    Modified JSONFieldSerializer
    If self.binary is True, this serializer will only save data as dict-like value in JSONField
    If self.binary is False and the data is json string, the data will be saved as string
    """

    def to_internal_value(self, data):

        try:
            # If the binary is true, check whether data is a valid Json String
            if self.binary or getattr(data, "is_json_string", False):
                if isinstance(data, bytes):
                    data = data.decode()
                return json.loads(data)
        except (TypeError, ValueError):
            # If the data is a dict, return it directly
            return data

        """If the binary is false, check whether data is a valid Json Dict"""
        try:
            json.dumps(data, cls=self.encoder)
        except ValueError:
            self.fail("Invalid")
        return data


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
    value = AGJSONSerializerField(binary=True, encoder=DjangoJSONEncoder)
    timestamp = serializers.DateTimeField()

    class Meta:
        model = AGMeasurement
        fields = ("timestamp", "sensor_id", "event_uuid", "value")
