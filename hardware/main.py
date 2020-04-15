import time
from hardware.CommunicationsPi.lan_client import LANClient
from hardware.SensorPi.sense_pi import SensePi

# This file shows the usage of SensePi and LANClient
sensePi = SensePi()
client = LANClient()

while True:
    print("iteration")
    temp = sensePi.get_temperature()
    pres = sensePi.get_pressure()
    hum = sensePi.get_humidity()
    acc = sensePi.get_acceleration()
    orie = sensePi.get_orientation()
    all = sensePi.get_all()

    data = [temp, pres, hum, acc, orie, all]
    for i in data:
        print(i)
        client.ping_lan_server(i)
    time.sleep(1)
