import os
import time

from dotenv import load_dotenv

PI_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_file = os.path.join(PI_DIR, "hardware/env")
if os.path.isfile(dotenv_file):  # pragma: no cover
    load_dotenv(dotenv_path=dotenv_file)
else:
    print("dotenv_file was not a file")

from hardware.CommunicationsPi.comm_pi import CommPi  # noqa: E402
from hardware.CommunicationsPi.lan_server import runServer  # noqa: E402
from hardware.CommunicationsPi.lan_client import LANClient  # noqa: E402
from hardware.SensorPi.sense_pi import SensePi  # noqa: E402
from hardware.gpsPi.gps_reader import GPSReader  # noqa: E402

if os.environ["PI_TYPE"] == "commPi":
    print("CommunicationsPi")
    runServer(handler_class=CommPi)
else:
    print("SensePi")
    sensePi = SensePi()
    gpsPi = GPSReader()
    client = LANClient()

    while True:
        print("while true")
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
