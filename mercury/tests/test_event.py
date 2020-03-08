from django.test import TestCase
import datetime
from mercury.models import Event

# Test value constants that should all work
TEST_NAME = "test_rockcrawl"
TEST_EVENT_LOCATION = "test_peoria"
TEST_COMMENTS = "this is coming from test_event.py"


def create_simulated_event():
    Event.objects.create(
        event_name=TEST_NAME,
        event_location=TEST_EVENT_LOCATION,
        date=datetime.date.today(),
        comments=TEST_COMMENTS,
    )


class TestSensorModels(TestCase):
    def setUp(self):
        create_simulated_event()

    def test_event(self):
        foo = Event.objects.get(event_name=TEST_NAME)
        self.assertEqual(foo.event_name, TEST_NAME)

        foo = Event.objects.get(event_location=TEST_EVENT_LOCATION)
        self.assertEqual(foo.event_location, TEST_EVENT_LOCATION)

        foo = Event.objects.get(comments=TEST_COMMENTS)
        self.assertEqual(foo.comments, TEST_COMMENTS)
