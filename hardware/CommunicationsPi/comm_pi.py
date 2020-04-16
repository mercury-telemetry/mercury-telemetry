from http.server import BaseHTTPRequestHandler, HTTPServer
from hardware.CommunicationsPi.radio_transceiver import Transceiver

transceiver = Transceiver()

class CommPi(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode("utf-8"))

    def do_POST(self):
        content_length = int(
                self.headers["Content-Length"]
                )
        post_data = self.rfile.read(content_length)

        self.send_data(str(post_data.decode("utf-8")))
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode("utf-8"))

    def send_data(self, payload):
        transceiver.send(payload)
        return
