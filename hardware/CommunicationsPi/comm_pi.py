import os
import json
from http.server import BaseHTTPRequestHandler
from hardware.CommunicationsPi.radio_transceiver import Transceiver


class CommPi(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.transceiver = Transceiver()
        super().__init__(*args, **kwargs)

    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        self.send_data(str(post_data.decode("utf-8")))
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode("utf-8"))

    def send_data(self, payload):
        if os.environ.get('ENABLE_INTERNET_TRANSMISSION'):
            print('transmit via internet')
        if os.environ.get('ENABLE_RADIO_TRANSMISSION'):
            print('transmit via radio')
            self.transceiver.send(payload)
        return
