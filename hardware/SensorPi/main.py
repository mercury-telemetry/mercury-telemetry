from sense_hat import SenseHat
import requests
from sensehat_reader import temperature, pressure, humidity, acceleration, orientation

# import json

TEST_ENDPOINT = "http://pastebin.com/api/api_post.php"
API_ENDPOINT = "http://mecury-backend-prod.herokuapp.com/measurement/"

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

    response_temperature = requests.post(url=API_ENDPOINT, data=json_temperature)
    response_pressure = requests.post(url=API_ENDPOINT, data=json_pressure)
    response_humidity = requests.post(url=API_ENDPOINT, data=json_humidity)
    response_acceleration = requests.post(url=API_ENDPOINT, data=json_acceleration)
    response_orientation = requests.post(url=API_ENDPOINT, data=json_orientation)

    # print(response_temperature)
    # print(response_pressure)
    # print(response_humidity)
    # print(response_acceleration)
    # print(response_orientation)
    # print("")
