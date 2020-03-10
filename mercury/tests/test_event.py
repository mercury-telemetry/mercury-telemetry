from django.test import TestCase
import datetime
from django.urls import reverse
from mercury.models import AGEvent, EventCodeAccess
import datetime

class TestEventModel(TestCase):
    # Test value constants that should all work
    TEST_NAME = "test_rockcrawl"
    TEST_EVENT_LOCATION = "test_peoria"
    TEST_COMMENTS = "this is coming from test_event.py"

    def create_simulated_event(self):
        AGEvent.objects.create(
            event_name=self.TEST_NAME,
            event_location=self.TEST_EVENT_LOCATION,
            event_date=datetime.date.today(),
            event_description=self.TEST_COMMENTS,
        )

    def setUp(self):
        self.create_simulated_event()

    def test_event(self):
        foo = AGEvent.objects.get(event_name=self.TEST_NAME)
        self.assertEqual(foo.event_name, self.TEST_NAME)

        foo = AGEvent.objects.get(event_location=self.TEST_EVENT_LOCATION)
        self.assertEqual(foo.event_location, self.TEST_EVENT_LOCATION)

        foo = AGEvent.objects.get(event_description=self.TEST_COMMENTS)
        self.assertEqual(foo.event_description, self.TEST_COMMENTS)


class TestEventView(TestCase):
    TESTCODE = "testcode"

    test_event_data = {
        "name": "Sunny Day Test Drive",
        "date": datetime.datetime(2020, 2, 2, 20, 21, 22),
        "description": "A very progressive test run at \
                Sunnyside Daycare's Butterfly Room.",
        "location": "New York, NY"
    }

    def setUp(self):
        self.login_url = "mercury:EventAccess"
        self.event_url = "mercury:events"
        test_code = EventCodeAccess(event_code=self.TESTCODE, enabled=True)
        test_code.save()

    def _get_with_event_code(self, url, event_code):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": event_code})
        response = self.client.get(reverse(url))
        session = self.client.session
        return response, session

    def post_event_data(self):
        # POST sensor data to the sensor url
        response = self.client.post(
            reverse(self.event_url),
            data={
                "submit": "",
                "event_name": self.test_event_data["name"],
                "event_date": self.test_event_data["date"],
                "event_description": self.test_event_data["description"],
                "event_location": self.test_event_data["location"],
            },
        )
        return response

    def test_EventView_GET_success(self):
        response, session = self._get_with_event_code(self.event_url, self.TESTCODE)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])

    def test_ConfigureSensorView_POST_success(self):
        # Login
        self._get_with_event_code(self.event_url, self.TESTCODE)

        # POST sensor data
        response = self.post_event_data()

        self.assertEqual(200, response.status_code)

    def test_ConfigureSensorView_POST_creates_event(self):
        # Login
        self._get_with_event_code(self.event_url, self.TESTCODE)

        # POST sensor data
        self.post_event_data()

        events = AGEvent.objects.all()
        self.assertEqual(events.count(), 1)

    def test_ConfigureSensorView_POST_creates_event_correct_object_created(self):
        # Login
        self._get_with_event_code(self.event_url, self.TESTCODE)

        # POST sensor data
        self.post_event_data()

        # Check that event object was created with correct values
        events = AGEvent.objects.all()
        event = events[0]
        self.assertEqual(event.event_name, self.test_event_data["name"])
        self.assertEqual(event.event_date, self.test_event_data["date"])
        self.assertEqual(event.event_location, self.test_event_data["location"])
        self.assertEqual(event.event_description, self.test_event_data["description"])



