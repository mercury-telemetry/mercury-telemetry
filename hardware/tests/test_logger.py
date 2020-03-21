from django.test import SimpleTestCase
from testfixtures import TempDirectory

from logging import INFO
from unittest import mock
import os

from ..CommunicationsPi.logger import Logger


class LoggerTests(SimpleTestCase):
    def setUp(self):
        self.temp_dir = TempDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_create_logger_with_dir(self):
        """
        Simple test for creating a logger
        """
        with mock.patch.dict(os.environ, {"LOG_DIRECTORY": self.temp_dir.path}):
            logger = Logger(name="test_logger", filename="logger.txt")

            self.assertTrue(logger.name == "test_logger")
            self.assertTrue(
                logger.format == "%(asctime)s | %(levelname)s | %(message)s"
            )
            self.assertTrue(logger.level is INFO)

    @mock.patch.object(os, "makedirs")
    @mock.patch("os.path.exists")
    def test_makedir_if_not_exist(self, path_mock, dir_mock):
        """
        insures that the function os.makedir is called if the supplied directory
        doesn't exist
        """
        path_mock.return_value = False
        dir_mock.return_value = self.temp_dir.path
        with mock.patch.dict(os.environ, {"LOG_DIRECTORY": self.temp_dir.path}):
            Logger(name="test_logger", filename="logger.txt")

        dir_mock.assert_called()
        dir_mock.assert_called_with(self.temp_dir.path)
