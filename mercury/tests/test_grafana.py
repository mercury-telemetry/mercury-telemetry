from django.test import TestCase
from django.urls import reverse
from mercury.models import EventCodeAccess
from ag_data.models import AGSensor, AGSensorType
from ag_data import simulator
from mercury.grafanaAPI.grafana_api import Grafana
import requests
import os

# default host and token, use this if user did not provide anything
HOST = "https://mercurytests.grafana.net"
TOKEN = (
    "eyJrIjoiUm81MzlOUlRhalhGUFJ5OVVMNTZGTTZIdT"
    "dvVURDSzIiLCJuIjoiYXBpX2tleSIsImlkIjoxfQ=="
)


# This test needs to have access to a test deployment of grafana, otherwise
# we will need to wipe out the sensors each time it runs it runs
class TestGrafana(TestCase):
    TESTCODE = "testcode"

    sim = simulator.Simulator()

    title = "Bar"

    test_sensor_name = "Wind Sensor"
    test_sensor_type = "Dual wind"
    test_sensor_format = {
        "left_gust": {"unit": "km/h", "format": "float"},
        "right_gust": {"unit": "km/h", "format": "float"},
    }

    def setUp(self):
        self.login_url = "mercury:EventAccess"
        self.sensor_url = "mercury:sensor"
        test_code = EventCodeAccess(event_code="testcode", enabled=True)
        test_code.save()
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # Create fresh grafana instance
        self.grafana = Grafana(HOST, TOKEN)

        # Clear all of existing dashboards
        self.grafana.delete_all_dashboards()
        self.grafana.delete_datasource_by_name(self.grafana.database_grafana_name)

    def tearDown(self):
        # Create fresh grafana instance (in case test invalidated any tokens, etc.)
        self.grafana = Grafana(HOST, TOKEN)

        # Clear all of the created dashboards
        self.grafana.delete_all_dashboards()
        self.grafana.delete_datasource_by_name(self.grafana.database_grafana_name)

    def _get_with_event_code(self, url, event_code):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": event_code})
        response = self.client.get(reverse(url))
        session = self.client.session
        return response, session

    def test_get_dashboard_exists(self):
        dashboard = self.grafana.create_dashboard(self.title)

        self.assertTrue(dashboard)

        uid = dashboard["uid"]

        fetched_dashboard = self.grafana.get_dashboard_with_uid(uid)

        self.assertTrue(fetched_dashboard)
        self.assertTrue(fetched_dashboard["meta"])
        self.assertTrue(fetched_dashboard["meta"]["slug"], self.title.lower())
        self.assertTrue(fetched_dashboard["dashboard"])
        self.assertTrue(fetched_dashboard["dashboard"]["uid"], uid)
        self.assertTrue(fetched_dashboard["dashboard"]["title"], self.title)

    def test_get_dashboard_fail(self):
        uid = "abcde"  # doesn't exist

        fetched_dashboard = self.grafana.get_dashboard_with_uid(uid)

        self.assertFalse(fetched_dashboard)

    def test_create_grafana_dashboard_success(self):
        dashboard = self.grafana.create_dashboard(self.title)

        self.assertTrue(dashboard)

    def test_create_grafana_dashboard_verify_new_dashboard_contents(self):
        dashboard = self.grafana.create_dashboard(self.title)

        self.assertTrue(dashboard)
        self.assertEquals(dashboard["status"], "success")
        self.assertEquals(dashboard["slug"], self.title.lower())
        uid = dashboard["uid"]

        # confirm new dashboard can be queried from the API
        endpoint = os.path.join(self.grafana.endpoints["dashboard_uid"], uid)
        headers = {"Content-Type": "application/json"}
        response = requests.get(
            url=endpoint, headers=headers, auth=("api_key", self.grafana.api_token)
        )

        self.assertEquals(response.json()["dashboard"]["uid"], uid)
        self.assertEquals(response.json()["dashboard"]["title"], self.title)

    def test_create_grafana_dashboard_fail_authorization(self):
        self.grafana.api_token = "abcde"  # invalidate API token

        expected_message = "Invalid API key"
        with self.assertRaisesMessage(ValueError, expected_message):
            self.grafana.create_dashboard(self.title)

    def test_create_grafana_dashboard_fail_duplicate_title(self):
        dashboard = self.grafana.create_dashboard(self.title)
        self.assertTrue(dashboard)

        expected_message = "Dashboard with the same name already exists"
        with self.assertRaisesMessage(ValueError, expected_message):
            self.grafana.create_dashboard(self.title)

    def test_delete_grafana_dashboard(self):
        dashboard = self.grafana.create_dashboard(self.title)
        self.assertTrue(dashboard)

        deleted_dashboard = self.grafana.delete_dashboard(dashboard["uid"])
        self.assertTrue(deleted_dashboard)

        # figure out whether the dashboard was actually deleted
        endpoint = os.path.join(
            self.grafana.endpoints["dashboard_uid"], dashboard["uid"]
        )
        headers = {"Content-Type": "application/json"}
        response = requests.get(
            url=endpoint, headers=headers, auth=("api_key", self.grafana.api_token)
        )

        self.assertTrue(response.json()["message"])
        self.assertEquals(response.json()["message"], "Dashboard not found")

    def test_add_panel(self):
        dashboard = self.grafana.create_dashboard(self.title)
        self.assertTrue(dashboard)
        uid = dashboard["uid"]

        self.sim.createOrResetASensorTypeFromPresets(0)
        self.sim.createASensorFromPresets(0)

        dashboard_info = self.grafana.get_dashboard_with_uid(uid)
        try:
            panels = dashboard_info["dashboard"]["panels"]
        except KeyError:
            panels = []
        self.assertTrue(len(panels) == 0)

        sensor_type = AGSensorType.objects.create(
            name=self.test_sensor_type,
            processing_formula=0,
            format=self.test_sensor_format,
        )
        sensor_type.save()
        sensor = AGSensor.objects.create(
            name=self.test_sensor_name, type_id=sensor_type
        )
        sensor.save()

        self.grafana.add_panel(sensor, uid)

        dashboard_info = self.grafana.get_dashboard_with_uid(uid)

        self.assertTrue(dashboard_info)
        self.assertTrue(dashboard_info["dashboard"])
        self.assertTrue(dashboard_info["dashboard"]["panels"])
        self.assertTrue(len(dashboard_info["dashboard"]["panels"]) == 1)
        self.assertTrue(
            dashboard_info["dashboard"]["panels"][0]["title"] == sensor.name
        )

    def test_create_postgres_datasource(self):
        # create datasource
        self.grafana.create_postgres_datasource()

        # confirm that the datasource exists
        endpoint = os.path.join(
            self.grafana.endpoints["datasource_name"],
            self.grafana.database_grafana_name,
        )
        headers = {"Content-Type": "application/json"}
        response = requests.get(
            url=endpoint, headers=headers, auth=("api_key", self.grafana.api_token)
        )

        self.assertEquals(response.json()["name"], self.grafana.database_grafana_name)

    def test_delete_postgres_datasource(self):
        # create the datasource
        self.grafana.create_postgres_datasource()

        # deleted should be true if delete_datasource_by_name returns true
        deleted = self.grafana.delete_datasource_by_name(
            self.grafana.database_grafana_name
        )
        self.assertTrue(deleted)

        # figure out whether the datasource was actually deleted
        endpoint = os.path.join(
            self.grafana.endpoints["datasource_name"],
            self.grafana.database_grafana_name,
        )
        headers = {"Content-Type": "application/json"}
        response = requests.get(
            url=endpoint, headers=headers, auth=("api_key", self.grafana.api_token)
        )

        self.assertTrue(response.json()["message"])
        self.assertEquals(response.json()["message"], "Data source not found")
