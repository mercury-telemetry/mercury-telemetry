from django.test import SimpleTestCase
from testfixtures import TempDirectory, LogCapture

from logging import INFO, ERROR, DEBUG
from unittest import mock
import os

from hardware.Utils.logger import Logger


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

    def test_create_logger_with_level(self):
        with mock.patch.dict(os.environ, {"LOG_DIRECTORY": self.temp_dir.path}):
            logger = Logger(name="test_logger", filename="logger.txt", level=ERROR)

            self.assertTrue(logger.name == "test_logger")
            self.assertTrue(
                logger.format == "%(asctime)s | %(levelname)s | %(message)s"
            )
            self.assertTrue(logger.level is ERROR)

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

    def test_info_message(self):
        """
        Tests the .info method
        """
        with mock.patch.dict(os.environ, {"LOG_DIRECTORY": self.temp_dir.path}):
            with LogCapture() as capture:
                logger = Logger(name="test_logger", filename="logger.txt")
                logger.info("test message")

                capture.check(("test_logger", "INFO", "test message"))

    def test_message_failure(self):
        """
        makes sure that nothing is logged during initialization
        """
        with mock.patch.dict(os.environ, {"LOG_DIRECTORY": self.temp_dir.path}):
            with LogCapture() as capture:
                logger = Logger(name="test_logger", filename="logger.txt")  # noqa: F841
                capture.check()  # expect no output

    def test_error_message(self):
        """
        Tests the .error method
        """
        with mock.patch.dict(os.environ, {"LOG_DIRECTORY": self.temp_dir.path}):
            with LogCapture() as capture:
                logger = Logger(name="test_logger", filename="logger.txt")
                logger.error("test message")

                capture.check(("test_logger", "ERROR", "test message"))

    def test_debug_message(self):
        """
        Tests the .debug method
        """
        with mock.patch.dict(os.environ, {"LOG_DIRECTORY": self.temp_dir.path}):
            with LogCapture() as capture:
                mylogger = Logger(
                    name="test_logger", filename="logger.txt", level=DEBUG
                )
                mylogger.debug("test message")

                capture.check(("test_logger", "DEBUG", "test message"))

    def test_warn_message(self):
        """
        Tests the .warn method
        """
        with mock.patch.dict(os.environ, {"LOG_DIRECTORY": self.temp_dir.path}):
            with LogCapture() as capture:
                mylogger = Logger(name="test_logger", filename="logger.txt")
                mylogger.warn("test message")

                capture.check(("test_logger", "WARNING", "test message"))
