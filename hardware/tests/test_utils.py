from django.test import SimpleTestCase

from unittest import mock
from testfixtures import TempDirectory
from logging import INFO
import os
from datetime import datetime
import dateutil.parser

from hardware.Utils.utils import (
    get_logger,
    get_serial_stream,
    date_str_with_current_timezone,
    get_sensor_keys,
)
from hardware.Utils.logger import Logger


class UtilsTests(SimpleTestCase):

    SENSOR_KEYS = {
        "ALL": "all",
        "TEMPERATURE": "temperature",
        "PRESSURE": "pressure",
        "HUMIDITY": "humidity",
        "ACCELERATION": "acceleration",
        "ORIENTATION": "orientation",
    }

    def test_get_logger(self):

        with TempDirectory() as temp_dir:
            with mock.patch.dict(
                os.environ, {"LOG_DIRECTORY": temp_dir.path, "LOGGER": "logger.txt"}
            ):
                logger = get_logger("LOGGER")

                self.assertTrue(logger.name == "LOGGER")
                self.assertTrue(
                    logger.format == "%(asctime)s | %(levelname)s | %(message)s"
                )
                self.assertTrue(logger.level == INFO)
                self.assertIsInstance(logger, Logger)

    def test_serial_stream(self):

        message = {
            "id": 5,
            "value": {"value_a_name": 15.0, "value_b_name": 26.5, "value_c_name": 13.3},
        }
        stream = get_serial_stream(message)
        self.assertEqual(
            stream,
            b'{"id": 5, "value": {"value_a_name": 15.0, "value_b_name": 26.5, "value_c_name": 13.3}}\n',
        )

    def test_date_str_with_current_timezone(self):
        s = date_str_with_current_timezone()
        date = dateutil.parser.isoparse(s)
        self.assertTrue("T" in s)
        self.assertAlmostEqual(date.timestamp(), datetime.now().timestamp(), places=1)

    def test_get_sensor_keys(self):
        self.assertDictEqual(get_sensor_keys(), UtilsTests.SENSOR_KEYS)
