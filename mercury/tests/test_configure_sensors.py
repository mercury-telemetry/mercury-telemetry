from django.test import TestCase
from django.urls import reverse
from mercury.models import EventCodeAccess

TESTCODE = "testcode"


class TestConfigureSensorView(TestCase):
    def setUp(self):
        self.login_url = "mercury:EventAccess"
        self.sensor_url = "mercury:sensor"
        test_code = EventCodeAccess(event_code="testcode", enabled=True)
        test_code.save()

    def _get_with_event_code(self, url, event_code):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": event_code})
        response = self.client.get(reverse(url))
        session = self.client.session
        return response, session

    def test_ConfigureSensorView_GET_success(self):
        response, session = self._get_with_event_code(self.sensor_url, TESTCODE)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])