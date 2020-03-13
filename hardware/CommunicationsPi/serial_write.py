# test firmware to run from RPi that transmit JSON over serial

import time
import serial
import json

ser = serial.Serial(
    port="/dev/ttyUSB0",
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1,
)

while 1:

    # JSON message
    message = {
        "id": 5,
        "value": {"value_a_name": 15.0, "value_b_name": 26.5, "value_c_name": 13.3},
    }

    message_serial = json.dumps(message)
    ser.write(
        str(message_serial) + "\n"
    )  # newline gives linebreak needed for ser.readline() on receiving end

    time.sleep(1)
