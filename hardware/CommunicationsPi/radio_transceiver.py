import os
import serial
import json
import serial.tools.list_ports

from hardware.Utils.utils import get_logger, get_serial_stream


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
        else:
            port_info = next(
                (
                    p
                    for p in serial.tools.list_ports.comports()
                    if p.device == self.port
                ),
                {},
            )
            self.port_vid = port_info.vid if hasattr(port_info, "vid") else None
            self.port_pid = port_info.pid if hasattr(port_info, "pid") else None
            self.port_vendor = (
                port_info.manufacturer if hasattr(port_info, "manufacturer") else None
            )
            self.port_intf = (
                port_info.interface if hasattr(port_info, "interface") else None
            )
            self.port_serial_number = (
                port_info.serial_number if hasattr(port_info, "serial_number") else None
            )
            self.find_port()

        baudrate = os.environ["TRANSCEIVER_BAUDRATE"]
        parity = serial.PARITY_NONE
        stopbits = serial.STOPBITS_ONE
        bytesize = serial.EIGHTBITS
        timeout = int(os.environ["TRANSCEIVER_TIMEOUT"])

        self.logging.info("Opening serial on: " + str(self.port))
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=baudrate,
                parity=parity,
                stopbits=stopbits,
                bytesize=bytesize,
                timeout=timeout,
            )
        except Exception as err:
            self.logging.error("error occurred: {}".format(str(err)))
            raise

    def find_port(self):
        for port in serial.tools.list_ports.comports():
            if self.is_usb_serial(port):
                self.logging.info("Port device found: " + str(port.device))
                self.port = port.device
                return

        return

    def is_usb_serial(self, port):
        if port.vid is None:
            return False
        if self.port_vid is not None:
            if port.vid != self.port_vid:
                return False
        if self.port_pid is not None:
            if port.pid != self.port_pid:
                return False
        if self.port_vendor is not None:
            if not port.manufacturer.startswith(self.port_vendor):
                return False
        if self.port_serial_number is not None:
            if not port.serial_number.startswith(self.port_serial_number):
                return False
        if self.port_intf is not None:
            if port.interface is None or self.port_intf not in port.interface:
                return False
        return True

    def send(self, payload):
        self.logging.info("sending")
        self.serial.write(get_serial_stream(payload))
        self.logging.info(payload)

    def listen(self):
        payload = self.serial.readline().decode("utf-8")
        message = ""
        if payload and len(payload) > 0:
            try:
                message = json.loads(payload)
                self.logging.info(message)
            except json.JSONDecodeError:
                self.logging.error(json.JSONDecodeError)
                raise
            except Exception as err:
                self.logging.error("error occurred: {}".format(str(err)))
                raise
        return message
