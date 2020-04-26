import requests
import os
from gps_reader import GPSReader

# import json

API_ENDPOINT = "https://kayak-123.herokuapp.com/measurement"

gps = GPSReader()

while 1:
    json_coordinates = gps.get_geolocation()
    print(json_coordinates)

    response_coordinates = requests.post(url=API_ENDPOINT, data=json_coordinates)
    print(response_coordinates)

