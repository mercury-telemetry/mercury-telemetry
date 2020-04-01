#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from utils import get_logger

log = get_logger("LAN_SERVER_LOG_FILE")


class Server(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        global log

        log.info(
            "GET request,\nPath: %s\nHeaders:\n%s\n"
            + str(self.path)
            + str(self.headers)
        )
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode("utf-8"))

    def do_POST(self):
        global log

        content_length = int(
            self.headers["Content-Length"]
        )  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        log.info(
            "POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n"
            + str(self.path)
            + str(self.headers)
            + post_data.decode("utf-8")
        )
        log.info("data: " + str(post_data))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode("utf-8"))


def run(server_class=HTTPServer, handler_class=Server, log_file_name=None, port=8080):

    global log

    if log_file_name is not None:
        log = get_logger(log_file_name)

    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    log.info("Starting httpd...\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    log.info("Stopping httpd...\n")
