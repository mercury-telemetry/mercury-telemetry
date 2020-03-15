import os
import json
from logger import Logger

def get_serial_stream(s):
    return (json.dumps(s) + "\n").encode()

def get_logger(key):
    print(key, os.environ[key])
    logger = Logger(
            name=key,
            filename=os.environ[key]
            )
    return logger
