from sense_hat import SenseHat
import requests
import os
from sensehat_reader import temperature, pressure, humidity, acceleration, orientation

# import json

TEST_ENDPOINT = os.environ["TEST_ENDPOINT"]
API_ENDPOINT = os.environ["API_ENDPOINT"]

sense = SenseHat()
nyu_purple = (87, 46, 140)
sense.show_message("MERCURY", text_colour=nyu_purple, scroll_speed=0.04)
sense.clear()

while 1:
    json_temperature = temperature()
    json_pressure = pressure()
    json_humidity = humidity()
    json_acceleration = acceleration()
    json_orientation = orientation()

    response_temperature = requests.post(url=API_ENDPOINT, data=json_temperature)
    response_pressure = requests.post(url=API_ENDPOINT, data=json_pressure)
    response_humidity = requests.post(url=API_ENDPOINT, data=json_humidity)
    response_acceleration = requests.post(url=API_ENDPOINT, data=json_acceleration)
    response_orientation = requests.post(url=API_ENDPOINT, data=json_orientation)
