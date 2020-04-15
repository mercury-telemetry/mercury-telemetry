import os
from sense_hat import SenseHat
import requests
from sensehat_reader import temperature, pressure, humidity, acceleration, orientation
from datetime import datetime

# import json

TEST_ENDPOINT = "http://pastebin.com/api/api_post.php"
API_ENDPOINT = "http://mecury-backend-prod.herokuapp.com/measurement/"

sense = SenseHat()
nyu_purple = (87, 46, 140)
sense.show_message("MERCURY", text_colour=nyu_purple, scroll_speed=0.04)
sense.clear()

# initilaize time of last sent temperature
fmt = "%Y-%m-%d %H:%M:%S"
time_of_last_sent_temperature = datetime.now().strftime(fmt)
time_of_last_sent_pressure = datetime.now().strftime(fmt)
time_of_last_sent_humidity = datetime.now().strftime(fmt)
time_of_last_sent_acceleration = datetime.now().strftime(fmt)
time_of_last_sent_orientation = datetime.now().strftime(fmt)

datarate_temperature = os.environ["DATA_RATE_TEMPERATURE"]
datarate_pressure = os.environ["DATA_RATE_PRESSURE"]
datarate_humidity = os.environ["DATA_RATE_HUMIDITY"]
datarate_acceleration = os.environ["DATA_RATE_ACCELERATION"]
datarate_orientation = os.environ["DATA_RATE_ORIENTATION"]

while 1:
    json_temperature = temperature()
    json_pressure = pressure()
    json_humidity = humidity()
    json_acceleration = acceleration()
    json_orientation = orientation()

    # json_temperature  = json.dumps(temperature(sense))
    # json_pressure     = json.dumps(pressure(sense))
    # json_humidity     = json.dumps(humidity(sense))
    # json_acceleration = json.dumps(acceleration(sense))
    # json_orientation  = json.dumps(orientation(sense))

    # print(json_temperature)
    # print(json_pressure)
    # print(json_humidity)
    # print(json_acceleration)
    # print(json_orientation)

    tdelta = datetime.strptime(datetime.now().strftime(fmt), fmt) - datetime.strptime(
        time_of_last_sent_temperature, fmt
    )
    if (tdelta.seconds) / 60 >= datarate_temperature:
        print("Send Post request for Temperature")
        response_temperature = requests.post(url=API_ENDPOINT, data=json_temperature)
        time_of_last_sent_temperature = datetime.now().strftime(fmt)

    tdelta = datetime.strptime(datetime.now().strftime(fmt), fmt) - datetime.strptime(
        time_of_last_sent_pressure, fmt
    )
    if (tdelta.seconds) / 60 >= datarate_pressure:
        print("Send Post request for Pressure")
        response_pressure = requests.post(url=API_ENDPOINT, data=json_pressure)
        time_of_last_sent_pressure = datetime.now().strftime(fmt)

    tdelta = datetime.strptime(datetime.now().strftime(fmt), fmt) - datetime.strptime(
        time_of_last_sent_humidity, fmt
    )
    if (tdelta.seconds) / 60 >= datarate_humidity:
        print("Send Post request for Humidity")
        response_humidity = requests.post(url=API_ENDPOINT, data=json_humidity)
        time_of_last_sent_humidity = datetime.now().strftime(fmt)

    tdelta = datetime.strptime(datetime.now().strftime(fmt), fmt) - datetime.strptime(
        time_of_last_sent_acceleration, fmt
    )
    if (tdelta.seconds) / 60 >= datarate_acceleration:
        print("Send Post request for Acceleration")
        response_acceleration = requests.post(url=API_ENDPOINT, data=json_acceleration)
        time_of_last_sent_acceleration = datetime.now().strftime(fmt)

    tdelta = datetime.strptime(datetime.now().strftime(fmt), fmt) - datetime.strptime(
        time_of_last_sent_orientation, fmt
    )
    if (tdelta.seconds) / 60 >= datarate_orientation:
        print("Send Post request for Orientation")
        response_orientation = requests.post(url=API_ENDPOINT, data=json_orientation)
        time_of_last_sent_orientation = datetime.now().strftime(fmt)

    # print(response_temperature)
    # print(response_pressure)
    # print(response_humidity)
    # print(response_acceleration)
    # print(response_orientation)
    # print("")
