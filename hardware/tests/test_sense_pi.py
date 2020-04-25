from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock
from testfixtures import TempDirectory

import os
import sys

sys.modules[
    "sense_hat"
] = MagicMock()  # mock these modules so that they don't have to be installed
sys.modules["sense_emu"] = MagicMock()

from hardware.SensorPi.sense_pi import SensePi  # noqa : E402
from hardware.Utils.logger import Logger  # noqa : E402


@patch("hardware.SensorPi.sense_pi.SenseHat")
class SensePiTests(SimpleTestCase):
    def setUp(self):
        self.temp_dir = TempDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_init_no_logs_no_ids(self, mock_sense):

        mock_show_message = MagicMock()
        mock_clear = MagicMock()
        mock_sense.return_value.show_message = mock_show_message
        mock_sense.return_value.clear = mock_clear

        expected_sensor_ids = {
            "temperature": 1,
            "pressure": 2,
            "humidity": 3,
            "acceleration": 4,
            "orientation": 5,
        }

        expected_color = (87, 46, 140)

        with patch.dict(
            os.environ,
            {"SENSE_HAT_LOG_FILE": "logger.txt", "LOG_DIRECTORY": self.temp_dir.path},
        ):
            sense = SensePi()

            mock_show_message.assert_called_with(
                "MERCURY", text_colour=expected_color, scroll_speed=0.04
            )
            mock_clear.assert_called()

            self.assertTrue(sense.logging is not None)
            self.assertTrue(sense.logging.name == "SENSE_HAT_LOG_FILE")
            self.assertIsInstance(sense.logging, Logger)

            self.assertDictEqual(sense.sensor_ids, expected_sensor_ids)

    def test_init_logs_ids(self, mock_sense):

        mock_show_message = MagicMock()
        mock_clear = MagicMock()
        mock_sense.return_value.show_message = mock_show_message
        mock_sense.return_value.clear = mock_clear

        expected_sensor_ids = {
            "temperature": 5,
            "pressure": 4,
            "humidity": 3,
            "acceleration": 2,
            "orientation": 1,
        }

        expected_color = (87, 46, 140)

        with patch.dict(
            os.environ, {"SENSE_LOG": "logger.txt", "LOG_DIRECTORY": self.temp_dir.path}
        ):
            sense = SensePi(log_file_name="SENSE_LOG", sensor_ids=expected_sensor_ids)

            mock_show_message.assert_called_with(
                "MERCURY", text_colour=expected_color, scroll_speed=0.04
            )
            mock_clear.assert_called()

            self.assertTrue(sense.logging is not None)
            self.assertTrue(sense.logging.name == "SENSE_LOG")
            self.assertIsInstance(sense.logging, Logger)

            self.assertDictEqual(sense.sensor_ids, expected_sensor_ids)

    def test_init_no_logs_ids(self, mock_sense):

        mock_show_message = MagicMock()
        mock_clear = MagicMock()
        mock_sense.return_value.show_message = mock_show_message
        mock_sense.return_value.clear = mock_clear

        expected_sensor_ids = {
            "temperature": 5,
            "pressure": 4,
            "humidity": 3,
            "acceleration": 2,
            "orientation": 1,
        }

        expected_color = (87, 46, 140)

        with patch.dict(
            os.environ,
            {"SENSE_HAT_LOG_FILE": "logger.txt", "LOG_DIRECTORY": self.temp_dir.path},
        ):
            sense = SensePi(sensor_ids=expected_sensor_ids)

            mock_show_message.assert_called_with(
                "MERCURY", text_colour=expected_color, scroll_speed=0.04
            )
            mock_clear.assert_called()

            self.assertTrue(sense.logging is not None)
            self.assertTrue(sense.logging.name == "SENSE_HAT_LOG_FILE")
            self.assertIsInstance(sense.logging, Logger)

            self.assertDictEqual(sense.sensor_ids, expected_sensor_ids)

    def test_init_logs_no_ids(self, mock_sense):

        mock_show_message = MagicMock()
        mock_clear = MagicMock()
        mock_sense.return_value.show_message = mock_show_message
        mock_sense.return_value.clear = mock_clear

        expected_sensor_ids = {
            "temperature": 1,
            "pressure": 2,
            "humidity": 3,
            "acceleration": 4,
            "orientation": 5,
        }

        expected_color = (87, 46, 140)

        with patch.dict(
            os.environ, {"SENSE_LOG": "logger.txt", "LOG_DIRECTORY": self.temp_dir.path}
        ):
            sense = SensePi(log_file_name="SENSE_LOG")

            mock_show_message.assert_called_with(
                "MERCURY", text_colour=expected_color, scroll_speed=0.04
            )
            mock_clear.assert_called()

            self.assertTrue(sense.logging is not None)
            self.assertTrue(sense.logging.name == "SENSE_LOG")
            self.assertIsInstance(sense.logging, Logger)

            self.assertDictEqual(sense.sensor_ids, expected_sensor_ids)
