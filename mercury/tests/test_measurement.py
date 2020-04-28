import json
import uuid

from django.test import TestCase
from rest_framework.reverse import reverse

from ag_data.models import AGEvent, AGSensor, AGSensorType, AGActiveEvent, ErrorLog
from ag_data.error_record import record


class TestMeasurement(TestCase):
    fixtures = ["sample.json"]

    @classmethod
    def setUpTestData(cls):
        sensor_uuid = uuid.uuid4()

        cls.test_measurement_data = {
            "sensor_id": str(sensor_uuid),
            "values": {"power": 2, "speed": 1},
            "date": "2020-03-11T19:20:00",
        }
        cls.sensor_type = AGSensorType.objects.first()
        AGSensor.objects.create(
            uuid=sensor_uuid, name="test sensor", type_id=cls.sensor_type
        )
        AGActiveEvent.objects.create(agevent=AGEvent.objects.first())

    def setUp(self):
        self.data = TestMeasurement.test_measurement_data.copy()

    def post_data(self, data):
        return self.client.post(
            reverse("mercury:measurement"),
            data=json.dumps(data),
            content_type="application/json",
        )

    def assert_error(self, error_code, raw_data):
        foo = ErrorLog.objects.first()
        return (foo.error_code == error_code) and (foo.raw_data == raw_data)

    def test_success(self):
        response = self.post_data(self.data)
        self.assertEqual(201, response.status_code)

    def test_error_sensor_not_exist(self):
        self.data["sensor_id"] = 9999
        response = self.post_data(self.data)
        self.assertEqual(400, response.status_code)
        self.assertTrue("sensor_id" in str(response.content))
        self.assertTrue(
            self.assert_error(
                error_code=record.ERROR_CODE["INVALID_COL_VL"],
                raw_data=json.dumps(self.data),
            )
        )

    def test_error_missing_params(self):
        self.data.pop("sensor_id")
        response = self.post_data(self.data)
        self.assertEqual(400, response.status_code)
        self.assertTrue("Missing required params" in str(response.content))
        self.assertTrue(
            self.assert_error(
                error_code=record.ERROR_CODE["MISSING_COL"],
                raw_data=json.dumps(self.data),
            )
        )

    def test_error_invalid_timestamp(self):
        self.data["date"] = "May 05, 2020"
        response = self.post_data(self.data)
        self.assertEqual(400, response.status_code)
        self.assertTrue("Invalid timestamp" in str(response.content))
        self.assertTrue(
            self.assert_error(
                error_code=record.ERROR_CODE["INVALID_COL_VL"],
                raw_data=json.dumps(self.data),
            )
        )

    def test_error_no_event(self):
        AGActiveEvent.objects.all().delete()
        response = self.post_data(self.data)
        self.assertEqual(400, response.status_code)
        self.assertTrue("No active event" in str(response.content))
        self.assertTrue(
            self.assert_error(
                error_code=record.ERROR_CODE["NO_ACT_EVENT"], raw_data=str(self.data)
            )
        )
