from django.test import SimpleTestCase
from http.server import HTTPServer
from testfixtures import LogCapture, TempDirectory

from unittest import mock

import threading
import socket
import requests
import os

from hardware.CommunicationsPi.lan_server import Server, runServer


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(("localhost", 0))
    address, port = s.getsockname()
    s.close()
    return port


class LanServerTests(SimpleTestCase):
    def setUp(self):
        self.temp_dir = TempDirectory()
        self.mock_server_port = get_free_port()
        self.mock_server = HTTPServer(("localhost", self.mock_server_port), Server)

        self.mock_server_thread = threading.Thread(
            target=self.mock_server.serve_forever
        )
        self.mock_server_thread.setDaemon(True)
        self.mock_server_thread.start()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_get(self, mock_transceiver=mock.MagicMock()):
        with mock.patch.dict(
            os.environ,
            {"LAN_SERVER_LOG_FILE": "logger.txt", "LOG_DIRECTORY": self.temp_dir.path},
        ):
            with LogCapture() as capture:
                url = f"http://localhost:{self.mock_server_port}/"
                response = requests.get(url)

                self.assertTrue(response.ok)
                self.assertTrue(response.headers.get("Content-Type") == "text/html")

                capture.check(
                    (
                        "urllib3.connectionpool",
                        "DEBUG",
                        f"Starting new HTTP connection (1): localhost:{self.mock_server_port}",
                    ),
                    (
                        "LAN_SERVER_LOG_FILE",
                        "INFO",
                        "GET request,\n"
                        "Path: %s\n"
                        "Headers:\n"
                        "%s\n"
                        f"/Host: localhost:{self.mock_server_port}\n"
                        "User-Agent: python-requests/2.23.0\n"
                        "Accept-Encoding: gzip, deflate\n"
                        "Accept: */*\n"
                        "Connection: keep-alive\n"
                        "\n",
                    ),
                    (
                        "urllib3.connectionpool",
                        "DEBUG",
                        f'http://localhost:{self.mock_server_port} "GET / HTTP/1.1" 200 None',
                    ),
                )

    def test_post(self, mock_transceiver=mock.MagicMock()):
        with mock.patch.dict(
            os.environ,
            {"LAN_SERVER_LOG_FILE": "logger.txt", "LOG_DIRECTORY": self.temp_dir.path},
        ):
            with LogCapture() as capture:
                url = f"http://localhost:{self.mock_server_port}/"
                response = requests.post(
                    url, data={"key": "value"}, headers={"Content-Length": "15"}
                )

                self.assertTrue(response.ok)
                self.assertTrue(response.headers.get("Content-Type") == "text/html")

                capture.check(
                    (
                        "urllib3.connectionpool",
                        "DEBUG",
                        f"Starting new HTTP connection (1): localhost:{self.mock_server_port}",
                    ),
                    (
                        "LAN_SERVER_LOG_FILE",
                        "INFO",
                        "POST request,\n"
                        "Path: %s\n"
                        "Headers:\n"
                        "%s\n"
                        "\n"
                        "Body:\n"
                        "%s\n"
                        f"/Host: localhost:{self.mock_server_port}\n"
                        "User-Agent: python-requests/2.23.0\n"
                        "Accept-Encoding: gzip, deflate\n"
                        "Accept: */*\n"
                        "Connection: keep-alive\n"
                        "Content-Length: 9\n"
                        "Content-Type: application/x-www-form-urlencoded\n"
                        "\n"
                        "key=value",
                    ),
                    ("LAN_SERVER_LOG_FILE", "INFO", "data: b'key=value'"),
                    (
                        "urllib3.connectionpool",
                        "DEBUG",
                        f'http://localhost:{self.mock_server_port} "POST / HTTP/1.1" 200 None',
                    ),
                )


class RunServerTests(SimpleTestCase):
    def setUp(self):
        self.temp_dir = TempDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_run_server(self):
        with mock.patch.dict(
            os.environ,
            {
                "LAN_SERVER_LOG_FILE": "logger.txt",
                "LOG_DIRECTORY": self.temp_dir.path,
                "LAN_PORT": "0000",
            },
        ):
            with LogCapture() as capture:
                mock_server = mock.MagicMock()
                mock_server.return_value.server_forever = mock.MagicMock()
                mock_handler = mock.MagicMock()

                runServer(mock_server, mock_handler)

                capture.check(
                    ("LAN_SERVER_LOG_FILE", "INFO", "Starting server on port: 0"),
                    ("LAN_SERVER_LOG_FILE", "INFO", "Stopping\n"),
                )


#     def test_interrupt(self):
#         with mock.patch.dict(os.environ, {
#             "LAN_SERVER_LOG_FILE": "logger.txt",
#             "LOG_DIRECTORY": self.temp_dir.path,
#             "LAN_PORT": "0000"
#         }):
#             with LogCapture() as capture:
#                 mock_server = mock.MagicMock()
#                 mock_server.return_value.server_forever.side_effect = KeyboardInterrupt
#                 mock_handler = mock.MagicMock()

#                 with self.assertRaises(KeyboardInterrupt):
#                     runServer(mock_server, mock_handler)

#                 capture.check(('LAN_SERVER_LOG_FILE', 'INFO', 'Starting server on port: 0'),
#  ('LAN_SERVER_LOG_FILE', 'INFO', 'Stopping\n'))
