import json

from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from ag_data.models import AGActiveEvent
from ag_data.serializers import AGMeasurementSerializer


def build_error(str):
    return json.dumps({"error": str})


def fetch_event():
    try:
        active_event = AGActiveEvent.objects.first()
        event = active_event.first().agevent
    except (AGActiveEvent.DoesNotExist, AttributeError):
        return Response(build_error("No active events"), status=status.HTTP_404_NOT_FOUND)

    return event


def add_measurement(request, event):
    json_data = request.data

    res = {"event_uuid": event.uuid}
    key_map = {"timestamp": "date", "sensor_id": "sensor_id", "value": "values"}

    for key, json_key in key_map.items():
        if json_key not in json_data:
            return Response(
                build_error("Missing required params " + json_key),
                status=status.HTTP_400_BAD_REQUEST,
            )
        res[key] = json_data[json_key]

    serializer = AGMeasurementSerializer(data=res)
    try:
        serializer.is_valid(raise_exception=True)
        serializer.save()
    except serializers.ValidationError:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MeasurementView(APIView):
    def post(self, request):
        """
        The post receives sensor data through internet
        Url example:
        http://localhost:8000/measurement/
        Post Json Data Example
        {
          "sensor_id": 1,
          "values": {
            "power" : "1",
            "speed" : "2",
          }
          "date" : 2020-03-11T20:20+01:00
        }

        TODO: fetch the active event
        Now we use the first event in the db
        """
        event = fetch_event()
        if isinstance(event, Response):
            return event

        return add_measurement(request, event)
