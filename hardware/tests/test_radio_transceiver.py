from django.test import SimpleTestCase
from testfixtures import TempDirectory, LogCapture

from unittest.mock import patch, MagicMock
from serial.tools.list_ports_common import ListPortInfo

import os
import serial

from ..CommunicationsPi.radio_transceiver import Transceiver
from ..Utils.logger import Logger
from ..Utils.utils import get_serial_stream


class TransceiverTests(SimpleTestCase):
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

        port = ListPortInfo()
        port.vid = "vid"
        port.pid = None
        port.manufacturer = None
        port.serial_number = None
        port.interface = None
        port.device = "usb"

        mock_port_list.return_value = [port]

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

        port = ListPortInfo()
        port.vid = "vid"
        port.pid = None
        port.manufacturer = None
        port.serial_number = None
        port.interface = None
        port.device = "usb"

        mock_port_list.return_value = [port]

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

        port = ListPortInfo()
        port.vid = None
        port.pid = None
        port.manufacturer = None
        port.serial_number = None
        port.interface = None
        port.device = "usb"

        mock_port_list.return_value = [port]

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
    def test_is_serial_usb_vid_match(self, mock_port_list, mock_serial):
        """
        Tests the __init__ function where the port vid
        is not empty and matches the supplied port in RADIO_TRANSMITTER_PORT
        """

        port, port2 = ListPortInfo(), ListPortInfo()
        port.vid = "foo"
        port.pid = "bar"
        port.manufacturer = "Microsoft"
        port.serial_number = "456"
        port.interface = "usb"
        port.device = "usb"

        port2.vid = "foo2"
        port2.pid = "baz"
        port2.manufacturer = "Apple"
        port2.serial_number = "123"
        port2.interface = "bluetooth"
        port2.device = "usb"

        mock_port_list.return_value = [port, port2]

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
            self.assertTrue(transciever.port_vid == "foo")
            self.assertTrue(transciever.port_pid == "bar")
            self.assertTrue(transciever.port_vendor == "Microsoft")
            self.assertTrue(transciever.port_intf == "usb")
            self.assertTrue(transciever.port_serial_number == "456")

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
    def test_is_serial_usb_vid_no_match(self, mock_port_list, mock_serial):
        """
        Tests the __init__ function where the port vid
        is not empty and doesn't match the supplied port in RADIO_TRANSMITTER_PORT
        """

        port, port2 = ListPortInfo(), ListPortInfo()
        port.vid = "foo"
        port.pid = "bar"
        port.manufacturer = "Microsoft"
        port.serial_number = "456"
        port.interface = "usb"
        port.device = "usb"

        port2.vid = "foo2"
        port2.pid = "baz"
        port2.manufacturer = "Apple"
        port2.serial_number = "123"
        port2.interface = "bluetooth"
        port2.device = "usb2"

        mock_port_list.return_value = [port, port2]

        with patch.dict(
            os.environ,
            {
                "LOG_DIRECTORY": self.temp_dir.path,
                "RADIO_TRANSMITTER_PORT": "usb2",
                "LOG_FILE": "logger.txt",
            },
        ):
            transciever = Transceiver(log_file_name="LOG_FILE")

            self.assertTrue(transciever.logging is not None)
            self.assertTrue(transciever.logging.name == "LOG_FILE")
            self.assertIsInstance(transciever.logging, Logger)

            self.assertTrue(transciever.port == "usb2")
            self.assertTrue(transciever.port_vid == "foo2")
            self.assertTrue(transciever.port_pid == "baz")
            self.assertTrue(transciever.port_vendor == "Apple")
            self.assertTrue(transciever.port_intf == "bluetooth")
            self.assertTrue(transciever.port_serial_number == "123")

            mock_serial.assert_called_with(
                port="usb2",
                baudrate=self.baudrate,
                parity=self.parity,
                stopbits=self.stopbits,
                bytesize=self.bytesize,
                timeout=self.timeout,
            )

    @patch("serial.Serial")
    @patch("serial.tools.list_ports.comports")
    def test_is_serial_usb_pid_no_match(self, mock_port_list, mock_serial):
        """
        Tests the __init__ function where the port pid
        is not empty and doesn't match the supplied port in RADIO_TRANSMITTER_PORT
        """

        port, port2 = ListPortInfo(), ListPortInfo()
        port.vid = "foo"
        port.pid = "bar"
        port.manufacturer = "Microsoft"
        port.serial_number = "456"
        port.interface = "usb"
        port.device = "usb"

        port2.vid = "foo"
        port2.pid = "baz"
        port2.manufacturer = "Apple"
        port2.serial_number = "123"
        port2.interface = "bluetooth"
        port2.device = "usb2"

        mock_port_list.return_value = [port, port2]

        with patch.dict(
            os.environ,
            {
                "LOG_DIRECTORY": self.temp_dir.path,
                "RADIO_TRANSMITTER_PORT": "usb2",
                "LOG_FILE": "logger.txt",
            },
        ):
            transciever = Transceiver(log_file_name="LOG_FILE")

            self.assertTrue(transciever.logging is not None)
            self.assertTrue(transciever.logging.name == "LOG_FILE")
            self.assertIsInstance(transciever.logging, Logger)

            self.assertTrue(transciever.port == "usb2")
            self.assertTrue(transciever.port_vid == "foo")
            self.assertTrue(transciever.port_pid == "baz")
            self.assertTrue(transciever.port_vendor == "Apple")
            self.assertTrue(transciever.port_intf == "bluetooth")
            self.assertTrue(transciever.port_serial_number == "123")

            mock_serial.assert_called_with(
                port="usb2",
                baudrate=self.baudrate,
                parity=self.parity,
                stopbits=self.stopbits,
                bytesize=self.bytesize,
                timeout=self.timeout,
            )

    @patch("serial.Serial")
    @patch("serial.tools.list_ports.comports")
    def test_is_serial_usb_serial_no_match(self, mock_port_list, mock_serial):
        """
        Tests the __init__ function where the port serial_number
        is not empty and doesn't match the supplied port in RADIO_TRANSMITTER_PORT
        """

        port, port2 = ListPortInfo(), ListPortInfo()
        port.vid = "foo"
        port.pid = "bar"
        port.manufacturer = "Microsoft"
        port.serial_number = "456"
        port.interface = "usb"
        port.device = "usb"

        port2.vid = "foo"
        port2.pid = "bar"
        port2.manufacturer = "Microsoft"
        port2.serial_number = "123"
        port2.interface = "bluetooth"
        port2.device = "usb2"

        mock_port_list.return_value = [port, port2]

        with patch.dict(
            os.environ,
            {
                "LOG_DIRECTORY": self.temp_dir.path,
                "RADIO_TRANSMITTER_PORT": "usb2",
                "LOG_FILE": "logger.txt",
            },
        ):
            transciever = Transceiver(log_file_name="LOG_FILE")

            self.assertTrue(transciever.logging is not None)
            self.assertTrue(transciever.logging.name == "LOG_FILE")
            self.assertIsInstance(transciever.logging, Logger)

            self.assertTrue(transciever.port == "usb2")
            self.assertTrue(transciever.port_vid == "foo")
            self.assertTrue(transciever.port_pid == "bar")
            self.assertTrue(transciever.port_vendor == "Microsoft")
            self.assertTrue(transciever.port_intf == "bluetooth")
            self.assertTrue(transciever.port_serial_number == "123")

            mock_serial.assert_called_with(
                port="usb2",
                baudrate=self.baudrate,
                parity=self.parity,
                stopbits=self.stopbits,
                bytesize=self.bytesize,
                timeout=self.timeout,
            )

    @patch("serial.Serial")
    @patch("serial.tools.list_ports.comports")
    def test_is_serial_usb_manufacturer_match(self, mock_port_list, mock_serial):
        """
        Tests the __init__ function where the port manufacturer
        is not empty and doesn't match the supplied port in RADIO_TRANSMITTER_PORT
        """

        port, port2 = ListPortInfo(), ListPortInfo()
        port.vid = "foo"
        port.pid = "bar"
        port.manufacturer = "Microsoft"
        port.serial_number = "456"
        port.interface = "usb"
        port.device = "usb"

        port2.vid = "foo"
        port2.pid = "bar"
        port2.manufacturer = "Apple"
        port2.serial_number = "123"
        port2.interface = "bluetooth"
        port2.device = "usb2"

        mock_port_list.return_value = [port, port2]

        with patch.dict(
            os.environ,
            {
                "LOG_DIRECTORY": self.temp_dir.path,
                "RADIO_TRANSMITTER_PORT": "usb2",
                "LOG_FILE": "logger.txt",
            },
        ):
            transciever = Transceiver(log_file_name="LOG_FILE")

            self.assertTrue(transciever.logging is not None)
            self.assertTrue(transciever.logging.name == "LOG_FILE")
            self.assertIsInstance(transciever.logging, Logger)

            self.assertTrue(transciever.port == "usb2")
            self.assertTrue(transciever.port_vid == "foo")
            self.assertTrue(transciever.port_pid == "bar")
            self.assertTrue(transciever.port_vendor == "Apple")
            self.assertTrue(transciever.port_intf == "bluetooth")
            self.assertTrue(transciever.port_serial_number == "123")

            mock_serial.assert_called_with(
                port="usb2",
                baudrate=self.baudrate,
                parity=self.parity,
                stopbits=self.stopbits,
                bytesize=self.bytesize,
                timeout=self.timeout,
            )

    @patch("serial.Serial")
    @patch("serial.tools.list_ports.comports")
    def test_is_serial_usb_interface_match(self, mock_port_list, mock_serial):
        """
        Tests the __init__ function where the port interface
        is not empty and doesn't match the supplied port in RADIO_TRANSMITTER_PORT
        """

        port, port2 = ListPortInfo(), ListPortInfo()
        port.vid = "foo"
        port.pid = "bar"
        port.manufacturer = "Microsoft"
        port.serial_number = "456"
        port.interface = "usb"
        port.device = "usb"

        port2.vid = "foo"
        port2.pid = "bar"
        port2.manufacturer = "Microsoft"
        port2.serial_number = "456"
        port2.interface = "bluetooth"
        port2.device = "usb2"

        mock_port_list.return_value = [port, port2]

        with patch.dict(
            os.environ,
            {
                "LOG_DIRECTORY": self.temp_dir.path,
                "RADIO_TRANSMITTER_PORT": "usb2",
                "LOG_FILE": "logger.txt",
            },
        ):
            transciever = Transceiver(log_file_name="LOG_FILE")

            self.assertTrue(transciever.logging is not None)
            self.assertTrue(transciever.logging.name == "LOG_FILE")
            self.assertIsInstance(transciever.logging, Logger)

            self.assertTrue(transciever.port == "usb2")
            self.assertTrue(transciever.port_vid == "foo")
            self.assertTrue(transciever.port_pid == "bar")
            self.assertTrue(transciever.port_vendor == "Microsoft")
            self.assertTrue(transciever.port_intf == "bluetooth")
            self.assertTrue(transciever.port_serial_number == "456")

            mock_serial.assert_called_with(
                port="usb2",
                baudrate=self.baudrate,
                parity=self.parity,
                stopbits=self.stopbits,
                bytesize=self.bytesize,
                timeout=self.timeout,
            )

    @patch("serial.Serial")
    @patch("serial.tools.list_ports.comports")
    def test_send(self, mock_port_list, mock_serial):
        """
        tests the send method
        """
        port = ListPortInfo()
        port.vid = "vid"
        port.pid = "pid"
        port.manufacturer = "Microsoft"
        port.serial_number = "456"
        port.interface = "usb"
        port.device = "usb"

        mock_port_list.return_value = [port]

        test_payload = {"value": "value"}

        output = get_serial_stream(test_payload)

        with patch.dict(
            os.environ,
            {
                "LOG_DIRECTORY": self.temp_dir.path,
                "RADIO_TRANSMITTER_PORT": "usb",
                "LOG_FILE": "logger.txt",
            },
        ):
            with LogCapture() as capture:
                transciever = Transceiver(log_file_name="LOG_FILE")

                mock_serial_sender = MagicMock()
                transciever.serial = mock_serial_sender

                transciever.send(test_payload)
                mock_serial_sender.write.assert_called_with(output)
                capture.check(
                    ("LOG_FILE", "INFO", "Port device found: usb"),
                    ("LOG_FILE", "INFO", "Opening serial on: usb"),
                    ("LOG_FILE", "INFO", "sending"),
                    ("LOG_FILE", "INFO", "{'value': 'value'}"),
                )

    @patch("serial.Serial")
    @patch("serial.tools.list_ports.comports")
    def test_listen_valid(self, mock_port_list, mock_serial):
        """
        tests the listen method
        """
        port = ListPortInfo()
        port.vid = "vid"
        port.pid = "pid"
        port.manufacturer = "Microsoft"
        port.serial_number = "456"
        port.interface = "usb"
        port.device = "usb"

        mock_port_list.return_value = [port]

        test_input = '{"value": "value"}'

        with patch.dict(
            os.environ,
            {
                "LOG_DIRECTORY": self.temp_dir.path,
                "RADIO_TRANSMITTER_PORT": "usb",
                "LOG_FILE": "logger.txt",
            },
        ):
            with LogCapture() as capture:
                transceiver = Transceiver(log_file_name="LOG_FILE")

                mock_receiver = MagicMock()
                mock_receiver.readline.return_value.decode.return_value = test_input
                transceiver.serial = mock_receiver

                transceiver.listen()
                capture.check(
                    ("LOG_FILE", "INFO", "Port device found: usb"),
                    ("LOG_FILE", "INFO", "Opening serial on: usb"),
                    ("LOG_FILE", "INFO", "{'value': 'value'}"),
                )

    @patch("serial.Serial")
    @patch("serial.tools.list_ports.comports")
    def test_listen_invalid(self, mock_port_list, mock_serial):
        """
        tests the listen method with invalid input
        """
        port = ListPortInfo()
        port.vid = "vid"
        port.pid = "pid"
        port.manufacturer = "Microsoft"
        port.serial_number = "456"
        port.interface = "usb"
        port.device = "usb"

        mock_port_list.return_value = [port]

        test_input = "{'value': 'value'}"
        with patch.dict(
            os.environ,
            {
                "LOG_DIRECTORY": self.temp_dir.path,
                "RADIO_TRANSMITTER_PORT": "usb",
                "LOG_FILE": "logger.txt",
            },
        ):
            with LogCapture() as capture:
                transceiver = Transceiver(log_file_name="LOG_FILE")

                mock_receiver = MagicMock()
                mock_receiver.readline.return_value.decode.return_value = test_input
                transceiver.serial = mock_receiver

                transceiver.listen()
                capture.check(
                    ("LOG_FILE", "INFO", "Port device found: usb"),
                    ("LOG_FILE", "INFO", "Opening serial on: usb"),
                    ("LOG_FILE", "ERROR", "<class 'json.decoder.JSONDecodeError'>"),
                )
