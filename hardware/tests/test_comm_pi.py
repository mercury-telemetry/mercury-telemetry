from django.test import SimpleTestCase
import os

# from json.decoder import JSONDecodeError
from http.server import HTTPServer

from unittest import mock
from unittest.mock import patch

import threading
import socket
import requests

from hardware.CommunicationsPi.comm_pi import CommPi


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(("localhost", 0))
    address, port = s.getsockname()
    s.close()
    return address, port


class CommPiTests(SimpleTestCase):
    def setUp(self):
        self.mock_server_url, self.mock_server_port = get_free_port()
        self.mock_server = HTTPServer(
            (self.mock_server_url, self.mock_server_port), CommPi
        )
        self.mock_server_thread = threading.Thread(
            target=self.mock_server.serve_forever
        )
        self.mock_server_thread.setDaemon(True)
        self.mock_server_thread.start()

    @mock.patch("hardware.CommunicationsPi.comm_pi.WebClient")
    @mock.patch("hardware.CommunicationsPi.comm_pi.Transceiver")
    def test_get(self, mock_transceiver=mock.MagicMock(), mock_client=mock.MagicMock()):
        with patch.dict(
            os.environ, {"COMM_PI_LOG_FILE": "comm.log", "LOG_DIRECTORY": "logs"}
        ):
            url = f"http://{self.mock_server_url}:{self.mock_server_port}/"
            response = requests.get(url)

            self.assertTrue(response.ok)
            self.assertTrue(response.headers.get("Content-Type") == "text/html")

    @mock.patch("hardware.CommunicationsPi.comm_pi.WebClient")
    @mock.patch("hardware.CommunicationsPi.comm_pi.Transceiver")
    def test_post_radio(
        self, mock_transceiver=mock.MagicMock(), mock_client=mock.MagicMock()
    ):
        with patch.dict(
            os.environ,
            {
                "ENABLE_RADIO_TRANSMISSION": "True",
                "COMM_PI_LOG_FILE": "comm.log",
                "LOG_DIRECTORY": "logs",
            },
        ):
            mock_transceiver.return_value.send = mock.MagicMock()
            mock_client.return_value.send = mock.MagicMock()
            url = f"http://{self.mock_server_url}:{self.mock_server_port}/"
            requests.post(url, data={"key": "value"}, headers={"Content-Length": "15"})
            mock_transceiver.return_value.send.assert_called()

    @mock.patch("hardware.CommunicationsPi.comm_pi.WebClient")
    @mock.patch("hardware.CommunicationsPi.comm_pi.Transceiver")
    def test_post_radio_with_internet(
        self, mock_transceiver=mock.MagicMock(), mock_client=mock.MagicMock(),
    ):
        with patch.dict(
            os.environ,
            {
                "ENABLE_INTERNET_TRANSMISSION": "True",
                "COMM_PI_LOG_FILE": "comm.log",
                "LOG_DIRECTORY": "logs",
            },
        ):
            mock_transceiver.return_value.send = mock.MagicMock()
            mock_client.return_value.send = mock.MagicMock()
            url = f"http://{self.mock_server_url}:{self.mock_server_port}/"
            requests.post(url, data={"key": "value"}, headers={"Content-Length": "15"})
            mock_transceiver.return_value.send.assert_not_called()
            mock_client.return_value.send.assert_called_with("key=value", is_json=True)
