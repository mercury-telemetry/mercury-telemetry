from django.test import TestCase, Client
from django.urls import reverse
from .models import SimulatedData
from datetime import datetime


class TestViews(TestCase):
    def test_dashboard(self):
        client = Client()
        response = client.get(reverse("mercury:dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_live(self):
        client = Client()
        response = client.get(reverse("mercury:dashboard-live"))
        self.assertEqual(response.status_code, 200)

    def test_simulator(self):
        client = Client()
        response = client.get(reverse("mercury:simulator"))
        self.assertEqual(response.status_code, 200)

    def test_simulator_post(self):
        client = Client()
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
            "current_fuel_level": 0
        }
        response = client.post(reverse("mercury:simulator"), data=test_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SimulatedData.objects.last().temperature, 123)

    def test_index(self):
        client = Client()
        response = client.get(reverse("mercury:index"))
        self.assertEqual(response.status_code, 200)
