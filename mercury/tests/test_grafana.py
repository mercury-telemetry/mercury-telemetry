from django.test import TestCase
from django.urls import reverse
from mercury.models import EventCodeAccess
from ag_data.models import AGSensor, AGSensorType
from ag_data import simulator
from mercury.grafanaAPI.grafana_api import Grafana


# This test needs to have access to a test deployment of grafana, otherwise
# we will need to wipe out the sensors each time it runs it runs
class TestGrafana(TestCase):
    TESTCODE = "testcode"

    sim = simulator.Simulator()
    grafana = Grafana()

    title = "Bar"

    test_sensor_name = "Wind Sensor"
    test_sensor_type = "Dual wind"
    test_sensor_format = {
        "left_gust": {
            "unit": "km/h",
            "format": "float"
        },
        "right_gust": {
            "unit": "km/h",
            "format": "float"
        },
    }

    def setUp(self):
        self.login_url = "mercury:EventAccess"
        self.sensor_url = "mercury:sensor"
        test_code = EventCodeAccess(event_code="testcode", enabled=True)
        test_code.save()
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)
        # Clear all of existing dashboards
        #self.grafana.delete_all_dashboards()

    def tearDown(self):
        # Clear all of the created dashboards
        #self.grafana.delete_all_dashboards()
        pass

    def _get_with_event_code(self, url, event_code):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": event_code})
        response = self.client.get(reverse(url))
        session = self.client.session
        return response, session

    """
    def test_create_grafana_dashboard(self):
        dashboard = self.grafana.create_dashboard(self.title)

        print(dashboard)

        self.assertTrue(dashboard)
        self.assertEquals(dashboard["status"], "success")
        self.assertEquals(dashboard["slug"], self.title.lower())

        ## should check in some other way that the dashboard was created,
        ## don't trust the function output itself

        self.grafana.delete_all_dashboards()
    """

    def not_test_delete_grafana_dashboard(self):
        dashboard = self.grafana.create_dashboard(self.title)

        self.assertTrue(dashboard)
        self.assertTrue(self.grafana.delete_dashboard(dashboard["uid"]))

        ## should check in some other way that the dashboard was deleted
        ## don't trust the function output itself
        ## query to see if other dashboards exist

    def not_test_add_grafana_panel(self):
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
            format=self.test_sensor_format
        )
        sensor_type.save()
        sensor = AGSensor.objects.create(
            name=self.test_sensor_name,
            type_id=sensor_type
        )
        sensor.save()

        self.grafana.add_grafana_panel(sensor, uid)

        dashboard_info = self.grafana.get_dashboard_with_uid(uid)
        print(dashboard_info)

        self.assertTrue(dashboard_info["dashboard"])
        self.assertTrue(dashboard_info["dashboard"]["panels"])
        self.assertTrue(len(dashboard_info["dashboard"]["panels"]) == 1)
        self.assertTrue(dashboard_info["dashboard"]["panels"][0]["title"] ==
                        sensor.name)

    def test_add_grafana_panels(self):
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
            format=self.test_sensor_format
        )
        sensor_type.save()
        sensor = AGSensor.objects.create(
            name=self.test_sensor_name,
            type_id=sensor_type
        )
        sensor.save()

        self.grafana.add_grafana_panel(sensor, uid)
        self.grafana.add_grafana_panel(sensor, uid)
        self.grafana.add_grafana_panel(sensor, uid)
        self.grafana.add_grafana_panel(sensor, uid)

        dashboard_info = self.grafana.get_dashboard_with_uid(uid)
        print(dashboard_info)

        self.assertTrue(dashboard_info["dashboard"])
        self.assertTrue(dashboard_info["dashboard"]["panels"])
        self.assertTrue(len(dashboard_info["dashboard"]["panels"]) == 4)
        # simple check that 4 panels with the expected titles were made
        for i in range(4):
            self.assertTrue(dashboard_info["dashboard"]["panels"][i]["title"] ==
                            sensor.name)

    """
    def test_create_grafana_panels(self, uid="GjrBC6uZz"):
    
        dashboard = self.grafana.create_dashboard()

        self.sim.createOrResetASensorTypeFromPresets(0)
        self.sim.createASensorFromPresets(0)

        

        # delete all grafana panels
        self.grafana.delete_grafana_panels(uid)

        # Assert that no panel exists yet
        self.assertTrue(len(panels) == 0)

        self.grafana.add_grafana_panel(sensor, uid)

        dashboard_info = self.grafana.get_dashboard_with_uid(uid)
        panels = dashboard_info["dashboard"]["panels"]

        # Assert that a panel was created
        self.assertTrue(len(panels) == 1)

        self.grafana.add_grafana_panel(sensor, uid)
    """