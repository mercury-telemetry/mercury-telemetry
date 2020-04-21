from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock
from testfixtures import TempDirectory, LogCapture
from requests.exceptions import HTTPError

import os
import json

from hardware.CommunicationsPi.lan_client import LANClient
from hardware.Utils.logger import Logger


class LanClientTests(SimpleTestCase):
    def setUp(self):
        self.temp_dir = TempDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_init_no_log_no_server(self):
        with patch.dict(
            os.environ,
            {
                "LAN_CLIENT_LOG_FILE": "lan_client.log",
                "LOG_DIRECTORY": self.temp_dir.path,
                "LAN_SERVER_HTTPS": "True",
                "LAN_SERVER_IP": "0.0.0.0",
                "LAN_PORT": "0",
            },
        ):
            l_client = LANClient()

            self.assertTrue(l_client.logging is not None)
            self.assertTrue(l_client.logging.name == "LAN_CLIENT_LOG_FILE")
            self.assertIsInstance(l_client.logging, Logger)

            self.assertEqual(l_client.url, "https://0.0.0.0:0")

    def test_init_no_log_no_server_http(self):
        with patch.dict(
            os.environ,
            {
                "LAN_CLIENT_LOG_FILE": "lan_client.log",
                "LOG_DIRECTORY": self.temp_dir.path,
                "LAN_SERVER_IP": "0.0.0.0",
                "LAN_PORT": "0",
            },
        ):
            l_client = LANClient()

            self.assertTrue(l_client.logging is not None)
            self.assertTrue(l_client.logging.name == "LAN_CLIENT_LOG_FILE")
            self.assertIsInstance(l_client.logging, Logger)

            self.assertEqual(l_client.url, "http://0.0.0.0:0")

    def test_init_no_log_server(self):
        with patch.dict(
            os.environ,
            {
                "LAN_CLIENT_LOG_FILE": "lan_client.log",
                "LOG_DIRECTORY": self.temp_dir.path,
                "LAN_SERVER_HTTPS": "True",
                "LAN_SERVER_IP": "0.0.0.0",
                "LAN_PORT": "0",
            },
        ):
            l_client = LANClient(lan_server_url="/url")

            self.assertTrue(l_client.logging is not None)
            self.assertTrue(l_client.logging.name == "LAN_CLIENT_LOG_FILE")
            self.assertIsInstance(l_client.logging, Logger)

            self.assertEqual(l_client.url, "/url")

    def test_init_log_no_server(self):
        with patch.dict(
            os.environ,
            {
                "NEW_LOG_FILE": "lan_client.log",
                "LOG_DIRECTORY": self.temp_dir.path,
                "LAN_SERVER_HTTPS": "True",
                "LAN_SERVER_IP": "0.0.0.0",
                "LAN_PORT": "0",
            },
        ):
            l_client = LANClient(log_file_name="NEW_LOG_FILE")

            self.assertTrue(l_client.logging is not None)
            self.assertTrue(l_client.logging.name == "NEW_LOG_FILE")
            self.assertIsInstance(l_client.logging, Logger)

            self.assertEqual(l_client.url, "https://0.0.0.0:0")

    def test_init_log_server(self):
        with patch.dict(
            os.environ,
            {
                "NEW_LOG_FILE": "lan_client.log",
                "LOG_DIRECTORY": self.temp_dir.path,
                "LAN_SERVER_HTTPS": "True",
                "LAN_SERVER_IP": "0.0.0.0",
                "LAN_PORT": "0",
            },
        ):
            l_client = LANClient(log_file_name="NEW_LOG_FILE", lan_server_url="/url")

            self.assertTrue(l_client.logging is not None)
            self.assertTrue(l_client.logging.name == "NEW_LOG_FILE")
            self.assertIsInstance(l_client.logging, Logger)

            self.assertEqual(l_client.url, "/url")

    @patch("hardware.CommunicationsPi.lan_client.requests")
    def test_ping_server(self, mock_requests=MagicMock()):
        with patch.dict(
            os.environ,
            {
                "LAN_CLIENT_LOG_FILE": "lan_client.log",
                "LOG_DIRECTORY": self.temp_dir.path,
                "LAN_SERVER_HTTPS": "True",
                "LAN_SERVER_IP": "0.0.0.0",
                "LAN_PORT": "0",
            },
        ):
            with LogCapture() as capture:
                l_client = LANClient()

                payload = "{'key':'value'}"

                l_client.ping_lan_server(payload)

                mock_requests.post.assert_called_with("https://0.0.0.0:0", data=payload)
                capture.check(
                    ("LAN_CLIENT_LOG_FILE", "INFO", "Pinging"),
                    ("LAN_CLIENT_LOG_FILE", "INFO", f"data: {json.dumps(payload)}"),
                )

    @patch("hardware.CommunicationsPi.lan_client.requests")
    def test_ping_server_raise_http_ex(self, mock_requests=MagicMock()):
        with patch.dict(
            os.environ,
            {
                "LAN_CLIENT_LOG_FILE": "lan_client.log",
                "LOG_DIRECTORY": self.temp_dir.path,
                "LAN_SERVER_HTTPS": "True",
                "LAN_SERVER_IP": "0.0.0.0",
                "LAN_PORT": "0",
            },
        ):
            with LogCapture() as capture:
                l_client = LANClient()
                mock_requests.post.side_effect = HTTPError("HTTPError")

                payload = "{'key':'value'}"

                with self.assertRaises(HTTPError):
                    l_client.ping_lan_server(payload)

                mock_requests.post.assert_called_with("https://0.0.0.0:0", data=payload)
                capture.check(
                    ("LAN_CLIENT_LOG_FILE", "INFO", "Pinging"),
                    ("LAN_CLIENT_LOG_FILE", "INFO", f"data: {json.dumps(payload)}"),
                    ("LAN_CLIENT_LOG_FILE", "ERROR", "HTTP error occurred: HTTPError"),
                )

    @patch("hardware.CommunicationsPi.lan_client.requests")
    def test_ping_server_raise_ex(self, mock_requests=MagicMock()):
        with patch.dict(
            os.environ,
            {
                "LAN_CLIENT_LOG_FILE": "lan_client.log",
                "LOG_DIRECTORY": self.temp_dir.path,
                "LAN_SERVER_HTTPS": "True",
                "LAN_SERVER_IP": "0.0.0.0",
                "LAN_PORT": "0",
            },
        ):
            with LogCapture() as capture:
                l_client = LANClient()
                mock_requests.post.side_effect = Exception("Exception")

                payload = "{'key':'value'}"

                with self.assertRaises(Exception):
                    l_client.ping_lan_server(payload)

                mock_requests.post.assert_called_with("https://0.0.0.0:0", data=payload)
                capture.check(
                    ("LAN_CLIENT_LOG_FILE", "INFO", "Pinging"),
                    ("LAN_CLIENT_LOG_FILE", "INFO", f"data: {json.dumps(payload)}"),
                    ("LAN_CLIENT_LOG_FILE", "ERROR", "error occurred: Exception"),
                )
