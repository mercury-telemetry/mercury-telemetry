import datetime

import mock
from django.test import TestCase
from rest_framework.reverse import reverse

from mercury.models import AGEvent


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


def fake_valid(res, raise_exception=True):
    return True


class TestMeasurement(TestCase):
    def setUp(self) -> None:
        self.post_url = "mercury:measurement"
        self.uuid = "d81cac8d-26e1-4983-a942-1922e54a943d"
        self.uuid2 = "d81cac8d-26e1-4983-a942-1922e54a943a"

    def post_radio_data(self):
        # POST sensor data to the measurement url
        response = self.client.post(
            reverse(self.post_url, args=[self.uuid]),
            data={
                "sensor_id": 1,
                "values": {"power": "2", "speed": 1},
                "date": datetime.datetime(2020, 2, 2, 20, 21, 22),
            },
        )
        return response

    def post_defect_data(self):
        response = self.client.post(
            reverse(self.post_url, args=[self.uuid]),
            data={
                "values": {"power": "2", "speed": 1},
                "date": datetime.datetime(2020, 2, 2, 20, 21, 22),
            },
        )
        return response

    def test_Radio_Receiver_POST_Event_Not_Exist(self):
        response = self.client.post(reverse(self.post_url, args=[self.uuid2]))
        self.assertEqual(404, response.status_code)

    @mock.patch("mercury.models.AGEvent.objects.get", fake_event)
    def test_Radio_Receiver_POST_Missing_Params(self):
        response = self.post_defect_data()
        self.assertEqual(400, response.status_code)

    @mock.patch("mercury.models.AGEvent.objects.get", fake_event)
    def test_Radio_Receiver_POST_Fail_to_Save(self):
        response = self.post_radio_data()
        self.assertEqual(400, response.status_code)

    @mock.patch("mercury.models.AGEvent.objects.get", fake_event)
    @mock.patch("mercury.serializers.AGMeasurementSerializer.is_valid", fake_valid)
    @mock.patch("mercury.serializers.AGMeasurementSerializer.save", fake_valid)
    @mock.patch("mercury.serializers.AGMeasurementSerializer.data", "")
    def test_Radio_Receiver_POST_Event_Success(self):
        response = self.post_radio_data()
        self.assertEqual(201, response.status_code)
