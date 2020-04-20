from django.test import TestCase
from django.urls import reverse
from mercury.models import EventCodeAccess
from ag_data.models import AGEvent, AGVenue, AGSensor, AGSensorType, AGMeasurement, AGActiveEvent
import datetime


class TestEventView(TestCase):
    TESTCODE = "testcode"

    test_event_data = {
        "name": "Sunny Day Test Drive",
        "date": datetime.datetime(2020, 2, 2, 20, 21, 22),
        "description": "A very progressive test run at \
                Sunnyside Daycare's Butterfly Room.",
        "location": "New York, NY",
    }

    test_event_data_update = {
        "name": "Another Day Test Drive",
        "date": datetime.datetime(2020, 3, 3, 20, 21, 22),
        "description": "A very modern test run at \
                    my backyard.",
        "location": "Buffalo, NY",
    }

    test_venue_data = {
        "name": "Venue 1",
        "description": "foo",
        "latitude": 100,
        "longitude": 200,
    }

    test_venue_data_update = {
        "name": "Venue 2",
        "description": "bar",
        "latitude": 200,
        "longitude": 100,
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

    # Returns sensor
    def create_sensor(self):

        sensor_type = AGSensorType.objects.create(
            name="test",
            format={"lefts": {"data_type": "test", "unit": "test",},},  # noqa
        )

        sensor = AGSensor.objects.create(name="test", type_id=sensor_type,)

        return sensor

    # Returns measurement
    def create_measurement(self, event, sensor):

        measurement = AGMeasurement.objects.create(
            event_uuid=event, sensor_id=sensor, value={"lefts": 30},
        )

        return measurement

    def setUp(self):
        self.login_url = "mercury:EventAccess"
        self.event_url = "mercury:events"
        self.event_delete_url = "mercury:delete_event"
        self.event_update_url = "mercury:update_event"
        self.venue_update_url = "mercury:update_venue"
        self.event_activate_url = "mercury:activate_event"
        self.event_deactivate_url = "mercury:deactivate_event"
        self.event_export_csv_url = "mercury:export_csv"
        self.event_export_all_csv_url = "mercury:export_all_csv"
        self.event_export_json_url = "mercury:export_json"
        self.event_export_all_json_url = "mercury:export_all_json"

        # Create random event name
        self.event_name = "test"

        test_code = EventCodeAccess(event_code=self.TESTCODE, enabled=True)
        test_code.save()

    def _get_with_event_code(self, url, event_code):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": event_code})
        response = self.client.get(reverse(url))
        session = self.client.session
        return response, session

    def post_event_data(self, venue_id):
        response = self.client.post(
            reverse(self.event_url),
            data={
                "submit-event": "",
                "name": self.test_event_data["name"],
                "date": self.test_event_data["date"],
                "description": self.test_event_data["description"],
                "venue_uuid": venue_id,
            },
        )
        return response

    def post_venue_data(self):
        response = self.client.post(
            reverse(self.event_url),
            data={
                "submit-venue": "",
                "name": self.test_venue_data["name"],
                "description": self.test_venue_data["description"],
                "latitude": self.test_venue_data["latitude"],
                "longitude": self.test_venue_data["longitude"],
            },
        )
        return response

    def test_event_view_get_success(self):
        response, session = self._get_with_event_code(self.event_url, self.TESTCODE)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])

    def test_create_venue(self):
        # Login
        self._get_with_event_code(self.event_url, self.TESTCODE)

        response = self.post_venue_data()

        self.assertEqual(200, response.status_code)
        venues = AGVenue.objects.all()
        self.assertTrue(venues.count() > 0)

    def test_create_venue_with_correct_parameters(self):
        # Login
        self._get_with_event_code(self.event_url, self.TESTCODE)

        response = self.post_venue_data()

        self.assertEqual(200, response.status_code)
        venues = AGVenue.objects.all()
        self.assertTrue(venues.count() > 0)

        venue = venues[0]

        self.assertEqual(venue.name, self.test_venue_data["name"])
        self.assertEqual(venue.description, self.test_venue_data["description"])
        self.assertEqual(venue.latitude, self.test_venue_data["latitude"])
        self.assertEqual(venue.longitude, self.test_venue_data["longitude"])

    def test_create_event(self):
        # Login
        self._get_with_event_code(self.event_url, self.TESTCODE)

        venue = AGVenue.objects.create(
            name=self.test_venue_data["name"],
            description=self.test_venue_data["description"],
            latitude=self.test_venue_data["latitude"],
            longitude=self.test_venue_data["longitude"],
        )
        venue.save()

        # POST sensor data
        response = self.post_event_data(venue.uuid)

        self.assertEqual(200, response.status_code)
        events = AGEvent.objects.all()
        self.assertEqual(events.count(), 1)

    def test_create_event_with_correct_parameters(self):
        # Login
        self._get_with_event_code(self.event_url, self.TESTCODE)

        venue = AGVenue.objects.create(
            name=self.test_venue_data["name"],
            description=self.test_venue_data["description"],
            latitude=self.test_venue_data["latitude"],
            longitude=self.test_venue_data["longitude"],
        )
        venue.save()

        # POST sensor data
        response = self.post_event_data(venue.uuid)

        self.assertEqual(200, response.status_code)
        events = AGEvent.objects.all()
        self.assertEqual(events.count(), 1)

        event = events[0]

        self.assertEqual(event.name, self.test_event_data["name"])
        self.assertEqual(event.date, self.test_event_data["date"])
        self.assertEqual(event.venue_uuid.uuid, venue.uuid)
        self.assertEqual(event.description, self.test_event_data["description"])

    def test_delete_event(self):
        # Create an event
        event = self.create_venue_and_event(self.event_name)

        # Confirm that event was created
        self.assertEquals(AGEvent.objects.all().count(), 1)

        # Delete the event
        self.client.post(
            reverse(self.event_delete_url, kwargs={"event_uuid": event.uuid})
        )

        # Confirm that event was deleted
        self.assertEquals(AGEvent.objects.all().count(), 0)

    def test_update_event(self):
        # Create an event
        event = self.create_venue_and_event(self.event_name)

        # Confirm that event was created
        self.assertEquals(AGEvent.objects.all().count(), 1)

        venue_name_update = "test name"

        # Create another venue
        venue = AGVenue.objects.create(
            name=venue_name_update,
            description=self.test_venue_data["description"],
            latitude=self.test_venue_data["latitude"],
            longitude=self.test_venue_data["longitude"],
        )
        venue.save()

        # Update the event
        self.client.post(
            reverse(self.event_update_url, kwargs={"event_uuid": event.uuid}),
            data={
                "name": self.test_event_data_update["name"],
                "venue_uuid": venue.uuid,
                "description": self.test_event_data_update["description"],
            },
        )

        # Confirm that event was updated
        event = AGEvent.objects.all().first()

        self.assertEquals(event.name, self.test_event_data_update["name"])
        self.assertEquals(event.venue_uuid.name, venue_name_update)
        self.assertEquals(event.description, self.test_event_data_update["description"])

    def test_update_venue(self):

        venue_name_update = "test name"
        # Create a venue
        venue = AGVenue.objects.create(
            name=venue_name_update,
            description=self.test_venue_data["description"],
            latitude=self.test_venue_data["latitude"],
            longitude=self.test_venue_data["longitude"],
        )
        venue.save()

        # Confirm that venue was created
        self.assertEquals(AGVenue.objects.all().count(), 1)

        # Update the event
        response = self.client.post(
            reverse(self.venue_update_url, kwargs={"venue_uuid": venue.uuid}),
            data={
                "name": self.test_venue_data_update["name"],
                "description": self.test_venue_data_update["description"],
                "latitude": self.test_venue_data_update["latitude"],
                "longitude": self.test_venue_data_update["longitude"],
            },
        )

        self.assertEqual(302, response.status_code)

        # Confirm that venue was updated
        venue = AGVenue.objects.all().first()

        self.assertEquals(venue.name, self.test_venue_data_update["name"])
        self.assertEquals(venue.description, self.test_venue_data_update["description"])
        self.assertEquals(venue.latitude, self.test_venue_data_update["latitude"])
        self.assertEquals(venue.longitude, self.test_venue_data_update["longitude"])

    def test_export_all_csv(self):
        event = self.create_venue_and_event(self.event_name)
        sensor = self.create_sensor()
        self.create_measurement(event, sensor)

        response = self.client.post(reverse(self.event_export_all_csv_url))

        self.assertEqual(200, response.status_code)

    def test_export_all_json(self):
        event = self.create_venue_and_event(self.event_name)
        sensor = self.create_sensor()
        self.create_measurement(event, sensor)

        response = self.client.post(reverse(self.event_export_all_json_url))

        self.assertEqual(200, response.status_code)

    # def test_export_csv(self):
    #     event = self.create_venue_and_event(self.event_name)
    #     sensor = self.create_sensor()
    #     measurement = self.create_measurement(event, sensor)

    #     response = self.client.post(
    #         reverse(self.event_export_csv_url, kwargs={"event_uuid": event.uuid})
    #     )

    #     self.assertEqual(200, response.status_code)

    def test_export_json(self):
        event = self.create_venue_and_event(self.event_name)
        sensor = self.create_sensor()
        self.create_measurement(event, sensor)

        response = self.client.post(
            reverse(self.event_export_json_url, kwargs={"event_uuid": event.uuid})
        )

        self.assertEqual(200, response.status_code)

    def test_export_no_measurements(self):
        event = self.create_venue_and_event(self.event_name)

        response = self.client.post(
            reverse(self.event_export_csv_url, kwargs={"event_uuid": event.uuid})
        )

        self.assertEqual(302, response.status_code)

    def test_export_all_no_measurements(self):
        self.create_venue_and_event(self.event_name)

        response = self.client.post(reverse(self.event_export_all_csv_url))

        self.assertEqual(200, response.status_code)

    def test_activate_event(self):
        event = self.create_venue_and_event(self.event_name)

        response = self.client.post(
            reverse(self.event_activate_url, kwargs={"event_uuid": event.uuid})
        )

        self.assertEqual(AGActiveEvent.objects.first().agevent, event)
        self.assertEqual(302, response.status_code)

    def test_deactivate_event(self):
        event = self.create_venue_and_event(self.event_name)

        response = self.client.post(
            reverse(self.event_activate_url, kwargs={"event_uuid": event.uuid})
        )

        self.assertEqual(302, response.status_code)

        response = self.client.post(
            reverse(self.event_deactivate_url, kwargs={"event_uuid": event.uuid})
        )

        self.assertEqual(AGActiveEvent.objects.first(), None)
        self.assertEqual(302, response.status_code)
