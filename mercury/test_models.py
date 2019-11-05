from django.test import TestCase
from mercury.models import SimulatedData
import datetime

TEST_TEMP = 999.0

def create_simulated_data():
    SimulatedData.objects.create(temperature=TEST_TEMP, created_at=datetime.datetime.now())


class TestSimulatedData(TestCase):
    def setUp(self):
        create_simulated_data()

    def test_vehicle_temp(self):
        foo = SimulatedData.objects.get(temperature=TEST_TEMP)
        self.assertEqual(foo.temperature, TEST_TEMP)
