from django.test import TestCase
from mercury.models import EventCodeAccess

# Test value constants that should all work
TEST_TEMP = 999.0
TEST_ACCEL_Y = 9.81
TEST_WHEEL_SPEED_FR = 30
TEST_SUSPENSION_FR = 2
TEST_FUEL = 6
TEST_EVENT_CODE = "abcdefgh"


def create_simulated_data_objects():
    EventCodeAccess.objects.create(event_code=TEST_EVENT_CODE, enabled=False)


class TestSensorModels(TestCase):
    def test_event_code_access(self):
        foo = EventCodeAccess.objects.get(event_code=TEST_EVENT_CODE, enabled=False)
        self.assertEqual(TEST_EVENT_CODE, foo.event_code)
