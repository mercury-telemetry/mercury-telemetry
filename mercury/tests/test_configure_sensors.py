from django.test import TestCase
from django.urls import reverse
from mercury.models import EventCodeAccess
from ag_data.models import AGSensor, AGSensorType


class TestConfigureSensorView(TestCase):
    TESTCODE = "testcode"

    def setUp(self):
        self.login_url = "mercury:EventAccess"
        self.sensor_url = "mercury:sensor"
        test_code = EventCodeAccess(event_code="testcode", enabled=True)
        test_code.save()

        # Create test objects to compare to
        self.test_type_object_name = "live-feed"
        test_type_object = AGSensorType.objects.create(
            name = self.test_type_object_name,
            processing_formula = 0,
            format = {
                "test-field-1": {
                    "data_type": "test-data-type-1",
                    "unit": "test-unit-1",
                },
                "test-field-2": {
                    "data_type": "test-data-type-2",
                    "unit": "test-unit-2",
                },
            },
        )   
        test_type_object.save()

        self.test_sensor = {
            "name": "wind speed sensor",
            "type_name": self.test_type_object_name,
        }

    def _get_with_event_code(self, url, event_code):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": event_code})
        response = self.client.get(reverse(url))
        session = self.client.session
        return response, session

    def test_ConfigureSensorView_GET_success(self):
        response, session = self._get_with_event_code(self.sensor_url, self.TESTCODE)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])

    # Valid POST tests

    # Valid POST returns status OK
    def test_ConfigureSensorView_valid_POST_returns_status_ok(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "", 
                "sensor-name": self.test_sensor["name"],
                "select-sensor-type": self.test_sensor["type_name"]
            }
        )

        # Check that POST redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    # Valid POST creates new AGSensor object
    def test_ConfigureSensorView_valid_POST_success_object_created(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST good sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "", 
                "sensor-name": self.test_sensor["name"],
                "select-sensor-type": self.test_sensor["type_name"]
            }
        )

        # Check that AGSensor object is created in db with expected params
        sensors = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 1)


    # # Valid POST creates new AGSensor object with expected parameters
    # def test_ConfigureSensorView_valid_POST_object_created_with_correct_params(self):
    #     # Login
    #     self._get_with_event_code(self.sensor_url, self.TESTCODE)

    #     # POST sensor data
    #     self.client.post(
    #         reverse(self.sensor_url),
    #         data={
    #             "sensor-name": self.test_sensor["name"],
    #             "field-name": [self.field_name_1, self.field_name_2],
    #             "field-type": [
    #                 self.test_sensor[self.field_name_1]["field_type"],
    #                 self.test_sensor[self.field_name_2]["field_type"],
    #             ],
    #             "field-unit": [
    #                 self.test_sensor[self.field_name_1]["field_unit"],
    #                 self.test_sensor[self.field_name_2]["field_unit"],
    #             ],
    #         },
    #     )

    #     # Check that AGSensor object is created in db with expected values
    #     sensors = AGSensor.objects.all()
    #     sensor = sensors[0]
    #     self.assertEqual(sensor.sensor_name, self.test_sensor["name"])
    #     self.assertEqual(
    #         sensor.sensor_format[self.field_name_1]["format"],
    #         self.test_sensor[self.field_name_1]["field_type"],
    #     )
    #     self.assertEqual(
    #         sensor.sensor_format[self.field_name_2]["format"],
    #         self.test_sensor[self.field_name_2]["field_type"],
    #     )
    #     self.assertEqual(
    #         sensor.sensor_format[self.field_name_1]["unit"],
    #         self.test_sensor[self.field_name_1]["field_unit"],
    #     )
    #     self.assertEqual(
    #         sensor.sensor_format[self.field_name_2]["unit"],
    #         self.test_sensor[self.field_name_2]["field_unit"],
    #     )

    # # Invalid POST tests

    # # Duplicate field names still returns status ok
    # def test_ConfigureSensorView_invalid_POST_duplicate_fields_returns_status_ok(self):
    #     # Login
    #     self._get_with_event_code(self.sensor_url, self.TESTCODE)

    #     # POST sensor data
    #     response = self.client.post(
    #         reverse(self.sensor_url),
    #         data={
    #             "sensor-name": self.test_sensor["name"],
    #             "field-name": [self.field_name_1, self.field_name_1],
    #             "field-type": [
    #                 self.test_sensor[self.field_name_1]["field_type"],
    #                 self.test_sensor[self.field_name_2]["field_type"],
    #             ],
    #             "field-unit": [
    #                 self.test_sensor[self.field_name_1]["field_unit"],
    #                 self.test_sensor[self.field_name_2]["field_unit"],
    #             ],
    #         },
    #     )

    #     # Check that POST redirects to sensor (same page reloads)
    #     self.assertEqual(200, response.status_code)

    # # Duplicate field names - no AGSensor object created
    # def test_ConfigureSensorView_invalid_POST_field_duplicates_no_object_created(self):
    #     # Login
    #     self._get_with_event_code(self.sensor_url, self.TESTCODE)

    #     # POST sensor data with duplicate field names
    #     self.client.post(
    #         reverse(self.sensor_url),
    #         data={
    #             "sensor-name": self.test_sensor["name"],
    #             "field-name": [self.field_name_1, self.field_name_1],
    #             "field-type": [
    #                 self.test_sensor[self.field_name_1]["field_type"],
    #                 self.test_sensor[self.field_name_2]["field_type"],
    #             ],
    #             "field-unit": [
    #                 self.test_sensor[self.field_name_1]["field_unit"],
    #                 self.test_sensor[self.field_name_2]["field_unit"],
    #             ],
    #         },
    #     )

    #     # Check that AGSensor object is created in db with expected params
    #     sensors = AGSensor.objects.all()
    #     self.assertEqual(sensors.count(), 0)

    # # Sensor name missing still returns status OK
    # def test_ConfigureSensorView_invalid_POST_sensor_name_missing_status_ok(self):
    #     # Login
    #     self._get_with_event_code(self.sensor_url, self.TESTCODE)

    #     # POST sensor data
    #     response = self.client.post(
    #         reverse(self.sensor_url),
    #         data={
    #             "sensor-name": "",
    #             "field-name": [self.field_name_1, self.field_name_2],
    #             "field-type": [
    #                 self.test_sensor[self.field_name_1]["field_type"],
    #                 self.test_sensor[self.field_name_2]["field_type"],
    #             ],
    #             "field-unit": [
    #                 self.test_sensor[self.field_name_1]["field_unit"],
    #                 self.test_sensor[self.field_name_2]["field_unit"],
    #             ],
    #         },
    #     )

    #     # Check that POST redirects to sensor (same page reloads)
    #     self.assertEqual(200, response.status_code)

    # # Sensor name missing - no AGSensor object created
    # def test_ConfigureSensorView_bad_POST_sensor_name_missing_no_object_created(self):
    #     # Login
    #     self._get_with_event_code(self.sensor_url, self.TESTCODE)

    #     # POST sensor data
    #     self.client.post(
    #         reverse(self.sensor_url),
    #         data={
    #             "sensor-name": "",
    #             "field-name": [self.field_name_1, self.field_name_1],
    #             "field-type": [
    #                 self.test_sensor[self.field_name_1]["field_type"],
    #                 self.test_sensor[self.field_name_2]["field_type"],
    #             ],
    #             "field-unit": [
    #                 self.test_sensor[self.field_name_1]["field_unit"],
    #                 self.test_sensor[self.field_name_2]["field_unit"],
    #             ],
    #         },
    #     )

    #     # Check that AGSensor object is created in db with expected params
    #     sensors = AGSensor.objects.all()
    #     self.assertEqual(sensors.count(), 0)

    # # Field name missing still returns status OK
    # def test_ConfigureSensorView_invalid_POST_field_name_missing_status_ok(self):
    #     # Login
    #     self._get_with_event_code(self.sensor_url, self.TESTCODE)

    #     # POST sensor data
    #     response = self.client.post(
    #         reverse(self.sensor_url),
    #         data={
    #             "sensor-name": self.test_sensor["name"],
    #             "field-name": [""],
    #             "field-type": [self.test_sensor[self.field_name_1]["field_type"]],
    #             "field-unit": [self.test_sensor[self.field_name_1]["field_unit"]],
    #         },
    #     )

    #     # Check that POST redirects to sensor (same page reloads)
    #     self.assertEqual(200, response.status_code)

    # # Field name missing - no AGSensor object created
    # def test_ConfigureSensorView_bad_POST_field_name_missing_no_object_created(self):
    #     # Login
    #     self._get_with_event_code(self.sensor_url, self.TESTCODE)

    #     # POST sensor data
    #     self.client.post(
    #         reverse(self.sensor_url),
    #         data={
    #             "sensor-name": self.test_sensor["name"],
    #             "field-name": [""],
    #             "field-type": [self.test_sensor[self.field_name_1]["field_type"]],
    #             "field-unit": [self.test_sensor[self.field_name_1]["field_unit"]],
    #         },
    #     )

    #     # Check that AGSensor object is created in db with expected params
    #     sensors = AGSensor.objects.all()
    #     self.assertEqual(sensors.count(), 0)

    # # Sensor name already in use - still returns status OK
    # def test_ConfigureSensorView_invalid_POST_sensor_name_taken_status_ok(self):
    #     sensor_format = {
    #         self.field_name_1: {
    #             "unit": self.test_sensor[self.field_name_1]["field_type"],
    #             "format": self.test_sensor[self.field_name_1]["field_unit"],
    #         }
    #     }

    #     AGSensor.objects.create(
    #         sensor_name=self.test_sensor["name"], sensor_format=sensor_format
    #     )

    #     # Login
    #     self._get_with_event_code(self.sensor_url, self.TESTCODE)

    #     # POST sensor data
    #     response = self.client.post(
    #         reverse(self.sensor_url),
    #         data={
    #             "sensor-name": self.test_sensor["name"],
    #             "field-name": [""],
    #             "field-type": [self.test_sensor[self.field_name_1]["field_type"]],
    #             "field-unit": [self.test_sensor[self.field_name_1]["field_unit"]],
    #         },
    #     )

    #     # Check that POST redirects to sensor (same page reloads)
    #     self.assertEqual(200, response.status_code)

    # # Sensor name already in use - new AGSensor object not created
    # def test_ConfigureSensorView_invalid_POST_sensor_name_taken_no_object_created(self):
    #     sensor_format = {
    #         self.field_name_1: {
    #             "unit": self.test_sensor[self.field_name_1]["field_type"],
    #             "format": self.test_sensor[self.field_name_1]["field_unit"],
    #         }
    #     }

    #     AGSensor.objects.create(
    #         sensor_name=self.test_sensor["name"], sensor_format=sensor_format
    #     )

    #     # Login
    #     self._get_with_event_code(self.sensor_url, self.TESTCODE)

    #     # POST sensor data
    #     self.client.post(
    #         reverse(self.sensor_url),
    #         data={
    #             "sensor-name": self.test_sensor["name"],
    #             "field-name": [""],
    #             "field-type": [self.test_sensor[self.field_name_1]["field_type"]],
    #             "field-unit": [self.test_sensor[self.field_name_1]["field_unit"]],
    #         },
    #     )

    #     # Check that additional AGSensor object is not created in db
    #     sensors = AGSensor.objects.all()
    #     self.assertEqual(sensors.count(), 1)
