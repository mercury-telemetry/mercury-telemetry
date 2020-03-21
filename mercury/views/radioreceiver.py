import glob
import json

import serial
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mercury.serializers import AGMeasurementSerializer


class RadioReceiverView(APIView):
    """
    This is a Django REST API supporting user to send GET request fetching the RADIO
    module configuration settings from backend and to send POST request sending
    JSON-formatted data.
    """

    def get(self, request, event_uuid=None):
        """
        The get request sent from web to determine the parameters of the serial port
            Url Sample:
            https://localhost:8000/radioreceiver/d81cac8d-26e1-4983-a942-1922e54a943d?
                eventid=1&enable=1&baudrate=8000&bytesize=8&parity=N&stopbits=1&timeout=None
            uuid: event_uuid
            enable: must define, set the port on if 1, off if 0
            baudrate: Optional, default 9600
            bytesize: Optional, default 8 bits
            parity: Optional, default no parity
            stop bits: Optional, default one stop bit
            timeout: Optional, default 1 second
            """
        params = request.query_params

        enable = params.get("enable")
        if enable is None:
            return Response("Missing enable value in url", status=status.HTTP_400_BAD_REQUEST)
        enable = int(enable)
        ser = serial.Serial()
        ports = glob.glob("/dev/tty.*")
        ser.port = ports[0]

        res = {"enable": enable}

        if params.get("baudrate"):
            ser.baudrate = params.get("baudrate")
        if params.get("bytesize"):
            ser.bytesize = params.get("bytesize")
        if params.get("parity"):
            ser.parity = params.get("parity")
        if params.get("stopbits"):
            ser.stopbits = params.get("stopbits")
        if params.get("timeout"):
            ser.timeout = params.get("timeout")

        if enable:
            ser.open()
            if ser.is_open:
                # Call Script
                self.call_script(event_uuid)
        else:
            if ser.is_open:
                ser.close()

        res["baudrate"] = ser.baudrate
        res["bytesize"] = ser.bytesize
        res["parity"] = ser.parity
        res["stopbits"] = ser.stopbits
        res["timeout"] = ser.timeout

        return Response(json.dumps(res), status=status.HTTP_200_OK)

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
        json_data = request.data

        if len(json_data) != 3:
            return Response("Missing required params", status=status.HTTP_400_BAD_REQUEST)

        res = {"measurement_event": event_uuid}
        dic = {"measurement_timestamp": "date",
               "measurement_sensor": "sensor_id", "measurement_value": "values"}

        for d in dic:
            res[d] = json_data[dic[d]]

        serializer = AGMeasurementSerializer(data=res)
        if serializer.is_valid():
            serializer.save()
            return Response("Saved Successfully", status=status.HTTP_200_OK)
        return Response("Bad Request", status=status.HTTP_400_BAD_REQUEST)

    def call_script(self, para):
        """
        Run a shell script to receive radio sensor data from the vehicle
        This script will call local server to store all data received
        """
        s_para = para
        # subprocess.call()
