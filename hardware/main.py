import os
import time

from hardware.CommunicationsPi.comm_pi import CommPi
from hardware.CommunicationsPi.lan_server import runServer
from hardware.CommunicationsPi.lan_client import LANClient
from hardware.SensorPi.sense_pi import SensePi
from hardware.Utils.utils import (
        get_sensor_keys,
)


if os.environ["PI_TYPE"] == "commPi":
    print("CommunicationsPi")
    runServer(handler_class=CommPi)
else:
    print("SensePi")
    sensor_keys = get_sensor_keys()
    sensor_ids = {}
    sensor_ids[sensor_keys["TEMPERATURE"]] = 2
    sensor_ids[sensor_keys["PRESSURE"]] = 3
    sensor_ids[sensor_keys["HUMIDITY"]] = 4
    sensor_ids[sensor_keys["ACCELERATION"]] = 5
    sensor_ids[sensor_keys["ORIENTATION"]] = 6
    sensePi = SensePi(sensor_ids=sensor_ids)
    client = LANClient()

    while True:
        temp = sensePi.get_temperature()
        pres = sensePi.get_pressure()
        hum = sensePi.get_humidity()
        acc = sensePi.get_acceleration()
        orie = sensePi.get_orientation()
        all = sensePi.get_all()

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
