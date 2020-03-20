import os
import json
import serial
from utils import get_logger  # , get_serial_stream

logging = get_logger("RECEIVER_LOG_FILE")

logging.info("Opening serial")
ser = serial.Serial(
    port=os.environ["RADIO_RECEIVER_PORT"],
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1,
)

logging.info("listening")
while 1:
    x = ser.readline().decode("utf-8")
    if x != "":
        try:
            message = json.loads(x)
            logging.info(message)
            print(message["value"]["value_c_name"])  # indexes into JSON message
        except json.JSONDecodeError:
            logging.error(message)
