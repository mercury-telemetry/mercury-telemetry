from django.test import TestCase
from django.urls import reverse
from mercury.models import EventCodeAccess, GFConfig
from mercury.grafanaAPI.grafana_api import Grafana


# default host and token, use this if user did not provide anything
HOST = "https://mercurytests.grafana.net"
# this token has Admin level permissions
TOKEN = "eyJrIjoiQzFMemVOQ0RDUExIcTdhbEluS0hPMDJTZXdKMWQyYTEiLCJuIjoiYXBpX2tleTIiLCJpZCI6MX0="
# this token has Editor level permissions
EDITOR_TOKEN = (
    "eyJrIjoibHlrZ2JWY0pnQk94b1YxSGYzd0NJ"
    "ZUdZa3JBeWZIT3QiLCJuIjoiZWRpdG9yX2tleSIsImlkIjoxfQ=="
)


class TestGFConfig(TestCase):
    TESTCODE = "testcode"

    def setUp(self):
        self.login_url = "mercury:EventAccess"
        self.sensor_url = "mercury:sensor"
        self.event_url = "mercury:events"
        self.config_url = "mercury:gfconfig"
        test_code = EventCodeAccess(event_code="testcode", enabled=True)
        test_code.save()
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        self.gfconfig = GFConfig.objects.create(
            gf_name="Test", gf_host=HOST, gf_token=TOKEN, gf_current=True
        )
        self.gfconfig.save()
        # Create fresh grafana object
        self.grafana = Grafana(self.gfconfig)

        # Create random name to be used for event and datasource
        self.event_name = self.grafana.generate_random_string(10)
        self.datasource_name = self.grafana.generate_random_string(10)

        # Clear existing dashboard and datasource
        self.grafana.delete_dashboard_by_name(self.event_name)
        self.grafana.delete_datasource_by_name(self.datasource_name)

    def tearDown(self):
        # Create fresh grafana instance (in case test invalidated any tokens, etc.)
        self.grafana = Grafana(self.gfconfig)

        # Clear all of the created dashboards
        self.grafana.delete_dashboard_by_name(self.event_name)
        self.grafana.delete_datasource_by_name(self.datasource_name)

    def _get_with_event_code(self, url, event_code):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": event_code})
        response = self.client.get(reverse(url))
        session = self.client.session
        return response, session

    def test_config_view_get_success(self):
        response = self.client.get(reverse(self.config_url))
        self.assertEqual(200, response.status_code)

    def test_config_post_success(self):
        response = self.client.post(
            reverse(self.config_url),
            data={
                "submit": "",
                "gf_name": "Test Grafana Instance",
                "gf_host": HOST,
                "gf_token": TOKEN,
            },
        )
        self.assertEqual(200, response.status_code)

        gfconfig = GFConfig.objects.filter(gf_name="Test Grafana Instance")
        self.assertTrue(gfconfig.count() > 0)
        self.assertTrue(gfconfig[0].gf_name == "Test Grafana Instance")
        self.assertTrue(gfconfig[0].gf_host == HOST)
        self.assertTrue(gfconfig[0].gf_token == TOKEN)

    def test_config_post_fail_invalid_API_key(self):
        response = self.client.post(
            reverse(self.config_url),
            data={
                "submit": "",
                "gf_name": "Test Grafana Instance",
                "gf_host": HOST,
                "gf_token": "abcde",
            },
        )
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Grafana API validation failed: Invalid API key")

        gfconfig = GFConfig.objects.filter(gf_name="Test Grafana Instance")
        self.assertTrue(gfconfig.count() == 0)

    def test_config_post_fail_insufficient_permissions(self):
        response = self.client.post(
            reverse(self.config_url),
            data={
                "submit": "",
                "gf_name": "Test Grafana Instance",
                "gf_host": HOST,
                "gf_token": EDITOR_TOKEN,
            },
        )
        self.assertEqual(200, response.status_code)
        self.assertContains(
            response,
            "Grafana API validation failed: Access denied - check API permissions",
        )

        gfconfig = GFConfig.objects.filter(gf_name="Test Grafana Instance")
        self.assertTrue(gfconfig.count() == 0)
