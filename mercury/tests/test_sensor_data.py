from django.test import TestCase
from django.urls import reverse
from mercury.models import EventCodeAccess
from ag_data.models import AGSensor, AGSensorType, AGMeasurement, AGEvent, AGVenue
import datetime
import uuid


class TestSensorDataExistsView(TestCase):

    login_url = "mercury:login"
    sensor_exists_url = "mercury:sensor_data_exists"
    TESTCODE = "testcode"

    event_name = "foo"

    test_sensor_name = "Wind Sensor"
    test_sensor_type = "Dual wind"

    test_sensor_format = {
        "left_gust": {"unit": "km/h", "format": "float"},
        "right_gust": {"unit": "km/h", "format": "float"},
    }

    test_event_data = {
        "name": "Sunny Day Test Drive",
        "date": datetime.datetime(2020, 2, 2, 20, 21, 22),
        "description": "A very progressive test run at \
                        Sunnyside Daycare's Butterfly Room.",
        "location": "New York, NY",
    }

    test_venue_data = {
        "name": "Venue 1",
        "description": "foo",
        "latitude": 100,
        "longitude": 200,
    }

    # Returns event
    def create_venue_and_event(self, event_name):
        venue = AGVenue.objects.create(
            name=self.test_venue_data["name"],
            description=self.test_venue_data["description"],
            latitude=self.test_venue_data["latitude"],
            longitude=self.test_venue_data["longitude"],
        )
        venue.save()

        event = AGEvent.objects.create(
            name=event_name,
            date=self.test_event_data["date"],
            description=self.test_event_data["description"],
            venue_uuid=venue,
        )
        event.save()

        return event

    def _get_with_event_code(self, url, event_code, kwargs):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": event_code})
        response = self.client.get(reverse(url, kwargs=kwargs))
        session = self.client.session
        return response, session

    def setUp(self):
        self.login_url = "mercury:EventAccess"
        self.sensor_url = "mercury:sensor"
        self.sensor_data_exists_url = "mercury:sensor_data_exists"
        self.event_data_exists_url = "mercury:event_data_exists"
        test_code = EventCodeAccess(event_code="testcode", enabled=True)
        test_code.save()

    def test_sensor_data_exists_no_measurements_for_sensor(self):
        # Create a sensor type and sensor
        sensor_type = AGSensorType.objects.create(
            name=self.test_sensor_type,
            processing_formula=0,
            format=self.test_sensor_format,
        )
        sensor_type.save()
        sensor = AGSensor.objects.create(
            name=self.test_sensor_name, type_id=sensor_type
        )
        sensor.save()

        kwargs = {"sensor_id": sensor.uuid}
        self._get_with_event_code(self.sensor_data_exists_url, self.TESTCODE, kwargs)

        # Create an event and venue
        self.create_venue_and_event(self.event_name)

        response = self.client.get(
            reverse(self.sensor_data_exists_url, kwargs={"sensor_id": sensor.uuid})
        )

        self.assertEquals(response.json()["status"], False)

    def test_sensor_data_exists_measurement_exists(self):
        # Create a sensor type and sensor
        sensor_type = AGSensorType.objects.create(
            name=self.test_sensor_type,
            processing_formula=0,
            format=self.test_sensor_format,
        )
        sensor_type.save()
        sensor = AGSensor.objects.create(
            name=self.test_sensor_name, type_id=sensor_type
        )
        sensor.save()

        kwargs = {"sensor_id": sensor.uuid}
        self._get_with_event_code(self.sensor_data_exists_url, self.TESTCODE, kwargs)

        # Create an event and venue
        event = self.create_venue_and_event(self.event_name)

        data = AGMeasurement.objects.create(
            event_uuid=event,
            sensor_id=sensor,
            timestamp=datetime.datetime(2020, 2, 2, 20, 21, 22),
            value={"left_gust": 10, "right_gust": 10},
        )
        data.save()

        response = self.client.get(
            reverse(self.sensor_data_exists_url, kwargs={"sensor_id": sensor.uuid})
        )

        self.assertEquals(response.json()["status"], True)

    def test_sensor_data_sensor_id_not_found(self):
        bad_id = uuid.uuid4()

        kwargs = {"sensor_id": bad_id}
        response, session = self._get_with_event_code(
            self.sensor_data_exists_url, self.TESTCODE, kwargs
        )

        self.assertEquals(response.json()["status"], False)

    def test_event_data_exists_no_measurements(self):
        # Create a sensor type and sensor
        sensor_type = AGSensorType.objects.create(
            name=self.test_sensor_type,
            processing_formula=0,
            format=self.test_sensor_format,
        )
        sensor_type.save()
        sensor = AGSensor.objects.create(
            name=self.test_sensor_name, type_id=sensor_type
        )
        sensor.save()

        kwargs = {"sensor_id": sensor.id}
        self._get_with_event_code(self.sensor_data_exists_url, self.TESTCODE, kwargs)

        # Create an event and venue
        event = self.create_venue_and_event(self.event_name)

        response = self.client.get(
            reverse(self.event_data_exists_url, kwargs={"event_uuid": event.uuid})
        )

        self.assertEquals(response.json()["status"], False)

    def test_event_data_exists_measurement_exists(self):
        # Create a sensor type and sensor
        sensor_type = AGSensorType.objects.create(
            name=self.test_sensor_type,
            processing_formula=0,
            format=self.test_sensor_format,
        )
        sensor_type.save()
        sensor = AGSensor.objects.create(
            name=self.test_sensor_name, type_id=sensor_type
        )
        sensor.save()

        kwargs = {"sensor_id": sensor.id}
        self._get_with_event_code(self.sensor_data_exists_url, self.TESTCODE, kwargs)

        # Create an event and venue
        event = self.create_venue_and_event(self.event_name)

        data = AGMeasurement.objects.create(
            event_uuid=event,
            sensor_id=sensor,
            timestamp=datetime.datetime(2020, 2, 2, 20, 21, 22),
            value={"left_gust": 10, "right_gust": 10},
        )
        data.save()

        response = self.client.get(
            reverse(self.event_data_exists_url, kwargs={"event_uuid": event.uuid})
        )

        self.assertEquals(response.json()["status"], True)

    def test_event_data_event_uuid_not_found(self):
        bad_id = "ade30a1f-d1df-4970-b02f-234a6187e3a5"

        kwargs = {"event_uuid": bad_id}
        response, session = self._get_with_event_code(
            self.event_data_exists_url, self.TESTCODE, kwargs
        )

        self.assertEquals(response.json()["status"], False)
