import json

from django.test import TestCase
from django.urls import reverse
from mercury.models import AGEvent
import datetime
import mock


def fake_event(event_uuid):
    """
        Mock a dummy AGEvent model
    """
    return AGEvent(
        event_uuid=event_uuid,
        event_name="fake event",
        event_description="fake event",
        event_date=datetime.datetime(2020, 2, 2, 20, 21, 22),
        event_location="nyu",
    )


def fake_valid(res):
    return True


def fake_valid_port():
    return ["dev/tty.USB"]


def fake_invalid_port():
    return []


class TestRadioReceiverView(TestCase):
    def setUp(self) -> None:
        self.get_url = "mercury:radioreceiver"
        self.post_url = "mercury:radioreceiver"
        self.uuid = "d81cac8d-26e1-4983-a942-1922e54a943d"
        self.uuid2 = "d81cac8d-26e1-4983-a942-1922e54a943a"

    def test_Radio_Receiver_GET_No_Related_Event(self):
        response = self.client.get(reverse(self.get_url, args=[self.uuid2]))
        self.assertEqual(400, response.status_code)

    @mock.patch("mercury.models.AGEvent.objects.get", fake_event)
    def test_Radio_Receiver_GET_Missing_Enable(self):
        response = self.client.get(
            reverse(self.get_url, args=[self.uuid]),
            data={
                "baudrate": 9000,
                "bytesize": 8,
                "parity": "N",
                "stopbits": 1,
                "timeout": 1,
            },
        )
        self.assertEqual(400, response.status_code)
        self.assertEqual("Missing enable value in url", json.loads(response.content))

    @mock.patch("mercury.models.AGEvent.objects.get", fake_event)
    @mock.patch("mercury.views.radioreceiver.serial_ports", fake_invalid_port)
    def test_Radio_Receiver_GET_No_Valid_Port(self):
        response = self.client.get(
            reverse(self.get_url, args=[self.uuid]),
            data={
                "enable": 1,
                "baudrate": 9000,
                "bytesize": 8,
                "parity": "N",
                "stopbits": 1,
                "timeout": 1,
            },
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual("No valid ports on the backend", json.loads(response.content))

    @mock.patch("mercury.models.AGEvent.objects.get", fake_event)
    @mock.patch("mercury.views.radioreceiver.serial_ports", fake_valid_port)
    def test_Radio_Receiver_GET_Success(self):
        response = self.client.get(
            reverse(self.get_url, args=[self.uuid]),
            data={
                "enable": 1,
                "baudrate": 9000,
                "bytesize": 8,
                "parity": "N",
                "stopbits": 1,
                "timeout": 1,
            },
        )
        self.assertEqual(200, response.status_code)

    @mock.patch("mercury.models.AGEvent.objects.get", fake_event)
    @mock.patch("mercury.views.radioreceiver.serial_ports", fake_valid_port)
    @mock.patch("mercury.views.radioreceiver.check_port", fake_valid)
    def test_Radio_Receiver_GET_Close_Port_Success(self):
        response = self.client.get(
            reverse(self.get_url, args=[self.uuid]),
            data={
                "enable": 0,
                "baudrate": 9000,
                "bytesize": 8,
                "parity": "N",
                "stopbits": 1,
                "timeout": 1,
            },
        )
        self.assertEqual(200, response.status_code)

    @mock.patch("mercury.models.AGEvent.objects.get", fake_event)
    def test_Radio_Receiver_Fake_GET_Success(self):
        response = self.client.get(
            reverse(self.get_url, args=[self.uuid]),
            data={
                "enable": 1,
                "baudrate": 9000,
                "bytesize": 8,
                "parity": "N",
                "stopbits": 1,
                "timeout": 1,
                "fake": 1,
            },
        )
        self.assertEqual(200, response.status_code)
