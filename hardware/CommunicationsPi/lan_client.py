import os
import time
import json
import requests
from requests.exceptions import HTTPError
from utils import get_logger

logging = get_logger("LAN_CLIENT_LOG_FILE")

url = os.environ["LAN_SERVER"]

logging.info('Pinging')
while True:
    try:
        payload = {
            'key1': 'value1',
            'key2': 'value2'
        }
        logging.info('data: ' + json.dumps(payload))
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except HTTPError as http_err:
        logging.error('HTTP error occurred: {}'.format(str(http_err)))
    except Exception as err:
        logging.error('error occurred: {}'.format(str(err)))
    else:
        time.sleep(1)
