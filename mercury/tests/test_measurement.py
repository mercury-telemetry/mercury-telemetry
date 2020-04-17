import datetime
import uuid

import mock
from django.test import TestCase
from rest_framework.reverse import reverse

from ag_data.models import AGEvent, AGVenue


def fake_venue():
    """
    Mock a dummy AGVenue model
    """
    return AGVenue(
        uuid="d81cac8d-26e1-4983-a942-1922e54a943a",
        name="fake venue",
        description="fake venue",
        latitude=111.11,
        longitude=111.11,
    )


def fake_event():
    """
    Mock a dummy AGEvent model
    """
    return AGEvent(
        uuid=uuid.uuid4(),
        name="fake event",
        description="fake event",
        date=datetime.datetime(2020, 2, 2, 20, 21, 22),
        venue_uuid=fake_venue(),
    )


def fake_valid(res, raise_exception=True):
    return True


class TestMeasurement(TestCase):
    test_measurement_data = {
        "sensor_id": 1,
        "values": {"power": 2, "speed": 1},
        "date": "2020-03-11T19:20:00",
    }

    def setUp(self) -> None:
        self.post_url = "mercury:measurement"

    def post_data(self, data):
        # POST sensor data to the measurement url
        response = self.client.post(reverse(self.post_url), data=data,)
        return response

    @mock.patch("mercury.views.measurement.fetch_event", fake_event)
    def test_Radio_Receiver_POST_Sensor_Not_Exist(self):
        data = self.test_measurement_data.copy()
        response = self.post_data(data)
        self.assertEqual(400, response.status_code)
        self.assertTrue("sensor_id" in str(response.content))

    @mock.patch("mercury.views.measurement.fetch_event", fake_event)
    def test_Radio_Receiver_POST_Missing_Params(self):
        data = self.test_measurement_data.copy()
        data.pop("sensor_id")
        response = self.post_data(data)
        self.assertEqual(400, response.status_code)
        self.assertTrue("Missing required params " in str(response.content))

    @mock.patch("mercury.views.measurement.fetch_event", fake_event)
    def test_Radio_Receiver_POST_Fail_to_Save(self):
        data = self.test_measurement_data.copy()
        response = self.post_data(data)
        self.assertEqual(400, response.status_code)
        self.assertTrue("object does not exist." in str(response.content))

    @mock.patch("mercury.views.measurement.fetch_event", fake_event)
    @mock.patch("ag_data.serializers.AGMeasurementSerializer.is_valid", fake_valid)
    @mock.patch("ag_data.serializers.AGMeasurementSerializer.save", fake_valid)
    @mock.patch("ag_data.serializers.AGMeasurementSerializer.data", "")
    def test_Radio_Receiver_POST_Event_Success(self):
        data = self.test_measurement_data.copy()
        response = self.post_data(data)
        self.assertEqual(201, response.status_code)
