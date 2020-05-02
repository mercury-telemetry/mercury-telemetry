import os
import json
import requests
from requests.exceptions import HTTPError
from hardware.Utils.utils import get_logger


class WebClient:
    def __init__(self, log_file_name=None, server_url=None):
        if log_file_name is None:
            self.logging = get_logger("WEB_CLIENT_LOG_FILE")
        else:
            self.logging = get_logger(log_file_name, log_file_name)

        if server_url is None:
            self.url = self.get_server_url_from_env()
        else:
            self.url = server_url

    def get_server_url_from_env(self):
        protocol = "https" if os.environ.get("LAN_SERVER_HTTPS") else "http"
        ip = os.environ["LAN_SERVER_IP"]
        port = os.environ["LAN_PORT"]

        url = "{}://{}".format(protocol, ip)
        url += ":{}".format(port) if port else ""

        return url

    # Function to ping the LAN server
    # Accepts payload as a python dictionary or json object
    def send(self, payload, is_json=True):
        self.logging.info("Pinging", self.url)

        try:
            self.logging.info("data: " + str(payload))
            if is_json:
                response = requests.post(self.url, json=payload)
                response.raise_for_status()
                return response
            else:
                response = requests.post(self.url, data=payload)
                response.raise_for_status()
                return response

        except HTTPError as http_err:
            self.logging.error("HTTP error occurred: {}".format(str(http_err)))
            # re-raised so that it can be handled further up the call stack
            raise

        except Exception as err:
            self.logging.error("error occurred: {}".format(str(err)))
            raise
