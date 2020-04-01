import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mercury.models import AGEvent
from mercury.serializers import AGMeasurementSerializer


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
            event = AGEvent.objects.get(event_uuid=event_uuid)
        except AGEvent.DoesNotExist:
            event = False
        if event is False:
            return Response("Wrong uuid in url", status=status.HTTP_400_BAD_REQUEST)

        json_data = request.data
        if isinstance(json_data, str):
            json_data = json.loads(json_data)
        res = {"measurement_event": event_uuid}
        dic = {
            "measurement_timestamp": "date",
            "measurement_sensor": "sensor_id",
            "measurement_value": "values",
        }

        for d in dic:
            if json_data.get(dic[d]) is None:
                return Response(
                    "Missing required params " + dic[d],
                    status=status.HTTP_400_BAD_REQUEST,
                )
            res[d] = json_data[dic[d]]

        serializer = AGMeasurementSerializer(data=res)
        if serializer.is_valid():
            serializer.save()
            return Response("Saved Successfully", status=status.HTTP_200_OK)
        return Response("The model fails to save", status=status.HTTP_400_BAD_REQUEST)
