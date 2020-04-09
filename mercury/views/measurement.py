import json

from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from ag_data.models import AGEvent
from ag_data.serializers import AGMeasurementSerializer


def build_error(str):
    return json.dumps({"error": str})


class MeasurementView(APIView):
    def post(self, request, event_uuid=None):
        """
        The post receives sensor data through internet
        Url example:
        http://localhost:8000/radioreceiver/d81cac8d-26e1-4983-a942-1922e54a943d
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

        json_data = request.data
        if isinstance(json_data, str):
            json_data = json.loads(json_data)

        res = {"event_uuid": event_uuid}
        dic = {"timestamp": "date", "sensor_id": "sensor_id", "value": "values"}

        for d in dic:
            if json_data.get(dic[d]) is None:
                return Response(
                    build_error("Missing required params " + dic[d]),
                    status=status.HTTP_400_BAD_REQUEST,
                )
            res[d] = json_data[dic[d]]

        serializer = AGMeasurementSerializer(data=res)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except serializers.ValidationError:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
