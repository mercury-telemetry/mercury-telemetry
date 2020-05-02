import os
import time
import json

from dotenv import load_dotenv
from hardware.Utils.logger import Logger

logger = Logger(name="main.log", filename="main.log")
logger.info("Started hardware main.py")

PI_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_file = os.path.join(PI_DIR, "hardware/env")
if os.path.isfile(dotenv_file):  # pragma: no cover
    load_dotenv(dotenv_path=dotenv_file)
else:  # pragma: no cover
    print("dotenv_file was not a file")
    logger.info("dotenv_file was not a file")

from hardware.CommunicationsPi.radio_transceiver import Transceiver  # noqa: E402
from hardware.CommunicationsPi.comm_pi import CommPi  # noqa: E402
from hardware.CommunicationsPi.lan_server import runServer  # noqa: E402
from hardware.CommunicationsPi.web_client import WebClient  # noqa: E402
from hardware.SensorPi.sense_pi import SensePi  # noqa: E402
from hardware.Utils.utils import get_sensor_keys  # noqa: E402
from hardware.gpsPi.gps_reader import GPSReader  # noqa: E402


def main():
    if os.environ["HARDWARE_TYPE"] == "commPi":
        logger.info("CommunicationsPi")
        handleComm()
    elif os.environ["HARDWARE_TYPE"] == "sensePi":
        logger.info("SensePi")
        handleSense()
    elif os.environ["HARDWARE_TYPE"] == "gpsPi":
        logger.info("gpsPi")
        handleGps()
    else:
        logger.info("Local Django Server")
        handleLocal()


def handleComm():
    """
    Starts up the CommunicationsPi server and starts listening for
    traffic
    """
    runServer(handler_class=CommPi)


def handleSense():
    """
    Starts up the SensorPi runtime, begins listening for SenseHat input,
    establishing a connection to a local CommPi via LAN, and sending data
    for transmission to the CommPi
    """
    sensor_keys = get_sensor_keys()
    sensor_ids = {}
    sensor_ids[sensor_keys["TEMPERATURE"]] = 2
    sensor_ids[sensor_keys["PRESSURE"]] = 3
    sensor_ids[sensor_keys["HUMIDITY"]] = 4
    sensor_ids[sensor_keys["ACCELERATION"]] = 5
    sensor_ids[sensor_keys["ORIENTATION"]] = 6
    sensePi = SensePi(sensor_ids=sensor_ids)

    client = WebClient()

    while True:
        print("while true")
        temp = sensePi.get_temperature()
        pres = sensePi.get_pressure()
        hum = sensePi.get_humidity()
        acc = sensePi.get_acceleration()
        orie = sensePi.get_orientation()
        all = sensePi.get_all()

        data = [temp, pres, hum, acc, orie, all]

        for payload in dataArr:
            payload = json.dumps(payload)
            payload = json.loads(payload)
            print(payload)
            try:
                client.send(payload)
            except Exception as err:
                print("error occurred: {}".format(str(err)))
                raise
            time.sleep(1)


def handleGps():
    """
    Starts up the GPSPi runtime, begins listening for GPS Hat input,
    establishing a connection to a local CommPi via LAN, and sending data
    for transmission to the CommPi
    """
    gpsPi = GPSReader()
    client = WebClient()

    while True:
        print("gps loop")
        coords = gpsPi.get_geolocation()
        if coords is not None:
            payload = json.dumps(coords)
            try:
                client.ping_lan_server(payload)
            except Exception as err:
                print("Error transmitting gps data: {}".format(str(err)))
                raise
            time.sleep(1)


def handleLocal():
    """
    starts listening on the defined serial port and passing
    received data along to the web client when received
    """
    transceiver = Transceiver()
    url = os.environ.get("DJANGO_SERVER_API_ENDPOINT")
    if url:
        client = WebClient(server_url=url)
        while True:
            data = transceiver.listen()
            if data:
                print(data, type(data))
                payload = json.loads(data)
                client.send(payload)
    else:
        print("DJANGO_SERVER_API_ENDPOINT not set")


if __name__ == "__main__":  # pragma: no cover
    main()
