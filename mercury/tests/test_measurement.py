import json

from django.test import TestCase
from rest_framework.reverse import reverse

from ag_data.models import AGEvent, AGSensor, AGSensorType, AGActiveEvent


class TestMeasurement(TestCase):
    fixtures = ["sample.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_measurement_data = {
            "sensor_id": 1,
            "values": {"power": 2, "speed": 1},
            "date": "2020-03-11T19:20:00",
        }
        cls.sensor_type = AGSensorType.objects.first()
        AGSensor.objects.create(id=1, name="test sensor", type_id=cls.sensor_type)
        AGActiveEvent.objects.create(agevent=AGEvent.objects.first())

    def setUp(self):
        self.data = TestMeasurement.test_measurement_data.copy()

    def post_data(self, data):
        return self.client.post(
            reverse("mercury:measurement"),
            data=json.dumps(data),
            content_type="application/json",
        )

    def test_success(self):
        response = self.post_data(self.data)
        self.assertEqual(201, response.status_code)

    def test_error_sensor_not_exist(self):
        self.data["sensor_id"] = 9999
        response = self.post_data(self.data)
        self.assertEqual(400, response.status_code)
        self.assertTrue("sensor_id" in str(response.content))

    def test_error_missing_params(self):
        self.data.pop("sensor_id")
        response = self.post_data(self.data)
        self.assertEqual(400, response.status_code)
        self.assertTrue("Missing required params" in str(response.content))

    def test_error_invalid_timestamp(self):
        self.data["date"] = "May 05, 2020"
        response = self.post_data(self.data)
        self.assertEqual(400, response.status_code)
        self.assertTrue("Invalid timestamp" in str(response.content))

    def test_error_no_event(self):
        AGActiveEvent.objects.all().delete()
        response = self.post_data(self.data)
        self.assertEqual(400, response.status_code)
        self.assertTrue("No active event" in str(response.content))
