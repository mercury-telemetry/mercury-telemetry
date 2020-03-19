import glob
import json

import serial
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
import subprocess


class RadioReceiverView(APIView):
    """
    This is a Django REST API supporting user to send GET request fetching the RADIO
    module configuration settings from backend and to send POST request sending
    JSON-formatted data.
    """

    def get(self, request, format=None):
        """
        The get request sent from web to determine the parameters of the serial port
            Url Sample:
            https://localhost:8000/radioreceiver?enable=1&baudrate=8000&bytesize=8
                &parity=N&stopbits=1&timeout=None
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
            return
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
                self.call_script("")
        else:
            if ser.is_open:
                ser.close()

        res["baudrate"] = ser.baudrate
        res["bytesize"] = ser.bytesize
        res["parity"] = ser.parity
        res["stopbits"] = ser.stopbits
        res["timeout"] = ser.timeout

        return Response(json.dumps(res), status=status.HTTP_200_OK)

    def call_script(self, para):
        """
        Run a shell script to receive radio sensor data from the vehicle
        This script will call local server to store all data received
        """
        s_para = para
        # subprocess.call()
