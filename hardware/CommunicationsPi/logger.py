# import sys
import os
import logging

from logging import INFO


class Logger(object):
    def __init__(
        self,
        name,
        filename,
        format="%(asctime)s | %(levelname)s | %(message)s",
        level=INFO,
    ):
        # Initial construct.
        self.format = format
        self.level = level
        self.name = name

        # Logger configuration.
        self.console_formatter = logging.Formatter(self.format)
        self.console_logger = logging.FileHandler(self.get_logger_file(filename), "w")
        self.console_logger.setFormatter(self.console_formatter)

        # Complete logging config.
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        self.logger.addHandler(self.console_logger)

    def get_logger_file(self, file_name):
        d = os.environ["LOG_DIRECTORY"]
        if not os.path.exists(d):
            os.makedirs(d)
        return d + "/" + file_name

    def info(self, msg, extra=None):
        print(msg)
        self.logger.info(msg, extra=extra)

    def error(self, msg, extra=None):
        print(msg)
        self.logger.error(msg, extra=extra)

    def debug(self, msg, extra=None):
        print(msg)
        self.logger.debug(msg, extra=extra)

    def warn(self, msg, extra=None):
        print(msg)
        self.logger.warn(msg, extra=extra)
