from django.test import TestCase, Client
from django.urls import reverse


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

    def test_index(self):
        client = Client()
        response = client.get(reverse("mercury:index"))
        self.assertEqual(response.status_code, 200)
