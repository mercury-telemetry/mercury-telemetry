import datetime

from django.test import TestCase
from django.urls import reverse
from ..models import EventCodeAccess

TESTCODE = "testcode"
BADCODE = "fakefake"
CREATED_AT = "2019-12-10 23:25"
EXPECTED_CREATED_AT = datetime.datetime.strptime(CREATED_AT, "%Y-%m-%d %H:%M")


class TestViewsWithActiveEvent(TestCase):
    def setUp(self):
        self.index_url = "mercury:index"
        self.login_url = "mercury:EventAccess"

        test_code = EventCodeAccess(event_code="testcode", enabled=True)
        test_code.save()

    def _get_with_event_code(self, url, event_code):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": event_code})
        response = self.client.get(reverse(url))
        session = self.client.session
        return response, session

    def test_HomePageView_GET_fail(self):
        response, session = self._get_with_event_code(self.index_url, BADCODE)
        self.assertEqual(302, response.status_code)
        self.assertEqual("/", response.url)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(False, session["event_code_known"])

    def test_HomePageView_GET_success(self):
        response, session = self._get_with_event_code(self.index_url, TESTCODE)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])


class TestViewsWithoutActiveEvent(TestCase):
    def setUp(self):
        self.index_url = "mercury:index"
        self.login_url = "mercury:EventAccess"

        # Calling GET against login_url is necessary to check for an event
        self.client.get(reverse(self.login_url))

    def test_HomePageView_GET(self):
        response = self.client.get(reverse(self.index_url))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed("index.html")


class TestLogout(TestCase):
    def setUp(self):
        self.login_url = "mercury:EventAccess"
        self.logout_url = "mercury:logout"

        test_code = EventCodeAccess(event_code="testcode", enabled=True)
        test_code.save()

    def _get_with_event_code(self, url):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": "testcode"})
        response = self.client.get(reverse(url))
        session = self.client.session
        return response, session

    def test_logout_after_login(self):
        response, session = self._get_with_event_code(self.logout_url)
        self.assertEqual(302, response.status_code)
        self.assertEqual("/", response.url)
        self.assertNotIn("event_code_active", session)
        self.assertNotIn("event_code_known", session)

    def test_logout_without_login(self):
        response = self.client.get(reverse(self.logout_url))
        session = self.client.session
        self.assertEqual(302, response.status_code)
        self.assertEqual("/", response.url)
        self.assertNotIn("event_code_active", session)
        self.assertNotIn("event_code_known", session)


class TestEventAccessDisabled(TestCase):
    def setUp(self):
        self.login_url = "mercury:EventAccess"
        test_code = EventCodeAccess(event_code="testcode", enabled=False)
        test_code.save()

    def test_active_event_get(self):
        response = self.client.get(reverse(self.login_url))
        session = self.client.session
        self.assertEqual(302, response.status_code)
        self.assertEqual(False, session["event_code_active"])


class TestEventAlreadyLoggedIn(TestCase):
    def setUp(self):
        self.login_url = "mercury:EventAccess"
        test_code = EventCodeAccess(event_code="testcode", enabled=True)
        test_code.save()

    def test_bypass_login(self):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": "testcode"})
        response = self.client.get(reverse(self.login_url))
        self.assertEqual(302, response.status_code)
        self.assertEqual("index", response.url)


class TestViewsWithoutCheckingEvent(TestCase):
    def setUp(self):
        self.index_url = "mercury:index"

    def test_HomePageView_GET(self):
        response = self.client.get(reverse(self.index_url))
        self.assertEqual(302, response.status_code)
