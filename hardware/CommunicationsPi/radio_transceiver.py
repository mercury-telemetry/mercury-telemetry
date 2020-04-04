import os
import serial
import json
import serial.tools.list_ports

from .utils import get_logger, get_serial_stream


class Transceiver:
    def __init__(self, log_file_name=None, port=None):
        if log_file_name is None:
            self.logging = get_logger("TRANSMITTER_LOG_FILE")
        else:
            self.logging = get_logger(log_file_name, log_file_name)

        self.port = os.environ["RADIO_TRANSMITTER_PORT"] if port is None else port

        if not self.port:
            self.port_vid = None
            self.port_pid = None
            self.port_vendor = None
            self.port_intf = None
            self.port_serial_number = None
            self.find_port()

        baudrate = 9600
        parity = serial.PARITY_NONE
        stopbits = serial.STOPBITS_ONE
        bytesize = serial.EIGHTBITS
        timeout = 1

        self.logging.info("Opening serial on: " + str(self.port))
        self.serial = serial.Serial(
            port=self.port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout,
        )

    def find_port(self):
        for port in serial.tools.list_ports.comports():
            if self.is_usb_serial(port):
                self.logging.info("Port device found: " + str(port.get("device")))
                self.port = port.get("device")
                return

        return

    def is_usb_serial(self, port):
        if port.get("vid") is None:
            return False
        if self.port_vid is not None:
            if port.get("vid") != self.port_vid:
                return False
        if self.port_pid is not None:
            if port.get("pid") != self.port_pid:
                return False
        if self.port_vendor is not None:
            if not port.get("manufacturer").startswith(self.port_vendor):
                return False
        if self.port_serial_number is not None:
            if not port.get("serial_number").startswith(self.port_serial_number):
                return False
        if self.port_intf is not None:
            if port.get("interface") is None or self.port_intf not in port.get(
                "interface"
            ):
                return False
        return True

    def send(self, payload):
        self.logging.info("sending")
        self.serial.write(get_serial_stream(payload))
        self.logging.info(payload)

    def listen(self):
        payload = self.serial.readline().decode("utf-8")
        message = "Error: Check logs"
        if payload != "":
            try:
                message = json.loads(payload)
                self.logging.info(message)
            except json.JSONDecodeError:
                self.logging.error(json.JSONDecodeError)
        return message
