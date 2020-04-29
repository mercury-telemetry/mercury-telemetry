import os
from http.server import BaseHTTPRequestHandler
from hardware.CommunicationsPi.web_client import WebClient
from hardware.CommunicationsPi.radio_transceiver import Transceiver


class CommPi(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.transceiver = Transceiver()

        apiUrl = os.environ.get("REMOTE_SERVER_API_ENDPOINT")
        self.web_client = WebClient(server_url=apiUrl)
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
        if os.environ.get("ENABLE_INTERNET_TRANSMISSION"):
            print("transmit via internet")
            self.web_client.send(payload)
        if os.environ.get("ENABLE_RADIO_TRANSMISSION"):
            print("transmit via radio")
            self.transceiver.send(payload)
        return
