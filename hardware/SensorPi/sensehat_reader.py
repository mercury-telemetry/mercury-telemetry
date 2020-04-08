from sense_hat import SenseHat
import json
from datetime import datetime


def temperature(sense):
    temperature = sense.get_temperature()
    date = str(datetime.now())
    data = {}
    data['id'] = 1
    data['values'] = {
        'temperature': temperature
        }
    data['date'] = date
    return data

def pressure(sense):
    pressure = sense.get_pressure()
    date = str(datetime.now())
    data = {}
    data['id'] = 2
    data['values'] = {
        'pressure': pressure
        }
    data['date'] = date
    return data

def humidity(sense):
    humidity = sense.get_humidity()
    date = str(datetime.now())
    data = {}
    data['id'] = 3
    data['values'] = {
        'humidity': humidity
        }
    data['date'] = date
    return data

def acceleration(sense):
    acceleration = sense.get_accelerometer_raw()
    date = str(datetime.now())
    data = {}
    data['id'] = 4
    data['values'] = {
        'x': acceleration['x'],
        'y': acceleration['y'],
        'z': acceleration['z'],
        }
    data['date'] = date
    return data

def orientation(sense):
    orientation = sense.get_orientation()
    date = str(datetime.now())
    data = {}
    data['id'] = 5
    data['values'] = {
        'roll': orientation['roll'],
        'pitch': orientation['pitch'],
        'yaw': orientation['yaw'],
        }
    data['date'] = date
    return data
    
    