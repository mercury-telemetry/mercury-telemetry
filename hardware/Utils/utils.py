import os
import json
from .logger import Logger

SENSOR_KEYS = {
        'ALL': 'all',
        'TEMPERATURE': 'temperature',
        'PRESSURE': 'pressure',
        'HUMIDITY': 'humidity',
        'ACCELERATION': 'acceleration',
        'ORIENTATION': 'orientation'
        }

def get_sensor_keys():
    return SENSOR_KEYS

def get_serial_stream(s):
    return (json.dumps(s) + "\n").encode()


def get_logger(key, file_name=None):
    if file_name is None:
        file_name = key
    logger = Logger(name=key, filename=os.environ[file_name])
    return logger
