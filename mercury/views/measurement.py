import json

from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from ag_data.models import AGEvent
from ag_data.serializers import AGMeasurementSerializer


def build_error(str):
    return json.dumps({"error": str})


def add_measurement(request, event):
    json_data = request.data
    if isinstance(json_data, str):
        json_data = json.loads(json_data)

    res = {"event_uuid": event.uuid}
    key_map = {
        "timestamp": "date",
        "sensor_id": "sensor_id",
        "value": "values",
    }

    for key, json_key in key_map.items():
        if json_key not in json_data:
            return Response(
                build_error("Missing required params " + json_key),
                status=status.HTTP_400_BAD_REQUEST,
            )
        res[key] = json_data[json_key]

    if isinstance(res["value"], str):
        res["value"] = json.loads(res["value"])

    serializer = AGMeasurementSerializer(data=res)
    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except serializers.ValidationError:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MeasurementView(APIView):
    def post(self, request, event_uuid=None):
        """
        The post receives sensor data through internet
        Url example:
        http://localhost:8000/measurement/d81cac8d-26e1-4983-a942-1922e54a943d
        Post Json Data Example
        {
          "sensor_id": 1,
          "values": {
            "power" : "1",
            "speed" : "2",
          }
          "date" : 2020-03-11T20:20+01:00
        }
        """
        # First check event_uuid exists
        try:
            event = AGEvent.objects.get(uuid=event_uuid)
        except AGEvent.DoesNotExist:
            event = False
        if event is False:
            return Response(
                build_error("Event uuid not found"), status=status.HTTP_404_NOT_FOUND
            )

        return add_measurement(request, event)


class MeasurementWithoutEvent(APIView):
    def post(self, request):
        """
        TODO: fetch the active event
        Now we use the first event in the db
        """
        try:
            events = AGEvent.objects.all()
            event = events.first()
        except AGEvent.DoesNotExist:
            event = False

        return add_measurement(request, event)
