import os
import time
import serial

# import json

from utils import get_logger, get_serial_stream

logging = get_logger("TRANSMITTER_LOG_FILE")

logging.info("Opening serial")
ser = serial.Serial(
    port=os.environ["RADIO_TRANSMITTER_PORT"],
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1,
)

logging.info("sending")

while 1:
    message = {
        "id": 5,
        "value": {"value_a_name": 15.0, "value_b_name": 26.5, "value_c_name": 13.3},
    }
    ser.write(get_serial_stream(message))
    logging.info(message)
    time.sleep(1)
