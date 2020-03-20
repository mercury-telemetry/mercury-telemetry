from django.test import TestCase
from django.urls import reverse
from mercury.models import EventCodeAccess
from ag_data.models import AGSensor
from ag_data import simulator
from mercury.grafanaAPI.grafana_api import Grafana


# This test needs to have access to a test deployment of grafana, otherwise
# we will need to wipe out the sensors each time it runs it runs
class TestGrafana(TestCase):
    TESTCODE = "testcode"

    sim = simulator.Simulator()
    grafana = Grafana()

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

    def test_create_grafana_panels(self):
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        self.sim.createOrResetASensorTypeFromPresets(0)
        self.sim.createASensorFromPresets(0)

        sensors = AGSensor.objects.filter(type_id=0)
        sensor = sensors[0]

        dashboard_info = self.grafana.get_dashboard_with_uid(self.grafana.uid)
        panels = dashboard_info["dashboard"]["panels"]

        # delete all grafana panels
        self.grafana.delete_grafana_panels(self.grafana.uid)

        # Assert that no panel exists yet
        self.assertTrue(len(panels) == 0)

        self.grafana.add_grafana_panel(sensor, self.grafana.uid)

        dashboard_info = self.grafana.get_dashboard_with_uid(self.grafana.uid)
        panels = dashboard_info["dashboard"]["panels"]

        # Assert that a panel was created
        self.assertTrue(len(panels) == 1)

        self.grafana.add_grafana_panel(sensor, self.grafana.uid)
