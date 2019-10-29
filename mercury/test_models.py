from django.test import TestCase
from mercury.models import SimulatedData
import datetime


def create_simulated_data():
    SimulatedData.objects.create(name="Foo", created_at=datetime.datetime.now())


class TestSimulatedData(TestCase):
    def setUp(self):
        create_simulated_data()

    def test_vehicle_name(self):
        test_name = "Foo"
        foo = SimulatedData.objects.get(name=test_name)
        self.assertEqual(foo.name, test_name)
