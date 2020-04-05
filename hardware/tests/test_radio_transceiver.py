from django.test import SimpleTestCase
from testfixtures import TempDirectory

from unittest.mock import patch

import os
import serial

from ..CommunicationsPi.radio_transceiver import Transceiver
from ..CommunicationsPi.logger import Logger


class TranscieverTests(SimpleTestCase):
    def setUp(self):
        self.temp_dir = TempDirectory()

        self.baudrate = 9600
        self.parity = serial.PARITY_NONE
        self.stopbits = serial.STOPBITS_ONE
        self.bytesize = serial.EIGHTBITS
        self.timeout = 1

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("serial.Serial")
    @patch("serial.tools.list_ports.comports")
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

        with patch.dict(
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

            mock_serial.assert_called_with(
                port="usb",
                baudrate=self.baudrate,
                parity=self.parity,
                stopbits=self.stopbits,
                bytesize=self.bytesize,
                timeout=self.timeout,
            )

    @patch("serial.Serial")
    @patch("serial.tools.list_ports.comports")
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

        with patch.dict(
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

            mock_serial.assert_called_with(
                port="usb",
                baudrate=self.baudrate,
                parity=self.parity,
                stopbits=self.stopbits,
                bytesize=self.bytesize,
                timeout=self.timeout,
            )

    @patch("serial.Serial")
    @patch("serial.tools.list_ports.comports")
    def test_init_no_usb(self, mock_port_list, mock_serial):
        """
        Tests the __init__ function where the serial port list
        is empty
        """

        mock_port_list.return_value = []

        with patch.dict(
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

            self.assertTrue(transciever.port == "")
            self.assertIsNone(transciever.port_vid)
            self.assertIsNone(transciever.port_pid)
            self.assertIsNone(transciever.port_vendor)
            self.assertIsNone(transciever.port_intf)
            self.assertIsNone(transciever.port_serial_number)

            mock_serial.assert_called_with(
                port="",
                baudrate=self.baudrate,
                parity=self.parity,
                stopbits=self.stopbits,
                bytesize=self.bytesize,
                timeout=self.timeout,
            )

    @patch("serial.Serial")
    @patch("serial.tools.list_ports.comports")
    def test_is_serial_usb_no_vid(self, mock_port_list, mock_serial):
        """
        Tests the __init__ function where the port vid
        is empty
        """

        mock_port_list.return_value = [{"port": None}]

        with patch.dict(
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

            self.assertTrue(transciever.port == "")
            self.assertIsNone(transciever.port_vid)
            self.assertIsNone(transciever.port_pid)
            self.assertIsNone(transciever.port_vendor)
            self.assertIsNone(transciever.port_intf)
            self.assertIsNone(transciever.port_serial_number)

            mock_serial.assert_called_with(
                port="",
                baudrate=self.baudrate,
                parity=self.parity,
                stopbits=self.stopbits,
                bytesize=self.bytesize,
                timeout=self.timeout,
            )

    @patch("serial.Serial")
    @patch("serial.tools.list_ports.comports")
    def test_is_serial_usb_vid_no_match(self, mock_port_list, mock_serial):
        """
        Tests the __init__ function where the port vid
        is not empty but does not match
        """

        mock_port_list.return_value = [{"port": None}]

        with patch.dict(
            os.environ,
            {
                "LOG_DIRECTORY": self.temp_dir.path,
                "RADIO_TRANSMITTER_PORT": "usb",
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

            mock_serial.assert_called_with(
                port="usb",
                baudrate=self.baudrate,
                parity=self.parity,
                stopbits=self.stopbits,
                bytesize=self.bytesize,
                timeout=self.timeout,
            )
