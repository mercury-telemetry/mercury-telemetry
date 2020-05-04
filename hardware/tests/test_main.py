from django.test import SimpleTestCase
from unittest.mock import patch, MagicMock, call

from testfixtures import TempDirectory

import os
import sys
import json

sys.modules[
    "sense_hat"
] = MagicMock()  # mock these modules so that they don't have to be installed
sys.modules["sense_emu"] = MagicMock()

from hardware import main  # noqa : E402
from hardware.CommunicationsPi.comm_pi import CommPi  # noqa : E402


@patch("hardware.main.Transceiver")
@patch("hardware.main.WebClient")
@patch("hardware.main.SensePi")
@patch("hardware.main.GPSReader")
class HardwareTests(SimpleTestCase):
    def setUp(self):
        self.temp_dir = TempDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    @patch("hardware.main.handleComm")
    def test_main_comm_pi(
        self,
        com_mock=MagicMock(),
        mock_gps=MagicMock(),
        mock_sense=MagicMock(),
        mock_web=MagicMock(),
        mock_trans=MagicMock(),
    ):
        with patch.dict(
            os.environ, {"HARDWARE_TYPE": "commPi", "LOG_DIRECTORY": self.temp_dir.path}
        ):
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
        with patch.dict(
            os.environ,
            {"HARDWARE_TYPE": "sensePi", "LOG_DIRECTORY": self.temp_dir.path},
        ):
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
        with patch.dict(
            os.environ, {"HARDWARE_TYPE": "gpsPi", "LOG_DIRECTORY": self.temp_dir.path}
        ):
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
        with patch.dict(
            os.environ, {"HARDWARE_TYPE": "", "LOG_DIRECTORY": self.temp_dir.path}
        ):
            main.main()
            local_mock.assert_called_once()

    @patch("hardware.main.runServer")
    def test_handle_comm(
        self,
        server_mock=MagicMock(),
        mock_gps=MagicMock(),
        mock_sense=MagicMock(),
        mock_web=MagicMock(),
        mock_trans=MagicMock(),
    ):
        main.handleComm()
        server_mock.assert_called_once_with(handler_class=CommPi)

    @patch("time.sleep")
    def test_handle_sense(
        self,
        sleep_mock=MagicMock(),
        mock_gps=MagicMock(),
        mock_sense=MagicMock(),
        mock_web=MagicMock(),
        mock_trans=MagicMock(),
    ):
        # allow the time.sleep method to be called 5 times before throwing an error
        # this allows us to check that the data is being sent, but prevents it from
        # iterating forever
        sleep_mock.side_effect = ErrorAfter(5)

        expected_sensor_keys = {
            "temperature": 2,
            "pressure": 3,
            "humidity": 4,
            "acceleration": 5,
            "orientation": 6,
        }

        temp_data = {"key": "temp"}
        pres_data = {"key": "pres"}
        hum_data = {"key": "hum"}
        acc_data = {"key": "acc"}
        orient_data = {"key": "orient"}
        all_data = {"key": "all"}

        mock_sense.return_value.get_temperature.return_value = temp_data
        mock_sense.return_value.get_pressure.return_value = pres_data
        mock_sense.return_value.get_humidity.return_value = hum_data
        mock_sense.return_value.get_acceleration.return_value = acc_data
        mock_sense.return_value.get_orientation.return_value = orient_data
        mock_sense.return_value.get_all.return_value = all_data

        send_data_mock = MagicMock()
        mock_web.return_value.send = send_data_mock

        with self.assertRaises(Exception):
            main.handleSense()

        print(f"call list: {send_data_mock.call_args_list}")
        mock_sense.assert_called_with(sensor_ids=expected_sensor_keys)  # assert init
        mock_web.assert_called()  # assert init

        self.assertEqual(6, send_data_mock.call_count)
        send_data_mock.assert_has_calls(
            [
                call(temp_data),
                call(pres_data),
                call(hum_data),
                call(acc_data),
                call(orient_data),
                call(all_data),
            ],
            any_order=True,
        )

    def test_handle_sense_with_exception(
        self,
        mock_gps=MagicMock(),
        mock_sense=MagicMock(),
        mock_web=MagicMock(),
        mock_trans=MagicMock(),
    ):
        expected_sensor_keys = {
            "temperature": 2,
            "pressure": 3,
            "humidity": 4,
            "acceleration": 5,
            "orientation": 6,
        }

        temp_data = {"key": "temp"}
        pres_data = {"key": "pres"}
        hum_data = {"key": "hum"}
        acc_data = {"key": "acc"}
        orient_data = {"key": "orient"}
        all_data = {"key": "all"}

        mock_sense.return_value.get_temperature.return_value = temp_data
        mock_sense.return_value.get_pressure.return_value = pres_data
        mock_sense.return_value.get_humidity.return_value = hum_data
        mock_sense.return_value.get_acceleration.return_value = acc_data
        mock_sense.return_value.get_orientation.return_value = orient_data
        mock_sense.return_value.get_all.return_value = all_data

        mock_web.return_value.send.side_effect = CallableExhausted("exhausted")

        with self.assertRaises(Exception):
            main.handleSense()

        mock_sense.assert_called_with(sensor_ids=expected_sensor_keys)  # assert init
        mock_web.assert_called()  # assert init

    @patch("time.sleep")
    def test_handle_gps(
        self,
        sleep_mock=MagicMock(),
        mock_gps=MagicMock(),
        mock_sense=MagicMock(),
        mock_web=MagicMock(),
        mock_trans=MagicMock(),
    ):
        sleep_mock.side_effect = ErrorAfter(1)

        gps_data = {"key": "gps"}
        speed_data = {"key": "speed"}

        mock_gps.return_value.get_geolocation.return_value = gps_data
        mock_gps.return_value.get_speed_mph.return_value = speed_data

        send_data_mock = MagicMock()
        mock_web.return_value.send = send_data_mock

        with self.assertRaises(CallableExhausted):
            main.handleGps()

        mock_gps.assert_called_once()  # assert init
        mock_web.assert_called_once()  # assert init
        self.assertEquals(2, send_data_mock.call_count)
        send_data_mock.assert_has_calls(
            [call(gps_data), call(speed_data)], any_order=True
        )

    def test_handle_gps_with_exception(
        self,
        mock_gps=MagicMock(),
        mock_sense=MagicMock(),
        mock_web=MagicMock(),
        mock_trans=MagicMock(),
    ):
        gps_data = {"key": "gps"}

        mock_gps.return_value.get_geolocation.return_value = gps_data

        mock_web.return_value.send.side_effect = Exception("ex")

        with self.assertRaises(Exception):
            main.handleGps()

        mock_gps.assert_called_once()  # assert init
        mock_web.assert_called_once()  # assert init

    def test_handle_local(
        self,
        mock_gps=MagicMock(),
        mock_sense=MagicMock(),
        mock_web=MagicMock(),
        mock_trans=MagicMock(),
    ):
        mock_url = "localhost"
        with patch.dict(os.environ, {"DJANGO_SERVER_API_ENDPOINT": mock_url}):

            str_data = '{"key": "value"}'
            mock_trans.return_value.listen.return_value = str_data

            send_data_mock = MagicMock()
            mock_web.return_value.send = send_data_mock
            mock_web.return_value.send.side_effect = ErrorAfter(0)

            with self.assertRaises(CallableExhausted):
                main.handleLocal()

            mock_trans.assert_called_once()  # assert init
            mock_web.assert_called_with(server_url=mock_url)  # assert init
            self.assertEquals(1, send_data_mock.call_count)
            send_data_mock.assert_has_calls(
                [call(json.loads(str_data))], any_order=True
            )

    @patch("builtins.print")
    def test_handle_local_no_url(
        self,
        mock_print=MagicMock(),
        mock_gps=MagicMock(),
        mock_sense=MagicMock(),
        mock_web=MagicMock(),
        mock_trans=MagicMock(),
    ):
        with patch.dict(os.environ, {"DJANGO_SERVER_API_ENDPOINT": ""}):

            main.handleLocal()

            mock_trans.assert_called_once()
            mock_print.assert_has_calls([call("DJANGO_SERVER_API_ENDPOINT not set")])

    def test_handle_local_no_data(
        self,
        mock_gps=MagicMock(),
        mock_sense=MagicMock(),
        mock_web=MagicMock(),
        mock_trans=MagicMock(),
    ):
        mock_url = "localhost"
        with patch.dict(os.environ, {"DJANGO_SERVER_API_ENDPOINT": mock_url}):

            str_data = None
            mock_trans.return_value.listen.return_value = str_data
            mock_trans.return_value.listen.side_effect = ErrorAfter(1)

            send_data_mock = MagicMock()
            mock_web.return_value.send = send_data_mock

            with self.assertRaises(CallableExhausted):
                main.handleLocal()

            mock_trans.assert_called_once()  # assert init
            mock_web.assert_called_with(server_url=mock_url)  # assert init
            send_data_mock.assert_not_called()


class ErrorAfter(object):
    """
    Callable that will raise `CallableExhausted`
    exception after `limit` calls
    """

    def __init__(self, limit):
        self.limit = limit
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        if self.calls > self.limit:
            raise CallableExhausted()


class CallableExhausted(Exception):
    pass
