import datetime

import mock
from django.test import TestCase
from rest_framework.reverse import reverse

from ag_data.models import AGEvent, AGVenue


def fake_venue():
    return AGVenue(
        uuid="d81cac8d-26e1-4983-a942-1922e54a943a",
        name="fake venue",
        description="fake venue",
        latitude=111.11,
        longitude=111.11,
    )


def fake_event(uuid):
    """
        Mock a dummy AGEvent model
    """
    return AGEvent(
        uuid=uuid,
        name="fake event",
        description="fake event",
        date=datetime.datetime(2020, 2, 2, 20, 21, 22),
        venue_uuid=fake_venue(),
    )


def fake_valid(res, raise_exception=True):
    return True


class TestMeasurement(TestCase):
    def setUp(self) -> None:
        self.post_url = "mercury:measurement"
        self.uuid = "d81cac8d-26e1-4983-a942-1922e54a943d"
        self.uuid2 = "d81cac8d-26e1-4983-a942-1922e54a943a"

    def post_radio_data_wo_event(self):
        data = {
            "sensor_id": 1,
            "values": '{"power": 2, "speed": 1}',
            "date": "2020-03-11T19:20:00",
        }
        response = self.client.post(reverse(self.post_url2), data=data,)
        return response

    def post_radio_data(self):
        # POST sensor data to the measurement url
        data = {
            "sensor_id": 1,
            "values": {"power": 2, "speed": 1},
            "date": "2020-03-11T19:20:00",
        }
        response = self.client.post(
            reverse(self.post_url, args=[self.uuid]), data=data,
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
        self.assertTrue("Event uuid not found" in str(response.content))

    @mock.patch("ag_data.models.AGEvent.objects.get", fake_event)
    def test_Radio_Receiver_POST_Sensor_Not_Exist(self):
        response = self.post_radio_data()
        self.assertEqual(400, response.status_code)
        self.assertTrue("sensor_id" in str(response.content))

    @mock.patch("ag_data.models.AGEvent.objects.get", fake_event)
    def test_Radio_Receiver_POST_Missing_Params(self):
        response = self.post_defect_data()
        self.assertEqual(400, response.status_code)
        self.assertTrue("Missing required params " in str(response.content))

    @mock.patch("ag_data.models.AGEvent.objects.get", fake_event)
    def test_Radio_Receiver_POST_Fail_to_Save(self):
        response = self.post_radio_data()
        self.assertEqual(400, response.status_code)
        self.assertTrue("object does not exist." in str(response.content))

    @mock.patch("ag_data.models.AGEvent.objects.get", fake_event)
    @mock.patch("ag_data.serializers.AGMeasurementSerializer.is_valid", fake_valid)
    @mock.patch("ag_data.serializers.AGMeasurementSerializer.save", fake_valid)
    @mock.patch("ag_data.serializers.AGMeasurementSerializer.data", "")
    def test_Radio_Receiver_POST_Event_Success(self):
        response = self.post_radio_data()
        self.assertEqual(201, response.status_code)
