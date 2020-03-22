from django.test import TestCase
from django.urls import reverse
from mercury.models import EventCodeAccess
from ag_data.models import AGSensor, AGSensorType
from ag_data import simulator
from mercury.grafanaAPI.grafana_api import Grafana
import requests
import os

# default host and token, use this if user did not provide anything
HOST = "https://dbc291.grafana.net"
TOKEN = "eyJrIjoiRTQ0cmNGcXRybkZlUUNZWmRvdFI0UlMwdFVYVUt3bzgiLCJuIjoia2V5IiwiaWQiOjF9"


# This test needs to have access to a test deployment of grafana, otherwise
# we will need to wipe out the sensors each time it runs it runs
class TestGrafana(TestCase):
    TESTCODE = "testcode"

    sim = simulator.Simulator()
    grafana = Grafana(HOST, TOKEN)

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
        # Clear all of existing dashboards
        self.grafana.delete_all_dashboards()
        self.grafana.delete_datasource_by_name(self.grafana.database_grafana_name)

    def tearDown(self):
        # Clear all of the created dashboards
        self.grafana.delete_all_dashboards()
        self.grafana.delete_datasource_by_name(self.grafana.database_grafana_name)

    def _get_with_event_code(self, url, event_code):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": event_code})
        response = self.client.get(reverse(url))
        session = self.client.session
        return response, session

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
            self.grafana.datasource_name_endpoint, self.grafana.database_grafana_name
        )
        headers = {"Content-Type": "application/json"}
        response = requests.get(
            url=endpoint, headers=headers, auth=("api_key", self.grafana.api_token)
        )

        self.assertTrue(response.json()["message"])
        self.assertEquals(response.json()["message"], "Data source not found")

    def test_create_postgres_datasource(self):
        # create datasource
        self.grafana.create_postgres_datasource()

        # confirm that the datasource exists
        endpoint = os.path.join(
            self.grafana.datasource_name_endpoint, self.grafana.database_grafana_name
        )
        headers = {"Content-Type": "application/json"}
        response = requests.get(
            url=endpoint, headers=headers, auth=("api_key", self.grafana.api_token)
        )

        self.assertEquals(response.json()["name"], self.grafana.database_grafana_name)

    def test_create_grafana_dashboard(self):
        dashboard = self.grafana.create_dashboard(self.title)
        self.assertTrue(dashboard)

        # check that the returned dashboard object has a success status message and
        # expected slug (name)
        self.assertEquals(dashboard["status"], "success")
        self.assertEquals(dashboard["slug"], self.title.lower())
        uid = dashboard["uid"]

        # check that the new dashboard can be queried from the API
        endpoint = os.path.join(self.grafana.dashboard_uid_endpoint, uid)
        headers = {"Content-Type": "application/json"}
        response = requests.get(
            url=endpoint, headers=headers, auth=("api_key", self.grafana.api_token)
        )

        self.assertEquals(response.json()["dashboard"]["uid"], uid)
        self.assertEquals(response.json()["dashboard"]["title"], self.title)

    def test_delete_grafana_dashboard(self):
        dashboard = self.grafana.create_dashboard(self.title)

        self.assertTrue(dashboard)

        deleted_dashboard = self.grafana.delete_dashboard(dashboard["uid"])

        self.assertTrue(deleted_dashboard)

        # figure out whether the dashboard was actually deleted
        endpoint = os.path.join(self.grafana.dashboard_uid_endpoint, dashboard["uid"])
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

        self.(dashboard_info)
        self.(dashboard_info["dashboard"])
        self.assertTrue(dashboard_info["dashboard"]["panels"])
        self.assertTrue(len(dashboard_info["dashboard"]["panels"]) == 1)
        self.assertTrue(
            dashboard_info["dashboard"]["panels"][0]["title"] == sensor.name
        )

        # check that created panel can be queried

    def not_test_add_multiple_grafana_panels(self):
        self.grafana.create_postgres_datasource()
        dashboard = self.grafana.create_dashboard(self.title)
        self.assertTrue(dashboard)
        uid = dashboard["uid"]

        self.assertTrue(dashboard)
        self.assertEquals(dashboard["status"], "success")

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
        self.grafana.add_panel(sensor, uid)
        self.grafana.add_panel(sensor, uid)
        self.grafana.add_panel(sensor, uid)

        dashboard_info = self.grafana.get_dashboard_with_uid(uid)
        self.assertTrue(dashboard_info)
        self.assertTrue(dashboard_info["dashboard"])
        self.assertTrue(dashboard_info["dashboard"]["panels"])
        self.assertTrue(len(dashboard_info["dashboard"]["panels"]) == 4)

        # simple check that 4 panels with the expected titles were made
        for i in range(4):
            self.assertTrue(
                dashboard_info["dashboard"]["panels"][i]["title"] == sensor.name
            )
            self.assertTrue(
                dashboard_info["dashboard"]["panels"][i]["title"] == sensor.name
            )
