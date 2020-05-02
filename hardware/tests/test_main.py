from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock

# from testfixtures import TempDirectory, LogCapture

import os
import sys

sys.modules[
    "sense_hat"
] = MagicMock()  # mock these modules so that they don't have to be installed
sys.modules["sense_emu"] = MagicMock()

from hardware import main  # noqa : E402


@patch("hardware.main.Transceiver")
@patch("hardware.main.WebClient")
@patch("hardware.main.SensePi")
@patch("hardware.main.GPSReader")
class HardwareTests(SimpleTestCase):
    @patch("hardware.main.handleComm")
    def test_main_comm_pi(
        self,
        com_mock=MagicMock(),
        mock_gps=MagicMock(),
        mock_sense=MagicMock(),
        mock_web=MagicMock(),
        mock_trans=MagicMock(),
    ):
        with patch.dict(os.environ, {"HARDWARE_TYPE": "commPi"}):
            main.main()
            com_mock.assert_called_once()

    @patch("hardware.main.handleSense")
    def test_main_sense_pi(
        self,
        sense_mock=MagicMock(),
        mock_gps=MagicMock(),
        mock_sense=MagicMock(),
        mock_web=MagicMock(),
        mock_trans=MagicMock(),
    ):
        with patch.dict(os.environ, {"HARDWARE_TYPE": "sensePi"}):
            main.main()
            sense_mock.assert_called_once()

    @patch("hardware.main.handleGps")
    def test_main_gps_pi(
        self,
        gps_mock=MagicMock(),
        mock_gps=MagicMock(),
        mock_sense=MagicMock(),
        mock_web=MagicMock(),
        mock_trans=MagicMock(),
    ):
        with patch.dict(os.environ, {"HARDWARE_TYPE": "gpsPi"}):
            main.main()
            gps_mock.assert_called_once()

    @patch("hardware.main.handleLocal")
    def test_main_local(
        self,
        local_mock=MagicMock(),
        mock_gps=MagicMock(),
        mock_sense=MagicMock(),
        mock_web=MagicMock(),
        mock_trans=MagicMock(),
    ):
        with patch.dict(os.environ, {"HARDWARE_TYPE": ""}):
            main.main()
            local_mock.assert_called_once()
