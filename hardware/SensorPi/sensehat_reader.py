from sense_hat import SenseHat
import json
from datetime import datetime

TEMPERATURE_ID  = 1
PRESSURE_ID     = 2
HUMIDITY_ID     = 3
ACCELERATION_ID = 4
ORIENTATION_ID  = 5

def temperature(sense):
    temperature = sense.get_temperature()
    date = str(datetime.now())
    data = {}
    data['id'] = TEMPERATURE_ID
    data['values'] = {
        'temperature': temperature
        }
    data['date'] = date
    return data

def pressure(sense):
    pressure = sense.get_pressure()
    date = str(datetime.now())
    data = {}
    data['id'] = PRESSURE_ID
    data['values'] = {
        'pressure': pressure
        }
    data['date'] = date
    return data

def humidity(sense):
    humidity = sense.get_humidity()
    date = str(datetime.now())
    data = {}
    data['id'] = HUMIDITY_ID
    data['values'] = {
        'humidity': humidity
        }
    data['date'] = date
    return data

def acceleration(sense):
    acceleration = sense.get_accelerometer_raw()
    date = str(datetime.now())
    data = {}
    data['id'] = ACCELERATION_ID
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
    data['id'] = ORIENTATION_ID
    data['values'] = {
        'roll': orientation['roll'],
        'pitch': orientation['pitch'],
        'yaw': orientation['yaw'],
        }
    data['date'] = date
    return data
    
    