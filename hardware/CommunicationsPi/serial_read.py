# Run on macbook receiving messagage via USB serial input

import json
import serial

ser = serial.Serial(
    port="/dev/tty.usbserial-DN05UVK1",
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1,
)

while 1:
    x = ser.readline().decode("utf-8")
    if x is not "":
        try:
            message = json.loads(x)
            print(message)  # full JSON message
            print(message["value"]["value_c_name"])  # indexes into JSON message
        except json.JSONDecodeError:
            print(x)
