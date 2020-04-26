import os
import time

from hardware.CommunicationsPi.comm_pi import CommPi
from hardware.CommunicationsPi.lan_server import runServer
from hardware.CommunicationsPi.lan_client import LANClient
from hardware.gpsPi.gps_reader import GPSReader

gps = GPSReader()
client = LANClient(lan_server_url='https://kayak-123.herokuapp.com/measurement/')

while True:
    coords = gps.get_geolocation()

    data = [coords]
    for i in data:
        if i is not None:
            print(i)
            try:
                client.ping_lan_server(i)
            except Exception as err:
                print("error occurred: {}".format(str(err)))
                raise
            time.sleep(1)
