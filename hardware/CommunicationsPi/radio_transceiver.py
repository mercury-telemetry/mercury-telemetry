import os
import time
import serial
import json

from utils import get_logger, get_serial_stream
class Transceiver:
    def __init__(self, log_file_name=None, port=None):
        if log_file_name is None:
            self.logging = get_logger("TRANSMITTER_LOG_FILE")
        else:
            self.logging = get_logger(log_file_name)

        port = os.environ["RADIO_TRANSMITTER_PORT"] if port is None else port
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1,

        self.logging.info("Opening serial")
        self.serial = serial.Serial(
                port=port,
                baudrate=baudrate,
                parity=parity,
                stopbits=stopbits,
                bytesize=bytesize,
                timeout=1,
                )


    def send(self, payload):
        self.logging.info("sending")
        self.serial.write(get_serial_stream(payload))
        self.logging.info(payload)

    def listen(self):
        payload = self.serial.readline().decode("utf-8")
        message = 'Error: Check logs'
        if payload is not "":
            try:
                message = json.loads(payload)
                self.logging.info(message)
            except json.JSONDecodeError:
                logging.error(json.JSONDecodeError)
        return message
