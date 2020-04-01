import os
import json
from .logger import Logger


def get_serial_stream(s):
    return (json.dumps(s) + "\n").encode()


def get_logger(key, file_name=None):
    if file_name is None:
        file_name = key
    logger = Logger(name=key, filename=os.environ[file_name])
    return logger
