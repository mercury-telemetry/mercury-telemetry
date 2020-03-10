from django.test import TestCase
from django.urls import reverse
from mercury.models import EventCodeAccess, AGSensor


class TestConfigureSensorView(TestCase):
    TESTCODE = "testcode"

    field_name_1 = "field-1"
    field_name_2 = "field-2"
    test_sensor = {
        "name": "Wind Speed Sensor",
        field_name_1: {"field_type": "string", "field_unit": "km"},
        field_name_2: {"field_type": "float", "field_unit": "mph"},
    }

    def setUp(self):
        self.login_url = "mercury:EventAccess"
        self.sensor_url = "mercury:sensor"
        test_code = EventCodeAccess(event_code="testcode", enabled=True)
        test_code.save()

    def _get_with_event_code(self, url, event_code):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": event_code})
        response = self.client.get(reverse(url))
        session = self.client.session
        return response, session

    def post_sensor_data(self):
        # POST sensor data to the sensor url
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "sensor-name": self.test_sensor["name"],
                "field-name": [self.field_name_1, self.field_name_2],
                "field-type": [
                    self.test_sensor[self.field_name_1]["field_type"],
                    self.test_sensor[self.field_name_2]["field_type"],
                ],
                "field-unit": [
                    self.test_sensor[self.field_name_1]["field_unit"],
                    self.test_sensor[self.field_name_2]["field_unit"],
                ],
            },
        )
        return response

    def test_ConfigureSensorView_GET_success(self):
        response, session = self._get_with_event_code(self.sensor_url, self.TESTCODE)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])

    def test_ConfigureSensorView_POST_redirects(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        response = self.post_sensor_data()

        # Check that POST redirects to sensor (same page reloads)
        self.assertEqual(302, response.status_code)
        self.assertEqual("/sensor/", response.url)

    def test_ConfigureSensorView_POST_success_model_created(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        self.post_sensor_data()

        # Check that AGSensor object is created in db with expected params
        sensors = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 1)

    def test_ConfigureSensorView_POST_success_correct_object_created(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        self.post_sensor_data()

        # Check that AGSensor object is created in db with expected values
        sensors = AGSensor.objects.all()
        sensor = sensors[0]
        self.assertEqual(sensor.sensor_name, self.test_sensor["name"])
        self.assertEqual(
            sensor.sensor_format[self.field_name_1]["format"],
            self.test_sensor[self.field_name_1]["field_type"],
        )
        self.assertEqual(
            sensor.sensor_format[self.field_name_2]["format"],
            self.test_sensor[self.field_name_2]["field_type"],
        )
        self.assertEqual(
            sensor.sensor_format[self.field_name_1]["unit"],
            self.test_sensor[self.field_name_1]["field_unit"],
        )
        self.assertEqual(
            sensor.sensor_format[self.field_name_2]["unit"],
            self.test_sensor[self.field_name_2]["field_unit"],
        )
