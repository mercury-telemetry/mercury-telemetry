from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
from mercury.models import SimulatedData


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.index_url = "mercury:index"
        self.dashboard_url = "mercury:dashboard"
        self.simulator_url = "mercury:simulator"

    def test_HomePageView_GET(self):
        response = self.client.get(reverse(self.index_url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_DashboardView_GET(self):
        response = self.client.get(reverse(self.dashboard_url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard.html")

    def test_SimulatorView_GET(self):
        response = self.client.get(reverse(self.simulator_url))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "simulator.html")

    # TODO after deciding, how to post data (no views function for the sensors as of now)
    def test_SimulatorView_POST(self):
        test_data = {
            "temperature": 123,
            "created_at": datetime.now(),
            "acceleration_x": 0,
            "acceleration_y": 0,
            "acceleration_z": 0,
            "wheel_speed_fr": 0,
            "wheel_speed_fl": 0,
            "wheel_speed_br": 0,
            "wheel_speed_bl": 0,
            "suspension_fr": 0,
            "suspension_fl": 0,
            "suspension_br": 0,
            "suspension_bl": 0,
            "current_fuel_level": 0,
        }
        response = self.client.post(reverse(self.simulator_url), data=test_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SimulatedData.objects.last().temperature, 123)
