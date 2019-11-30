from django.test import TestCase
from django.urls import reverse
from ..models import EventCodeAccess


class TestViewsWithActiveEvent(TestCase):
    def setUp(self):
        self.index_url = "mercury:index"
        self.login_url = "mercury:EventAccess"
        self.dashboard_url = "mercury:dashboard"
        self.simulator_url = "mercury:simulator"
        self.can_url = "mercury:can-ui"
        self.stopwatch_url = "mercury:stopwatch"

        test_code = EventCodeAccess(event_code="testcode", enabled=True)
        test_code.save()

    def _get_with_known_code(self, url):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": "testcode"})
        response = self.client.get(reverse(url))
        session = self.client.session
        return response, session

    def _get_without_known_code(self, url):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": "fakecode"})
        response = self.client.get(reverse(url))
        session = self.client.session
        return response, session

    def test_HomePageView_GET_fail(self):
        response, session = self._get_without_known_code(self.index_url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(False, session["event_code_known"])

    def test_HomePageView_GET_success(self):
        response, session = self._get_with_known_code(self.index_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])

    def test_DashboardView_GET_fail(self):
        response, session = self._get_without_known_code(self.dashboard_url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(False, session["event_code_known"])

    def test_DashboardView_GET_success(self):
        response, session = self._get_with_known_code(self.dashboard_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])

    def test_SimulatorView_GET_fail(self):
        response, session = self._get_without_known_code(self.simulator_url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(False, session["event_code_known"])

    def test_SimulatorView_GET_success(self):
        response, session = self._get_with_known_code(self.simulator_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])

    def test_CAN_GET_fail(self):
        response, session = self._get_without_known_code(self.can_url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(False, session["event_code_known"])

    def test_CAN_GET_success(self):
        response, session = self._get_with_known_code(self.can_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])

    def test_StopWatch_GET_fail(self):
        response, session = self._get_without_known_code(self.stopwatch_url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(False, session["event_code_known"])

    def test_StopWatch_GET_success(self):
        response, session = self._get_with_known_code(self.stopwatch_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])


class TestViewsWithoutActiveEvent(TestCase):
    def setUp(self):
        self.index_url = "mercury:index"
        self.login_url = "mercury:EventAccess"
        self.dashboard_url = "mercury:dashboard"
        self.simulator_url = "mercury:simulator"
        self.can_url = "mercury:can-ui"
        self.stopwatch_url = "mercury:stopwatch"

    def test_HomePageView_GET(self):
        response = self.client.get(reverse(self.index_url))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed("index.html")

    def test_DashboardView_GET(self):
        response = self.client.get(reverse(self.dashboard_url))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed("dashboard.html")

    def test_SimulatorView_GET(self):
        response = self.client.get(reverse(self.simulator_url))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed("simulator.html")

    def test_CAN_GET(self):
        response = self.client.get(reverse(self.can_url))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed("can.html")

    def test_StopWatch_GET(self):
        response = self.client.get(reverse(self.stopwatch_url))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed("stopwatch.html")
