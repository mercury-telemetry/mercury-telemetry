import logging
import glob
import serial
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import HttpResponse

log = logging.getLogger(__name__)


class HardwareView(TemplateView):
    def get(self, request, *args, **kwargs):
        """The get request sent from web to determine the parameters of the serial port
            Url Sample:
            https://localhost:8000/hardware?enable=1&baudrate=8000&bytesize=8
                &parity=N&stopbits=1&timeout=None
            enable: must define, set the port on if 1, off if 0
            port: must define, port number
            baudrate: Optional, default 9600
            bytesize: Optional, default 8 bits
            parity: Optional, default no parity
            stop bits: Optional, default one stop bit
            timeout: Optional, default 1 second
            """
        enable = request.GET.get("enable")
        if enable is None:
            return

        ser = serial.Serial()
        if enable:
            ports = glob.glob("/dev/tty.*")
            ser.port = ports[0]
            if request.GET.get("baudrate"):
                ser.baudrate = request.GET.get("baudrate")
            if request.GET.get("bytesize"):
                ser.bytesize = request.GET.get("bytesize")
            if request.GET.get("parity"):
                ser.parity = request.GET.get("parity")
            if request.GET.get("stopbits"):
                ser.stopbits = request.GET.get("stopbits")
            if request.GET.get("timeout"):
                ser.timeout = request.GET.get("timeout")
            ser.open()
            log.info("Serial port is open")
            messages.info("Serial port is open")
            while ser.is_open:
                # Store data into database
                j = ser.read_until()
                print(j)
        else:
            port = request.GET.get("port")
            ser.port = port
            ser.close()
            log.info("Serial port is close")
            messages.info("Serial port is close")

        return HttpResponse(status=201)
