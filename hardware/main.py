import os
import time
import json

from hardware.CommunicationsPi.radio_transceiver import Transceiver
from hardware.CommunicationsPi.comm_pi import CommPi
from hardware.CommunicationsPi.lan_server import runServer
from hardware.CommunicationsPi.lan_client import LANClient
from hardware.SensorPi.sense_pi import SensePi
from hardware.Utils.utils import get_sensor_keys
from hardware.gpsPi.gps_reader import GPSReader


if os.environ["HARDWARE_TYPE"] == "commPi":
    print("CommunicationsPi")
    runServer(handler_class=CommPi)
elif os.environ["HARDWARE_TYPE"] == "sensePi":
    print("SensePi")
    sensor_keys = get_sensor_keys()
    sensor_ids = {}
    sensor_ids[sensor_keys["TEMPERATURE"]] = 2
    sensor_ids[sensor_keys["PRESSURE"]] = 3
    sensor_ids[sensor_keys["HUMIDITY"]] = 4
    sensor_ids[sensor_keys["ACCELERATION"]] = 5
    sensor_ids[sensor_keys["ORIENTATION"]] = 6
    sensePi = SensePi(sensor_ids=sensor_ids)
    gpsPi = GPSReader()
    client = LANClient()

    while True:
        temp = sensePi.get_temperature()
        pres = sensePi.get_pressure()
        hum = sensePi.get_humidity()
        acc = sensePi.get_acceleration()
        orie = sensePi.get_orientation()
        all = sensePi.get_all()
        coords = gpsPi.get_geolocation()

        if coords is not None:
            data = [temp, pres, hum, acc, orie, coords, all]
        else:
            data = [temp, pres, hum, acc, orie, all]

        for i in data:
            payload = json.dumps(i)
            print(payload)
            try:
                client.ping_lan_server(payload)
            except Exception as err:
                print("error occurred: {}".format(str(err)))
                raise
            time.sleep(1)
else:
    print("Local Django Server")
    transceiver = Transceiver()
    url = os.environ.get('DJANGO_SERVER_API_ENDPOINT')
    if url:
        client = LANClient(lan_server_url=url)
        while True:
            data = transceiver.listen()
            if data:
                print(data)
                client.ping_lan_server(json.loads(data))
    else:
        print('DJANGO_SERVER_API_ENDPOINT not set')
