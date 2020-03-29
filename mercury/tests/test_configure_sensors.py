from django.test import TestCase
from django.urls import reverse
from mercury.models import EventCodeAccess
from ag_data.models import AGSensor, AGSensorType


class TestConfigureSensorView(TestCase):
    TESTCODE = "testcode"

    login_url = "mercury:EventAccess"
    sensor_url = "mercury:sensor"
    delete_sensor_url = "mercury:delete_sensor"
    delete_sensor_type_url = "mercury:delete_sensor_type"
    update_sensor_url = "mercury:update_sensor"
    update_sensor_type_url = "mercury:update_type"

    test_type_object_name = "live-feed"
    field_name_1 = "test-field-1"
    field_name_2 = "test-field-2"
    data_type_1 = "test-data-type-1"
    data_type_2 = "test-data-type-2"
    unit_1 = "test-unit-1"
    unit_2 = "test-unit-2"

    test_sensor_object_name = "test-sensor-object"

    updated_sensor_name = "UPDATED_sensor_success"
    updated_sensor_type_name = "UPDATED_sensor_type_success"

    updated_field_name = "UPDATED_field_success"
    updated_data_type = "UPDATED_data_type_success"
    updated_unit = "UPDATED_unit_success"

    test_sensor_update_object_name = "update_sensor"
    test_type_update_object_name = "update_type"

    test_sensor = {
        "name": "wind speed sensor",
        "type_id": test_type_object_name,
    }

    test_sensor_type = {
        "type-name": "fuel level",
        "processing formula": 0,
        "field-names": ["test-field-1", "test-field-2"],
        "data-types": ["test-data-type-1", "test-data-type-2"],
        "units": ["test-unit-1", "test-unit-2"],
    }

    def setUp(self):
        test_code = EventCodeAccess(event_code="testcode", enabled=True)
        test_code.save()

        # Create test objects to compare to later

        test_type_object = AGSensorType.objects.create(
            name=self.test_type_object_name,
            processing_formula=0,
            format={
                self.field_name_1: {
                    "data_type": self.data_type_1,
                    "unit": self.unit_1,
                },
                self.field_name_2: {
                    "data_type": self.data_type_1,
                    "unit": self.unit_1,
                },
            },
        )
        test_type_object.save()

        test_sensor_object = AGSensor.objects.create(
            name=self.test_sensor_object_name, type_id=test_type_object
        )
        test_sensor_object.save()

        test_type_update_object = AGSensorType.objects.create(
            name=self.test_type_update_object_name,
            processing_formula=0,
            format={
                self.field_name_1: {
                    "data_type": self.data_type_1,
                    "unit": self.unit_1,
                },
                self.field_name_2: {
                    "data_type": self.data_type_1,
                    "unit": self.unit_1,
                },
            },
        )

        test_type_update_object.save()
        test_sensor_update_object = AGSensor.objects.create(
            name=self.test_sensor_update_object_name, type_id=test_type_object
        )
        test_sensor_update_object.save()

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
        self.assertEqual(sensors.count(), 3)

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
        sensor = sensors[2]
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
        self.assertEqual(sensor_types.count(), 3)

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
        sensor_type = sensor_types[2]
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

        # Check that AGSensor object is not created in db
        sensors = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 2)

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
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # POST sensor data
        self.client.post(
            reverse(self.sensor_url),
            data={
                "submit_new_sensor": "",
                "sensor-name": self.test_sensor_object_name,
                "select-sensor-type": self.test_sensor["type_id"],
            },
        )

        # Check that additional AGSensor object is not created in db
        sensors = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 2)

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

        # Check that AGSensor object is not created in db
        sensors = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 2)

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

        # Check that AGSensor object is not created in db
        sensors = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 2)

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

        # Check that AGSensor object is not created in db
        sensors = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 2)

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

        # Check that AGSensor object is not created in db
        sensors = AGSensor.objects.all()
        self.assertEqual(sensors.count(), 2)

    # Valid DELETE attempts

    def test_configure_sensor_valid_DELETE_sensor_success_status_ok(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # DELETE sensor
        sensor_to_delete = AGSensor.objects.get(name=self.test_sensor_object_name)
        response = self.client.post(
            reverse(self.delete_sensor_url, kwargs={"sensor_id": sensor_to_delete.id}),
            follow=True,
        )

        # Check that EDIT redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    def test_configure_sensor_valid_DELETE_sensor_success_sensor_deleted(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # DELETE sensor
        sensor_to_delete = AGSensor.objects.get(name=self.test_sensor_object_name)
        self.client.post(
            reverse(self.delete_sensor_url, kwargs={"sensor_id": sensor_to_delete.id}),
            follow=True,
        )

        # Check that sensor is deleted from database
        sensors = AGSensor.objects.all()
        self.assertEqual(1, sensors.count())

    def test_configure_sensor_valid_DELETE_sensor_type_success_status_ok(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # DELETE sensor
        sensor_type_to_delete = AGSensorType.objects.get(
            name=self.test_type_object_name
        )
        response = self.client.post(
            reverse(
                self.delete_sensor_type_url,
                kwargs={"type_id": sensor_type_to_delete.id},
            ),
            follow=True,
        )

        # Check that EDIT redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    def test_configure_sensor_valid_DELETE_sensor_type_success_sensor_type_deleted(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # DELETE sensor
        sensor_type_to_delete = AGSensorType.objects.get(
            name=self.test_type_object_name
        )
        self.client.post(
            reverse(
                self.delete_sensor_type_url,
                kwargs={"type_id": sensor_type_to_delete.id},
            ),
            follow=True,
        )

        # Check that sensor is deleted from database
        sensor_types = AGSensorType.objects.all()
        self.assertEqual(1, sensor_types.count())

    # Invalid DELETE attempts

    def test_configure_sensor_invalid_DELETE_sensor_no_matching_id_status_ok(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # DELETE sensor
        response = self.client.post(
            reverse(self.delete_sensor_url, kwargs={"sensor_id": 99999999999999999}),
            follow=True,
        )

        # Check that EDIT redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    def test_configure_sensor_invalid_DELETE_sensor_no_matching_id_not_deleted(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # DELETE sensor
        self.client.post(
            reverse(self.delete_sensor_url, kwargs={"sensor_id": 99999999999999999}),
            follow=True,
        )

        # Check that sensor is not deleted from database
        sensors = AGSensor.objects.all()
        self.assertEqual(2, sensors.count())

    def test_configure_sensor_invalid_DELETE_sensor_type_no_matching_id_status_ok(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # DELETE sensor
        response = self.client.post(
            reverse(self.delete_sensor_type_url, kwargs={"type_id": 99999999999999999}),
            follow=True,
        )

        # Check that EDIT redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    def test_configure_sensor_invalid_DELETE_sensor_type_no_matching_id_not_deleted(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # DELETE sensor
        self.client.post(
            reverse(self.delete_sensor_type_url, kwargs={"type_id": 99999999999999999}),
            follow=True,
        )

        # Check that sensor is not deleted from database
        sensor_types = AGSensorType.objects.all()
        self.assertEqual(2, sensor_types.count())

    # Valid UPDATE Attempts

    def test_configure_sensor_valid_UPDATE_sensor_name_success_status_ok(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_to_edit = AGSensor.objects.get(name=self.test_sensor_object_name)
        response = self.client.post(
            reverse(self.update_sensor_url, kwargs={"sensor_id": sensor_to_edit.id}),
            data={"edit-sensor-name": self.updated_sensor_name},
            follow=True,
        )

        # Check that UPDATE redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    def test_configure_sensor_valid_UPDATE_sensor_name_success_valid_params(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_to_update = AGSensor.objects.get(name=self.test_sensor_object_name)
        self.client.post(
            reverse(self.update_sensor_url, kwargs={"sensor_id": sensor_to_update.id}),
            data={"edit-sensor-name": self.updated_sensor_name},
            follow=True,
        )
        updated_sensor = AGSensor.objects.get(name=self.updated_sensor_name.lower())

        # Check that updated name goes through
        self.assertEqual(updated_sensor.name, self.updated_sensor_name.lower())

    def test_configure_sensor_valid_UPDATE_sensor_type_name_success_status_ok(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(name=self.test_type_object_name)
        response = self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.updated_sensor_type_name,
                "edit-field-names": [
                    self.field_name_1,
                    self.field_name_2,
                ],  # stays the same
                "edit-data-types": [
                    self.data_type_1,
                    self.data_type_2,
                ],  # stays the same
                "edit-units": [self.unit_1, self.unit_2],  # stays the same
            },
            follow=True,
        )

        # Check that UPDATE redirects to sensor type (same page reloads)
        self.assertEqual(200, response.status_code)

    def test_configure_sensor_valid_UPDATE_sensor_type_name_success_valid_params(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(name=self.test_type_object_name)
        self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.updated_sensor_type_name,
                "edit-field-names": [
                    self.field_name_1,
                    self.field_name_2,
                ],  # stays the same
                "edit-data-types": [
                    self.data_type_1,
                    self.data_type_2,
                ],  # stays the same
                "edit-units": [self.unit_1, self.unit_2],  # stays the same
            },
            follow=True,
        )

        # Check that name was updated successfuly
        updated_sensor_type = AGSensorType.objects.get(
            name=self.updated_sensor_type_name.lower()
        )
        self.assertEqual(
            updated_sensor_type.name, self.updated_sensor_type_name.lower()
        )

    def test_configure_sensor_valid_UPDATE_sensor_type_field_name_success_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(name=self.test_type_object_name)
        response = self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.test_type_object_name,  # stays the same
                "edit-field-names": [self.updated_field_name, self.field_name_2],
                "edit-data-types": [
                    self.data_type_1,
                    self.data_type_2,
                ],  # stays the same
                "edit-units": [self.unit_1, self.unit_2],  # stays the same
            },
            follow=True,
        )

        # Check that UPDATE redirects to sensor type (same page reloads)
        self.assertEqual(200, response.status_code)

    def test_configure_sensor_valid_UPDATE_sensor_type_field_name_success_valid_params(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(name=self.test_type_object_name)
        self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.test_type_object_name,  # stays the same
                "edit-field-names": [self.updated_field_name, self.field_name_2],
                "edit-data-types": [
                    self.data_type_1,
                    self.data_type_2,
                ],  # stays the same
                "edit-units": [self.unit_1, self.unit_2],  # stays the same
            },
            follow=True,
        )

        # Check that field name was properly edited
        updated_sensor_type = AGSensorType.objects.get(name=self.test_type_object_name)
        self.assertTrue(self.updated_field_name.lower() in updated_sensor_type.format)
        self.assertEqual(
            updated_sensor_type.format[self.updated_field_name.lower()]["data_type"],
            self.data_type_1,
        )

    def test_configure_sensor_valid_UPDATE_sensor_type_data_type_success_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(name=self.test_type_object_name)
        response = self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.test_type_object_name,  # stays the same
                "edit-field-names": [
                    self.field_name_1,
                    self.field_name_2,
                ],  # stays the same
                "edit-data-types": [self.updated_data_type, self.data_type_2],
                "edit-units": [self.unit_1, self.unit_2],  # stays the same
            },
            follow=True,
        )

        # Check that UPDATE redirects to sensor type (same page reloads)
        self.assertEqual(200, response.status_code)

    def test_configure_sensor_valid_UPDATE_sensor_type_data_type_success_valid_params(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(name=self.test_type_object_name)
        self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.test_type_object_name,  # stays the same
                "edit-field-names": [
                    self.field_name_1,
                    self.field_name_2,
                ],  # stays the same
                "edit-data-types": [self.updated_data_type, self.data_type_2],
                "edit-units": [self.unit_1, self.unit_2],  # stays the same
            },
            follow=True,
        )

        # Check that field name was properly edited
        updated_sensor_type = AGSensorType.objects.get(name=self.test_type_object_name)
        self.assertEqual(
            self.updated_data_type,
            updated_sensor_type.format[self.field_name_1]["data_type"],
        )

    def test_configure_sensor_valid_UPDATE_sensor_type_unit_success_status_ok(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(name=self.test_type_object_name)
        response = self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.test_type_object_name,  # stays the same
                "edit-field-names": [
                    self.field_name_1,
                    self.field_name_2,
                ],  # stays the same
                "edit-data-types": [
                    self.data_type_1,
                    self.data_type_2,
                ],  # stays the same
                "edit-units": [self.updated_unit, self.unit_2],
            },
            follow=True,
        )

        # Check that UPDATE redirects to sensor type (same page reloads)
        self.assertEqual(200, response.status_code)

    def test_configure_sensor_valid_UPDATE_sensor_type_unit_success_valid_params(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(name=self.test_type_object_name)
        self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.test_type_object_name,  # stays the same
                "edit-field-names": [
                    self.field_name_1,
                    self.field_name_2,
                ],  # stays the same
                "edit-data-types": [
                    self.data_type_1,
                    self.data_type_2,
                ],  # stays the same
                "edit-units": [self.updated_unit, self.unit_2],
            },
            follow=True,
        )

        updated_sensor_type = AGSensorType.objects.get(name=self.test_type_object_name)
        self.assertEqual(
            self.updated_unit, updated_sensor_type.format[self.field_name_1]["unit"]
        )

    # Invalid UPDATE attempts

    def test_configure_sensor_valid_UPDATE_sensor_name_failure_name_taken_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_to_edit = AGSensor.objects.get(name=self.test_sensor_update_object_name)
        response = self.client.post(
            reverse(self.update_sensor_url, kwargs={"sensor_id": sensor_to_edit.id}),
            data={"edit-sensor-name": self.test_sensor_object_name},
            follow=True,
        )

        # Check that UPDATE redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    def test_configure_sensor_valid_UPDATE_sensor_name_failure_name_taken_not_updated(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_to_edit = AGSensor.objects.get(name=self.test_sensor_update_object_name)
        self.client.post(
            reverse(self.update_sensor_url, kwargs={"sensor_id": sensor_to_edit.id}),
            data={"edit-sensor-name": self.test_sensor_object_name},
            follow=True,
        )

        # Check that the sensor name was not changed
        updated_sensor = AGSensor.objects.get(name=self.test_sensor_update_object_name)
        self.assertEqual(
            updated_sensor.name, self.test_sensor_update_object_name.lower()
        )

    def test_configure_sensor_valid_UPDATE_sensor_name_failure_empty_name_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_to_edit = AGSensor.objects.get(name=self.test_sensor_update_object_name)
        response = self.client.post(
            reverse(self.update_sensor_url, kwargs={"sensor_id": sensor_to_edit.id}),
            data={"edit-sensor-name": ""},
            follow=True,
        )

        # Check that UPDATE redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    def test_configure_sensor_valid_UPDATE_sensor_name_failure_empty_name_not_updated(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_to_edit = AGSensor.objects.get(name=self.test_sensor_update_object_name)
        self.client.post(
            reverse(self.update_sensor_url, kwargs={"sensor_id": sensor_to_edit.id}),
            data={"edit-sensor-name": ""},
            follow=True,
        )

        # Check that the sensor name was not changed
        updated_sensor = AGSensor.objects.get(name=self.test_sensor_update_object_name)
        self.assertEqual(
            updated_sensor.name, self.test_sensor_update_object_name.lower()
        )

    def test_configure_sensor_valid_UPDATE_sensor_type_failure_name_taken_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        response = self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.test_type_object_name,
                "edit-field-names": [self.field_name_1, self.field_name_2],
                "edit-data-types": [self.data_type_1, self.data_type_2],
                "edit-units": [self.unit_1, self.unit_2],
            },
            follow=True,
        )

        # Check that UPDATE redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    def test_configure_sensor_valid_UPDATE_sensor_type_failure_name_taken_not_updated(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.test_type_object_name,
                "edit-field-names": [self.field_name_1, self.field_name_2],
                "edit-data-types": [self.data_type_1, self.data_type_2],
                "edit-units": [self.unit_1, self.unit_2],
            },
            follow=True,
        )

        # Check that the name was not updated
        updated_sensor_type = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        self.assertEqual(updated_sensor_type.name, self.test_type_update_object_name)

    def test_configure_sensor_valid_UPDATE_sensor_type_failure_name_empty_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        response = self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": "",
                "edit-field-names": [self.field_name_1, self.field_name_2],
                "edit-data-types": [self.data_type_1, self.data_type_2],
                "edit-units": [self.unit_1, self.unit_2],
            },
            follow=True,
        )

        # Check that UPDATE redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    def test_configure_sensor_valid_UPDATE_sensor_type_failure_name_empty_not_updated(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": "",
                "edit-field-names": [self.field_name_1, self.field_name_2],
                "edit-data-types": [self.data_type_1, self.data_type_2],
                "edit-units": [self.unit_1, self.unit_2],
            },
            follow=True,
        )

        # Check that the name was not updated
        updated_sensor_type = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        self.assertEqual(updated_sensor_type.name, self.test_type_update_object_name)

    def test_configure_sensor_valid_UPDATE_sensor_type_failure_field_name_taken_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        response = self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.test_type_object_name,
                "edit-field-names": [self.field_name_2, self.field_name_2],
                "edit-data-types": [self.data_type_1, self.data_type_2],
                "edit-units": [self.unit_1, self.unit_2],
            },
            follow=True,
        )

        # Check that UPDATE redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    def test_configure_sensor_valid_UPDATE_sensor_type_failure_field_name_taken_not_updated(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.test_type_object_name,
                "edit-field-names": [self.field_name_2, self.field_name_2],
                "edit-data-types": [self.data_type_1, self.data_type_2],
                "edit-units": [self.unit_1, self.unit_2],
            },
            follow=True,
        )

        # Check that the name was not updated
        updated_sensor_type = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        self.assertTrue(self.field_name_1 in updated_sensor_type.format)
        self.assertEqual(
            updated_sensor_type.format[self.field_name_1]["data_type"], self.data_type_1
        )

    def test_configure_sensor_valid_UPDATE_sensor_type_failure_field_name_empty_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        response = self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.test_type_object_name,
                "edit-field-names": ["", self.field_name_2],
                "edit-data-types": [self.data_type_1, self.data_type_2],
                "edit-units": [self.unit_1, self.unit_2],
            },
            follow=True,
        )

        # Check that UPDATE redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    def test_configure_sensor_valid_UPDATE_sensor_type_fail_field_name_empty_not_updated(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.test_type_object_name,
                "edit-field-names": ["", self.field_name_2],
                "edit-data-types": [self.data_type_1, self.data_type_2],
                "edit-units": [self.unit_1, self.unit_2],
            },
            follow=True,
        )

        # Check that the name was not updated
        updated_sensor_type = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        self.assertTrue(self.field_name_1 in updated_sensor_type.format)
        self.assertEqual(
            updated_sensor_type.format[self.field_name_1]["data_type"], self.data_type_1
        )

    def test_configure_sensor_valid_UPDATE_sensor_type_failure_data_type_empty_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        response = self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.test_type_object_name,
                "edit-field-names": [self.field_name_1, self.field_name_2],
                "edit-data-types": ["", self.data_type_2],
                "edit-units": [self.unit_1, self.unit_2],
            },
            follow=True,
        )

        # Check that UPDATE redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    def test_configure_sensor_valid_UPDATE_sensor_type_failure_data_type_empty_not_updated(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.test_type_object_name,
                "edit-field-names": [self.field_name_1, self.field_name_2],
                "edit-data-types": ["", self.data_type_2],
                "edit-units": [self.unit_1, self.unit_2],
            },
            follow=True,
        )

        # Check that the name was not updated
        updated_sensor_type = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        self.assertTrue(self.field_name_1 in updated_sensor_type.format)
        self.assertEqual(
            updated_sensor_type.format[self.field_name_1]["data_type"], self.data_type_1
        )

    def test_configure_sensor_valid_UPDATE_sensor_type_failure_unit_empty_status_ok(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        response = self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.test_type_object_name,
                "edit-field-names": [self.field_name_1, self.field_name_2],
                "edit-data-types": [self.data_type_1, self.data_type_2],
                "edit-units": ["", self.unit_2],
            },
            follow=True,
        )

        # Check that UPDATE redirects to sensor (same page reloads)
        self.assertEqual(200, response.status_code)

    def test_configure_sensor_valid_UPDATE_sensor_type_failure_unit_name_empty_not_updated(
        self,
    ):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # EDIT sensor
        sensor_type_to_edit = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        self.client.post(
            reverse(
                self.update_sensor_type_url, kwargs={"type_id": sensor_type_to_edit.id}
            ),
            data={
                "edit-type-name": self.test_type_object_name,
                "edit-field-names": [self.field_name_1, self.field_name_2],
                "edit-data-types": [self.data_type_1, self.data_type_2],
                "edit-units": ["", self.unit_2],
            },
            follow=True,
        )

        # Check that the name was not updated
        updated_sensor_type = AGSensorType.objects.get(
            name=self.test_type_update_object_name
        )
        self.assertTrue(self.field_name_1 in updated_sensor_type.format)
        self.assertEqual(
            updated_sensor_type.format[self.field_name_1]["unit"], self.unit_1
        )
