import datetime

from django.test import TestCase
from django.urls import reverse
from ..models import (
    EventCodeAccess,
    TemperatureSensor,
    AccelerationSensor,
    WheelSpeedSensor,
    SuspensionSensor,
    FuelLevelSensor,
)

TESTCODE = "testcode"
BADCODE = "fakefake"
CREATED_AT = "2019-12-10 23:25"
EXPECTED_CREATED_AT = datetime.datetime.strptime(CREATED_AT, "%Y-%m-%d %H:%M")


class TestViewsWithActiveEvent(TestCase):
    def setUp(self):
        self.index_url = "mercury:index"
        self.login_url = "mercury:EventAccess"
        self.dashboard_url = "mercury:dashboard"
        self.simulator_url = "mercury:simulator"
        self.can_url = "mercury:can-ui"
        self.stopwatch_url = "mercury:stopwatch"
        self.pitcrew_url = "mercury:pitcrew"

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

    def test_DashboardView_GET_fail(self):
        response, session = self._get_with_event_code(self.dashboard_url, BADCODE)
        self.assertEqual(302, response.status_code)
        self.assertEqual("/", response.url)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(False, session["event_code_known"])

    def test_DashboardView_GET_success(self):
        response, session = self._get_with_event_code(self.dashboard_url, TESTCODE)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])

    def test_SimulatorView_GET_fail(self):
        response, session = self._get_with_event_code(self.simulator_url, BADCODE)
        self.assertEqual(302, response.status_code)
        self.assertEqual("/", response.url)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(False, session["event_code_known"])

    def test_SimulatorView_GET_success(self):
        response, session = self._get_with_event_code(self.simulator_url, TESTCODE)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])

    def test_CAN_GET_fail(self):
        response, session = self._get_with_event_code(self.can_url, BADCODE)
        self.assertEqual(302, response.status_code)
        self.assertEqual("/", response.url)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(False, session["event_code_known"])

    def test_CAN_GET_success(self):
        response, session = self._get_with_event_code(self.can_url, TESTCODE)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])

    def test_StopWatch_GET_fail(self):
        response, session = self._get_with_event_code(self.stopwatch_url, BADCODE)
        self.assertEqual(302, response.status_code)
        self.assertEqual("/", response.url)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(False, session["event_code_known"])

    def test_StopWatch_GET_success(self):
        response, session = self._get_with_event_code(self.stopwatch_url, TESTCODE)
        self.assertEqual(200, response.status_code)
        self.assertEqual(True, session["event_code_active"])
        self.assertEqual(True, session["event_code_known"])

    def test_PitCrewView_GET_success(self):
        response, session = self._get_with_event_code(self.pitcrew_url, TESTCODE)
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

        # Calling GET against login_url is necessary to check for an event
        self.client.get(reverse(self.login_url))

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


class TestSimulatorPost(TestCase):
    """In this test case, returning a 201 from the simulator is only possible
    if the data was saved properly."""

    def setUp(self):
        self.simulator_url = "mercury:simulator"
        self.login_url = "mercury:EventAccess"

        # Calling GET against login_url is necessary to check for an event
        self.client.get(reverse(self.login_url))

    def test_SimulatorView_POST_temp(self):
        temp_value = 1001
        response = self.client.post(
            reverse(self.simulator_url),
            data={"created_at_temp": CREATED_AT, "temperature": temp_value},
        )
        self.assertEqual(201, response.status_code)
        self.assertTemplateUsed("simulator.html")

        foo = TemperatureSensor.objects.get(
            created_at=CREATED_AT, temperature=temp_value
        )
        self.assertEqual(EXPECTED_CREATED_AT, foo.created_at)
        self.assertEqual(temp_value, foo.temperature)

    def test_SimulatorView_POST_accel(self):
        x = 1002
        y = 1003
        z = 1004
        response = self.client.post(
            reverse(self.simulator_url),
            data={
                "created_at_accel": CREATED_AT,
                "acceleration_x": x,
                "acceleration_y": y,
                "acceleration_z": z,
            },
        )
        self.assertEqual(201, response.status_code)
        self.assertTemplateUsed("simulator.html")

        foo = AccelerationSensor.objects.get(
            created_at=CREATED_AT, acceleration_x=x, acceleration_y=y, acceleration_z=z,
        )
        self.assertEqual(EXPECTED_CREATED_AT, foo.created_at)
        self.assertEqual(x, foo.acceleration_x)
        self.assertEqual(y, foo.acceleration_y)
        self.assertEqual(z, foo.acceleration_z)

    def test_SimulatorView_POST_speed(self):
        bl = 1005
        br = 1006
        fl = 1007
        fr = 1008
        response = self.client.post(
            reverse(self.simulator_url),
            data={
                "created_at_ws": CREATED_AT,
                "wheel_speed_bl": bl,
                "wheel_speed_br": br,
                "wheel_speed_fl": fl,
                "wheel_speed_fr": fr,
            },
        )

        self.assertEqual(201, response.status_code)
        self.assertTemplateUsed("simulator.html")

        foo = WheelSpeedSensor.objects.get(
            created_at=CREATED_AT,
            wheel_speed_bl=bl,
            wheel_speed_br=br,
            wheel_speed_fl=fl,
            wheel_speed_fr=fr,
        )
        self.assertEqual(EXPECTED_CREATED_AT, foo.created_at)
        self.assertEqual(fl, foo.wheel_speed_fl)
        self.assertEqual(fr, foo.wheel_speed_fr)
        self.assertEqual(bl, foo.wheel_speed_bl)
        self.assertEqual(br, foo.wheel_speed_br)

    def test_SimulatorView_POST_suspension(self):
        bl = 1009
        br = 1010
        fl = 1011
        fr = 1012
        response = self.client.post(
            reverse(self.simulator_url),
            data={
                "created_at_ss": CREATED_AT,
                "suspension_bl": bl,
                "suspension_br": br,
                "suspension_fl": fl,
                "suspension_fr": fr,
            },
        )

        self.assertEqual(201, response.status_code)
        self.assertTemplateUsed("simulator.html")

        foo = SuspensionSensor.objects.get(
            created_at=CREATED_AT,
            suspension_bl=bl,
            suspension_br=br,
            suspension_fl=fl,
            suspension_fr=fr,
        )
        self.assertEqual(EXPECTED_CREATED_AT, foo.created_at)
        self.assertEqual(fl, foo.suspension_fl)
        self.assertEqual(fr, foo.suspension_fr)
        self.assertEqual(bl, foo.suspension_bl)
        self.assertEqual(br, foo.suspension_br)

    def test_SimulatorView_POST_fuel(self):
        fuel = 1013
        response = self.client.post(
            reverse(self.simulator_url),
            data={"created_at_fl": CREATED_AT, "current_fuel_level": fuel},
        )
        self.assertEqual(201, response.status_code)
        self.assertTemplateUsed("simulator.html")

        foo = FuelLevelSensor.objects.get(
            created_at=CREATED_AT, current_fuel_level=fuel
        )
        self.assertEqual(EXPECTED_CREATED_AT, foo.created_at)
        self.assertEqual(fuel, foo.current_fuel_level)
