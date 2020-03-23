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
        self.field_name_1 = "test-field-1"
        self.field_name_2 = "test-field-2"
        self.test_type_object_name = "live-feed"
        test_type_object = AGSensorType.objects.create(
            name=self.test_type_object_name,
            processing_formula=0,
            format={
                self.field_name_1: {
                    "data_type": "test-data-type-1",
                    "unit": "test-unit-1",
                },
                self.field_name_2: {
                    "data_type": "test-data-type-2",
                    "unit": "test-unit-2",
                },
            },
        )
        test_type_object.save()

        self.test_sensor = {
            "name": "wind speed sensor",
            "type_id": self.test_type_object_name,
        }

        self.test_sensor_type = {
            "type-name": "fuel level",
            "processing formula": 0,
            "field-names": ["test-field-1", "test-field-2"],
            "data-types": ["test-data-type-1", "test-data-type-2"],
            "units": ["test-unit-1", "test-unit-2"],
        }

    def _get_with_event_code(self, url, event_code):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": event_code})
        response = self.client.get(reverse(url))
        session = self.client.session
        return response, session

    def test_configure_sensor_view_get_success(self):
        response, session = self._get_with_event_code(self.sensor_url, self.TESTCODE)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])

    # Valid POST tests

    # Valid POST to create sensor returns status OK
    def test_configure_sensor_valid_POST_sensor_returns_status_ok(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": self.test_sensor["name"],
                "select-sensor-type": self.test_sensor["type_id"],
            },
        )

        # Check that POST redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    # Valid POST creates new AGSensor object
    def test_configure_sensor_valid_post_sensor_success_object_created(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST good sensor data
        self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": self.test_sensor["name"],
                "select-sensor-type": self.test_sensor["type_id"],
            },
        )

        # Check that AGSensor object is created in db with expected params
        sensors = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 1)

    # Valid POST creates new AGSensor object with expected parameters
    def test_configure_sensor_valid_post_sensor_object_created_with_correct_params(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": self.test_sensor["name"],
                "select-sensor-type": self.test_sensor["type_id"],
            },
        )

        # Check that AGSensor object is created in db with expected values
        sensors = AGSensor.objects.all()
        sensor = sensors[0]
        self.assertEqual(sensor.name, self.test_sensor["name"])
        self.assertEqual(sensor.type_id.name, self.test_sensor["type_id"])

    # Valid POST to create AGSensorType returns status OK
    def test_configure_sensor_valid_post_sensor_type_returns_status_ok(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor type data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_type": "",
                "type-name": self.test_sensor_type["type-name"],
                "field-names": self.test_sensor_type["field-names"],
                "data-types": self.test_sensor_type["data-types"],
                "units": self.test_sensor_type["units"],
            },
        )

        # Check that POST redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    # Valid POST creates new AGSensorType object
    def test_configure_sensor_valid_post_sensor_type_success_object_created(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST good sensor type data
        self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_type": "",
                "type-name": self.test_sensor_type["type-name"],
                "field-names": self.test_sensor_type["field-names"],
                "data-types": self.test_sensor_type["data-types"],
                "units": self.test_sensor_type["units"],
            },
        )

        # Check that AGSensor object is created in db with expected params
        sensor_types = AGSensorType.objects.all()
        self.assertEqual(
            sensor_types.count(), 2
        )  # not 1 since we created a sensor_type in the setUp() function

    def test_configure_sensor_valid_post_sensor_type_object_created_with_correct_params(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_type": "",
                "type-name": self.test_sensor_type["type-name"],
                "field-names": self.test_sensor_type["field-names"],
                "data-types": self.test_sensor_type["data-types"],
                "units": self.test_sensor_type["units"],
            },
        )

        # Check that AGSensor object is created in db with expected values
        sensor_types = AGSensorType.objects.all()
        sensor_type = sensor_types[1]
        self.assertEqual(sensor_type.name, self.test_sensor_type["type-name"])
        self.assertTrue(self.test_sensor_type["field-names"][0] in sensor_type.format)
        self.assertTrue(self.test_sensor_type["field-names"][1] in sensor_type.format)
        self.assertEqual(
            sensor_type.format[self.field_name_1]["data_type"],
            self.test_sensor_type["data-types"][0],
        )
        self.assertEqual(
            sensor_type.format[self.field_name_2]["data_type"],
            self.test_sensor_type["data-types"][1],
        )
        self.assertEqual(
            sensor_type.format[self.field_name_1]["unit"],
            self.test_sensor_type["units"][0],
        )
        self.assertEqual(
            sensor_type.format[self.field_name_2]["unit"],
            self.test_sensor_type["units"][1],
        )

    # # Invalid POST tests

    # Duplicate field names still returns status ok
    def test_configure_sensor_invalid_post_sensor_no_name_returns_status_ok(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": "",
                "select-sensor-type": self.test_sensor["type_id"],
            },
        )

        # Check that POST redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    # Duplicate field names - no AGSensor object created
    def test_configure_sensor_invalid_POST_sensor_no_name_no_object_created(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data with duplicate field names
        self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": "",
                "select-sensor-type": self.test_sensor["type_id"],
            },
        )

        # Check that AGSensor object is created in db with expected params
        sensors = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 0)

    # Sensor name already in use - still returns status OK
    def test_configure_sensor_view_invalid_post_sensor_name_taken_status_ok(self):
        AGSensor.objects.create(
            name=self.test_sensor["name"],
            type_id=AGSensorType.objects.get(name=self.test_type_object_name),
        )

        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": self.test_sensor["name"],
                "select-sensor-type": self.test_sensor["type_id"],
            },
        )

        # Check that POST redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    # Sensor name already in use - new AGSensor object not created
    def test_configure_sensor_invalid_POST_sensor_name_taken_no_object_created(self):
        AGSensor.objects.create(
            name=self.test_sensor["name"],
            type_id=AGSensorType.objects.get(name=self.test_type_object_name),
        )

        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": self.test_sensor["name"],
                "select-sensor-type": self.test_sensor["type_id"],
            },
        )

        # Check that additional AGSensor object is not created in db
        sensors = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 1)

    # Sensor type name missing still returns status OK
    def test_configure_sensor_invalid_POST_sensor_type_name_missing_status_ok(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_type": "",
                "type-name": "",
                "field-names": self.test_sensor_type["field-names"],
                "data-types": self.test_sensor_type["data-types"],
                "units": self.test_sensor_type["units"],
            },
        )

        # Check that POST redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    # Sensor type name missing - no AGSensorType object created
    def test_configure_sensor_bad_post_sensor_type_name_missing_no_object_created(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_type": "",
                "type-name": "",
                "field-names": self.test_sensor_type["field-names"],
                "data-types": self.test_sensor_type["data-types"],
                "units": self.test_sensor_type["units"],
            },
        )

        # Check that AGSensor object is created in db with expected params
        sensors = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 0)

    # Field name missing still returns status OK
    def test_configure_sensor_view_invalid_post_sensor_type_field_name_missing_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_type": "",
                "type-name": self.test_sensor_type["type-name"],
                "field-names": [self.field_name_1],
                "data-types": self.test_sensor_type["data-types"],
                "units": self.test_sensor_type["units"],
            },
        )

        # Check that POST redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    # Field name missing - no AGSensorType object created
    def test_configure_sensor_bad_post_sensor_type_field_name_missing_no_object_created(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_type": "",
                "type-name": self.test_sensor_type["type-name"],
                "field-names": [self.field_name_1],
                "data-types": self.test_sensor_type["data-types"],
                "units": self.test_sensor_type["units"],
            },
        )

        # Check that AGSensor object is created in db with expected params
        sensors = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 0)

    # AGSensorType name taken returns status OK
    def test_configure_sensor_invalid_post_sensor_type_name_taken_status_ok(self,):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_type": "",
                "type-name": self.test_type_object_name,
                # AGSensorType created in setUp()
                "field-names": self.test_sensor_type["field-names"],
                "data-types": self.test_sensor_type["data-types"],
                "units": self.test_sensor_type["units"],
            },
        )

        # Check that POST redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    # AGSensorType name taken - no AGSensorType object created
    def test_configure_sensor_view_invalid_post_sensor_type_name_taken_no_object_created(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_type": "",
                "type-name": self.test_type_object_name,
                # AGSensorType created in setUp()
                "field-names": self.test_sensor_type["field-names"],
                "data-types": self.test_sensor_type["data-types"],
                "units": self.test_sensor_type["units"],
            },
        )

        # Check that AGSensor object is created in db with expected params
        sensors = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 0)

    # AGSensorType duplicated field name returns status OK
    def test_configure_sensor_bad_post_sensor_type_dup_field_name_missing_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        response = self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_type": "",
                "type-name": self.test_sensor_type["type-name"],
                "field-names": [self.field_name_1, self.field_name_1],
                "data-types": self.test_sensor_type["data-types"],
                "units": self.test_sensor_type["units"],
            },
        )

        # Check that POST redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    # AGSensorType duplicated field name - no AGSensorType object created
    def test_configure_sensor_bad_post_sensor_type_dup_field_name_no_object_created(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_type": "",
                "type-name": self.test_sensor_type["type-name"],
                "field-names": [self.field_name_1, self.field_name_1],
                "data-types": self.test_sensor_type["data-types"],
                "units": self.test_sensor_type["units"],
            },
        )

        # Check that AGSensor object is created in db with expected params
        sensors = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 0)
