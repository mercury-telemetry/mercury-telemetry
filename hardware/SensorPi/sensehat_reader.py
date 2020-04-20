from sense_hat import SenseHat
import json
from utils import date_str_with_current_timezone


TEMPERATURE_ID = 6
PRESSURE_ID = 7
HUMIDITY_ID = 10
ACCELERATION_ID = 8
ORIENTATION_ID = 9


def temperature():
    sense = SenseHat()
    temperature = sense.get_temperature()
    date = date_str_with_current_timezone()
    data = {}
    data["sensor_id"] = TEMPERATURE_ID
    data["values"] = {"temperature": temperature}
    data["values"] = json.dumps(data["values"])
    data["date"] = date
    return data


def pressure():
    sense = SenseHat()
    pressure = sense.get_pressure()
    date = date_str_with_current_timezone()
    data = {}
    data["sensor_id"] = PRESSURE_ID
    data["values"] = {"pressure": pressure}
    data["values"] = json.dumps(data["values"])
    data["date"] = date
    return data


def humidity():
    sense = SenseHat()
    humidity = sense.get_humidity()
    date = date_str_with_current_timezone()
    data = {}
    data["sensor_id"] = HUMIDITY_ID
    data["values"] = {"humidity": humidity}
    data["values"] = json.dumps(data["values"])
    data["date"] = date
    return data


def acceleration():
    sense = SenseHat()
    acceleration = sense.get_accelerometer_raw()
    date = date_str_with_current_timezone()
    data = {}
    data["sensor_id"] = ACCELERATION_ID
    data["values"] = {
        "x": acceleration["x"],
        "y": acceleration["y"],
        "z": acceleration["z"],
    }
    data["values"] = json.dumps(data["values"])
    data["date"] = date
    return data


def orientation():
    sense = SenseHat()
    orientation = sense.get_orientation()
    date = date_str_with_current_timezone()
    data = {}
    data["sensor_id"] = ORIENTATION_ID
    data["values"] = {
        "roll": orientation["roll"],
        "pitch": orientation["pitch"],
        "yaw": orientation["yaw"],
    }
    data["values"] = json.dumps(data["values"])
    data["date"] = date
    return data
