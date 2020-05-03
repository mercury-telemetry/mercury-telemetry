from django.test import SimpleTestCase
from unittest.mock import patch
from testfixtures import TempDirectory

import os

from hardware.Utils.logger import Logger
from hardware.gpsPi.gps_reader import GPSReader


@patch("serial.Serial")
class GPSPiTests(SimpleTestCase):
    def setUp(self):
        self.temp_dir = TempDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_init_no_logs(self, mock_port):

        # Replace real object os.environ with mock dictionary
        with patch.dict(
            os.environ,
            {
                "GPS_LOG_FILE": "logger.txt",
                "LOG_DIRECTORY": self.temp_dir.path,
                "GPS_PORT": "/dev/serial0",
                "GPS_BAUDRATE": "9600",
            },
        ):
            gps_reader = GPSReader()
            mock_port.assert_called_with(
                os.environ["GPS_PORT"], os.environ["GPS_BAUDRATE"],
            )

            self.assertTrue(gps_reader.logging is not None)
            self.assertTrue(gps_reader.logging.name == "GPS_LOG_FILE")
            self.assertIsInstance(gps_reader.logging, Logger)

    def test_init_logs(self, mock_port):

        with patch.dict(
            os.environ,
            {
                "GPS_HAT_LOG_FILE": "logger.txt",
                "LOG_DIRECTORY": self.temp_dir.path,
                "GPS_PORT": "/dev/serial0",
                "GPS_BAUDRATE": "9600",
            },
        ):

            gps_reader = GPSReader("GPS_HAT_LOG_FILE")
            mock_port.assert_called_with(
                os.environ["GPS_PORT"], os.environ["GPS_BAUDRATE"],
            )

            self.assertTrue(gps_reader.logging is not None)
            self.assertTrue(gps_reader.logging.name == "GPS_HAT_LOG_FILE")
            self.assertIsInstance(gps_reader.logging, Logger)

    @patch("hardware.gpsPi.gps_reader.date_str_with_current_timezone")
    def test_get_location_valid_data(self, mock_date, mock_port):

        mock_port.return_value.inWaiting.return_value = 1
        mock_port.return_value.readline.return_value = (
            "b'$GPRMC,194509.000,A,4042.6142,N,07400.4168,W,2.03,221.11,160412,,,A*77"
        )
        mock_date.return_value = "example date"

        with patch.dict(
            os.environ,
            {
                "GPS_LOG_FILE": "logger.txt",
                "LOG_DIRECTORY": self.temp_dir.path,
                "GPS_PORT": "/dev/serial0",
                "GPS_BAUDRATE": "9600",
            },
        ):

            expected_data = {}
            expected_data["sensor_id"] = 1
            expected_data["values"] = {
                "latitude": 40.71023666666667,
                "longitude": -74.00694666666666,
            }
            expected_data["date"] = "example date"

            gps_reader = GPSReader()
            data = gps_reader.get_geolocation()

            mock_port.return_value.inWaiting.assert_called()
            mock_port.return_value.readline.assert_called()

            self.assertEqual(expected_data, data)

    @patch("hardware.gpsPi.gps_reader.date_str_with_current_timezone")
    def test_get_location_other_valid_data(self, mock_date, mock_port):

        mock_port.return_value.inWaiting.return_value = 1
        mock_port.return_value.readline.return_value = (
            "b'$GPRMC,194509.000,A,4042.6142,S,07400.4168,W,2.03,221.11,160412,,,A*77"
        )
        mock_date.return_value = "example date"

        with patch.dict(
            os.environ,
            {
                "GPS_LOG_FILE": "logger.txt",
                "LOG_DIRECTORY": self.temp_dir.path,
                "GPS_PORT": "/dev/serial0",
                "GPS_BAUDRATE": "9600",
            },
        ):

            expected_data = {}
            expected_data["sensor_id"] = 1
            expected_data["values"] = {
                "latitude": -40.71023666666667,
                "longitude": -74.00694666666666,
            }
            expected_data["date"] = "example date"

            gps_reader = GPSReader()
            data = gps_reader.get_geolocation()

            mock_port.return_value.inWaiting.assert_called()
            mock_port.return_value.readline.assert_called()

            self.assertEqual(expected_data, data)

    def test_get_location_invalid_nmeatype(self, mock_port):

        mock_port.return_value.inWaiting.return_value = 1
        mock_port.return_value.readline.return_value = (
            "b'$GPGGA,194509.000,A,4042.6142,N,07400.4168,W,2.03,221.11,160412,,,A*77"
        )

        with patch.dict(
            os.environ,
            {
                "GPS_LOG_FILE": "logger.txt",
                "LOG_DIRECTORY": self.temp_dir.path,
                "GPS_PORT": "/dev/serial0",
                "GPS_BAUDRATE": "9600",
            },
        ):

            expected_data = None

            gps_reader = GPSReader()
            data = gps_reader.get_geolocation()

            mock_port.return_value.inWaiting.assert_called()
            mock_port.return_value.readline.assert_called()

            self.assertEqual(expected_data, data)

    def test_get_location_invalid_data(self, mock_port):

        mock_port.return_value.inWaiting.return_value = 1
        mock_port.return_value.readline.return_value = (
            "b'$GPRMC,194509.000,V,4042.6142,N,07400.4168,W,2.03,221.11,160412,,,A*77"
        )

        with patch.dict(
            os.environ,
            {
                "GPS_LOG_FILE": "logger.txt",
                "LOG_DIRECTORY": self.temp_dir.path,
                "GPS_PORT": "/dev/serial0",
                "GPS_BAUDRATE": "9600",
            },
        ):

            expected_data = None

            gps_reader = GPSReader()
            data = gps_reader.get_geolocation()

            mock_port.return_value.inWaiting.assert_called()
            mock_port.return_value.readline.assert_called()

            self.assertEqual(expected_data, data)

    @patch("hardware.gpsPi.gps_reader.date_str_with_current_timezone")
    def test_get_speed_in_mph(self, mock_date, mock_port):

        mock_port.return_value.inWaiting.return_value = 1
        mock_port.return_value.readline.return_value = (
            "b'$GPRMC,194509.000,A,4042.6142,N,07400.4168,W,2.03,221.11,160412,,,A*77"
        )
        mock_date.return_value = "example date"

        with patch.dict(
            os.environ,
            {
                "GPS_LOG_FILE": "logger.txt",
                "LOG_DIRECTORY": self.temp_dir.path,
                "GPS_PORT": "/dev/serial0",
                "GPS_BAUDRATE": "9600",
            },
        ):

            speed_in_mph = 2.03 * 1.151

            expected_data = {}
            expected_data["sensor_id"] = 1
            expected_data["values"] = {
                "speed": speed_in_mph,
            }
            expected_data["date"] = "example date"

            gps_reader = GPSReader()
            data = gps_reader.get_speed_mph()

            mock_port.return_value.inWaiting.assert_called()
            mock_port.return_value.readline.assert_called()

            self.assertEqual(expected_data, data)

    def test_get_speed_in_mph_invalid_data(self, mock_port):

        mock_port.return_value.inWaiting.return_value = 1
        mock_port.return_value.readline.return_value = (
            "b'$GP,194509.000,A,4042.6142,N,07400.4168,W,2.03,221.11,160412,,,A*77"
        )

        with patch.dict(
            os.environ,
            {
                "GPS_LOG_FILE": "logger.txt",
                "LOG_DIRECTORY": self.temp_dir.path,
                "GPS_PORT": "/dev/serial0",
                "GPS_BAUDRATE": "9600",
            },
        ):

            expected_data = None

            gps_reader = GPSReader()
            data = gps_reader.get_speed_mph()

            mock_port.return_value.inWaiting.assert_called()
            mock_port.return_value.readline.assert_called()

            self.assertEqual(expected_data, data)
