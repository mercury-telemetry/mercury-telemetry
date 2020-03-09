from django.test import TestCase
from django.urls import reverse
from mercury.models import EventCodeAccess, AGSensor

TESTCODE = "testcode"

test_sensor = {
    "name": "Wind Speed Sensor",
    "field-0": {
        "field_type": "string",
        "field_unit": "km"
    },
    "field-1": {
        "field_type": "float",
        "field_unit": "mph"
    }
}

class TestConfigureSensorView(TestCase):
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

    def test_ConfigureSensorView_GET_success(self):
        response, session = self._get_with_event_code(self.sensor_url, TESTCODE)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])

    def test_ConfigureSensorView_POST_success(self):
        # login step
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": "testcode"})
        response = self.client.get(reverse(self.login_url))
        self.assertEqual(302, response.status_code)
        self.assertEqual("index", response.url)

        response = self.client.post(reverse(self.sensor_url), data={
            "sensor-name": test_sensor["name"],
            "field-name": ["field-0", "field-1"],
            "field-type": [test_sensor["field-0"]["field_type"], test_sensor[
                "field-1"]["field_type"]],
            "field-unit": [test_sensor["field-0"]["field_unit"], test_sensor[
                "field-1"]["field_unit"]]
        })
        self.assertEqual(302, response.status_code)
        sensors = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 1)
        sensor = sensors[0]
        self.assertEqual(sensor.sensor_name, "Wind Speed Sensor")
        self.assertEqual(sensor.sensor_format["field-0"]["format"], test_sensor[
            "field-0"]["field_type"])
        self.assertEqual(sensor.sensor_format["field-1"]["format"], test_sensor[
            "field-1"]["field_type"])
        self.assertEqual(sensor.sensor_format["field-0"]["unit"], test_sensor[
            "field-0"]["field_unit"])
        self.assertEqual(sensor.sensor_format["field-1"]["unit"], test_sensor[
            "field-1"]["field_unit"])