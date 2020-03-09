from django.test import TestCase
import datetime
from mercury.models import AGEvent

# Test value constants that should all work
TEST_NAME = "test_rockcrawl"
TEST_EVENT_LOCATION = "test_peoria"
TEST_COMMENTS = "this is coming from test_event.py"


def create_simulated_event():
    AGEvent.objects.create(
        event_name=TEST_NAME,
        event_location=TEST_EVENT_LOCATION,
        event_date=datetime.date.today(),
        event_description=TEST_COMMENTS,
    )


class TestEventModel(TestCase):
    def setUp(self):
        create_simulated_event()

    def test_event(self):
        foo = AGEvent.objects.get(event_name=TEST_NAME)
        self.assertEqual(foo.event_name, TEST_NAME)

        foo = AGEvent.objects.get(event_location=TEST_EVENT_LOCATION)
        self.assertEqual(foo.event_location, TEST_EVENT_LOCATION)

        foo = AGEvent.objects.get(event_description=TEST_COMMENTS)
        self.assertEqual(foo.event_description, TEST_COMMENTS)