import os
import time

from hardware.CommunicationsPi.comm_pi import CommPi
from hardware.CommunicationsPi.lan_server import runServer
from hardware.CommunicationsPi.lan_client import LANClient
from hardware.SensorPi.sense_pi import SensePi
from hardware.gpsPi.gps_reader import GPSReader

if os.environ["PI_TYPE"] == "commPi":
    print("CommunicationsPi")
    runServer(handler_class=CommPi)
else:
    print("SensePi")
    sensePi = SensePi()
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
            print(i)
            try:
                client.ping_lan_server(i)
            except Exception as err:
                print("error occurred: {}".format(str(err)))
                raise
            time.sleep(1)
