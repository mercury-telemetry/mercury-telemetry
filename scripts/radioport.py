import argparse
import json
import os
import time

import requests
import serial


class RadioPort:
    def __init__(self, serial_port):
        self.serial_port = serial_port
        self.url = "http://127.0.0.1:8000/measurement/"

    def post_request(self, data):
        headers = {"Content-type": "application/json"}

        r = requests.post(self.url, json=data, headers=headers)

        print("Status: " + str(r.status_code))
        print("Body: " + str(r.content))

    def post_fake_request(self, data):
        headers = {"Content-type": "application/json"}
        if data is None:
            data = {}
            data["sensor_id"] = 1
            data["date"] = "2020-04-09T19:20:00"
            data["values"] = {"power": "2", "speed": 1}
        # data = json.dumps(data, cls=DjangoJSONEncoder)

        # Skip in travis since there is no database in travis
        if "TRAVIS" in os.environ:
            return
        r = requests.post(self.url, json=data, headers=headers)

        print("Status: " + str(r.status_code))
        print("Body: " + str(r.content))

    def listen_port(self):
        print("Start listening port")
        while self.serial_port.is_open:
            data = self.serial_port.readline()
            self.post_request(data=data)
            time.sleep(1)


if __name__ == "__main__":
    print("Call radioport.py script")
    parser = argparse.ArgumentParser(description="Radio port setter.")
    parser.add_argument("-p", "--port", help="Port name for serial")
    parser.add_argument(
        "-d", "--data", type=json.loads, help="Data to send, must be json string"
    )
    parser.add_argument(
        "-f",
        "--fake",
        default=False,
        type=bool,
        const=True,
        nargs="?",
        help="send the fake post request",
    )

    args = parser.parse_args()

    if args.fake:
        radio_port = RadioPort(None)
        print("Send fake data")
        print(args.data)
        radio_port.post_fake_request(args.data)
    else:
        try:
            ser = serial.Serial(args.port)
            radio_port = RadioPort(ser)
            if ser.is_open:
                radio_port.listen_port()
            else:
                print("Serial is invalid")
        except serial.serialutil.SerialException:
            print("Serial is invalid")
