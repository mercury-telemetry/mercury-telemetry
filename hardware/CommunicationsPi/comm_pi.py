import os
from http.server import BaseHTTPRequestHandler
from hardware.CommunicationsPi.web_client import WebClient
from hardware.CommunicationsPi.radio_transceiver import Transceiver
from hardware.Utils.utils import get_logger


class CommPi(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        if os.environ.get("ENABLE_RADIO_TRANSMISSION"):
            self.transceiver = Transceiver()

        if os.environ.get("ENABLE_INTERNET_TRANSMISSION"):
            apiUrl = os.environ.get("REMOTE_SERVER_API_ENDPOINT")
            self.web_client = WebClient(server_url=apiUrl)
        self.logging = get_logger("COMM_PI_LOG_FILE")
        super().__init__(*args, **kwargs)

    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.logging.info("GET request for {}".format(self.path).encode("utf-8"))
        self.wfile.write("GET request for {}".format(self.path).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        self.send_data(str(post_data.decode("utf-8")))
        self._set_response()
        self.logging.info("POST request for {}".format(self.path).encode("utf-8"))
        self.wfile.write("POST request for {}".format(self.path).encode("utf-8"))

    def send_data(self, payload):
        self.logging.info("send_data called, payload: " + str(payload))
        if os.environ.get("ENABLE_INTERNET_TRANSMISSION"):
            self.logging.info("transmit via internet")
            self.web_client.send(payload, is_json=True)
        if os.environ.get("ENABLE_RADIO_TRANSMISSION"):
            self.logging.info("transmit via radio")
            self.transceiver.send(payload)
        return
