from django.test import SimpleTestCase
from testfixtures import TempDirectory

from unittest import mock
import os

# import serial
# import serial.tools.list_ports

from ..CommunicationsPi.radio_transceiver import Transceiver
from ..CommunicationsPi.logger import Logger


class TranscieverTests(SimpleTestCase):
    def setUp(self):
        self.temp_dir = TempDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    @mock.patch("serial.Serial")
    @mock.patch("serial.tools.list_ports.comports")
    def test_init_no_dir(self, mock_port_list, mock_serial):
        """
        Tests the __init__ function where no log dir is specified
        """

        mock_port_list.return_value = [
            {
                "vid": "vid",
                "pid": None,
                "manufacturer": None,
                "serial_number": None,
                "interface": None,
                "device": "usb",
            }
        ]

        # mock_serial = mock.Mock()

        with mock.patch.dict(
            os.environ,
            {
                "LOG_DIRECTORY": self.temp_dir.path,
                "TRANSMITTER_LOG_FILE": "logger.txt",
                "RADIO_TRANSMITTER_PORT": "",
            },
        ):
            transciever = Transceiver()

            self.assertTrue(transciever.logging is not None)
            self.assertTrue(transciever.logging.name == "TRANSMITTER_LOG_FILE")
            self.assertIsInstance(transciever.logging, Logger)

            self.assertTrue(transciever.port == "usb")
            self.assertIsNone(transciever.port_vid)
            self.assertIsNone(transciever.port_pid)
            self.assertIsNone(transciever.port_vendor)
            self.assertIsNone(transciever.port_intf)
            self.assertIsNone(transciever.port_serial_number)

    @mock.patch("serial.Serial")
    @mock.patch("serial.tools.list_ports.comports")
    def test_init_dir(self, mock_port_list, mock_serial):
        """
        Tests the __init__ function where log dir is specified
        """

        mock_port_list.return_value = [
            {
                "vid": "vid",
                "pid": None,
                "manufacturer": None,
                "serial_number": None,
                "interface": None,
                "device": "usb",
            }
        ]

        # mock_serial = mock.Mock()

        with mock.patch.dict(
            os.environ,
            {
                "LOG_DIRECTORY": self.temp_dir.path,
                "RADIO_TRANSMITTER_PORT": "",
                "LOG_FILE": "logger.txt",
            },
        ):
            transciever = Transceiver(log_file_name="LOG_FILE")

            self.assertTrue(transciever.logging is not None)
            self.assertTrue(transciever.logging.name == "LOG_FILE")
            self.assertIsInstance(transciever.logging, Logger)

            self.assertTrue(transciever.port == "usb")
            self.assertIsNone(transciever.port_vid)
            self.assertIsNone(transciever.port_pid)
            self.assertIsNone(transciever.port_vendor)
            self.assertIsNone(transciever.port_intf)
            self.assertIsNone(transciever.port_serial_number)
