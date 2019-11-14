from django.test import SimpleTestCase
from django.urls import reverse, resolve
from mercury.views import simulator, views, dashboard


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse("mercury:index")
        self.assertEquals(resolve(url).func.view_class, views.HomePageView)

    def test_simulator_url_is_resolved(self):
        url = reverse("mercury:simulator")
        self.assertEquals(resolve(url).func.view_class, simulator.SimulatorView)

    def test_dashboard_url_is_resolved(self):
        url = reverse("mercury:dashboard")
        self.assertEquals(resolve(url).func.view_class, dashboard.DashboardView)
