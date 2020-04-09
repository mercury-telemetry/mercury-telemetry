from django.test import TestCase
from django.urls import reverse
from mercury.models import EventCodeAccess, GFConfig
from ag_data.models import AGEvent, AGVenue, AGSensor, AGSensorType
from mercury.grafanaAPI.grafana_api import Grafana
from mercury.forms import DashboardSensorPanelsForm
import os
import datetime

# default host and token, use this if user did not provide anything
HOST = "http://test-grafana.eba-b2r7zzze.us-east-1.elasticbeanstalk.com"
# this token has Admin level permissions
TOKEN = (
    "eyJrIjoiUVN2NUVXejRLRm9mUWxkcGN4Njd5Z0c0UHJSSzltWGYiLCJuIjoiYWRtaW4iLCJpZCI6MX0="
)
# this token has viewer level permissions
VIEWER_TOKEN = (
    "eyJrIjoiNm13bW1NdDdqM3cwdVF4SkRwTXBuM2VDMzVEa2FtcFoiLCJuIjoidmlld2VyIiwiaWQiOjF9"
)


class TestGFConfig(TestCase):
    TESTCODE = "testcode"

    test_sensor_name = "Wind Sensor"
    test_sensor_type = "Dual wind"
    test_sensor_format = {
        "left_gust": {"unit": "km/h", "format": "float"},
        "right_gust": {"unit": "km/h", "format": "float"},
    }

    test_event_data = {
        "name": "Sunny Day Test Drive",
        "date": datetime.datetime(2020, 2, 2, 20, 21, 22),
        "description": "A very progressive test run at \
                        Sunnyside Daycare's Butterfly Room.",
        "location": "New York, NY",
    }

    test_venue_data = {
        "name": "Venue 1",
        "description": "foo",
        "latitude": 100,
        "longitude": 200,
    }

    def create_venue_and_event(self, event_name):
        venue = AGVenue.objects.create(
            name=self.test_venue_data["name"],
            description=self.test_venue_data["description"],
            latitude=self.test_venue_data["latitude"],
            longitude=self.test_venue_data["longitude"],
        )
        venue.save()

        event = AGEvent.objects.create(
            name=event_name,
            date=self.test_event_data["date"],
            description=self.test_event_data["description"],
            venue_uuid=venue,
        )
        event.save()

        return event

    def setUp(self):
        self.login_url = "mercury:EventAccess"
        self.sensor_url = "mercury:sensor"
        self.event_url = "mercury:events"
        self.config_url = "mercury:gfconfig"
        self.config_update_url = "mercury:gfconfig_update"
        self.config_delete_url = "mercury:gfconfig_delete"
        self.config_update_dashboard_url = "mercury:gfconfig_update_dashboard"
        self.config_reset_dashboard_url = "mercury:gfconfig_reset_dashboard"
        self.config_delete_dashboard_url = "mercury:gfconfig_delete_dashboard"
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

    def test_config_view_get_existing_dashboard_displayed(self):
        venue = AGVenue.objects.create(
            name=self.test_venue_data["name"],
            description=self.test_venue_data["description"],
            latitude=self.test_venue_data["latitude"],
            longitude=self.test_venue_data["longitude"],
        )
        venue.save()

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

        # Send a request to create an event (should trigger the creation of a
        # grafana dashboard of the same name)
        self.client.post(
            reverse(self.event_url),
            data={
                "submit-event": "",
                "name": self.event_name,
                "date": self.test_event_data["date"],
                "description": self.test_event_data["description"],
                "venue_uuid": venue.uuid,
            },
        )
        response = self.client.get(reverse(self.config_url))

        self.assertContains(response, self.event_name)
        self.assertContains(response, sensor.name)
        self.assertIsInstance(
            response.context["configs"][0]["dashboards"][0]["sensor_form"],
            DashboardSensorPanelsForm,
        )

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

    def test_config_post_fail_invalid_api_key(self):
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
                "gf_token": VIEWER_TOKEN,
            },
        )
        self.assertEqual(200, response.status_code)
        self.assertContains(
            response,
            "Grafana API validation failed: Access denied - check API permissions",
        )

        gfconfig = GFConfig.objects.filter(gf_name="Test Grafana Instance")
        self.assertTrue(gfconfig.count() == 0)

    def test_delete_config(self):
        GFConfig.objects.all().delete()

        gfconfig = GFConfig.objects.create(
            gf_name="Test Grafana Instance", gf_host=HOST, gf_token=TOKEN
        )
        gfconfig.save()
        gfconfig = GFConfig.objects.filter(gf_name="Test Grafana Instance").first()

        self.client.post(
            os.path.join(
                reverse(self.config_delete_url, kwargs={"gf_id": gfconfig.id})
            ),
            data={
                "submit": "",
                "gf_name": "Test Grafana Instance",
                "gf_host": HOST,
                "gf_token": TOKEN,
            },
        )
        gfconfig = GFConfig.objects.filter(gf_name="Test Grafana Instance")
        self.assertTrue(gfconfig.count() == 0)

    # test that GFConfig.gf_current can be set to True using the update view
    def test_update_config(self):
        GFConfig.objects.all().delete()

        gfconfig = GFConfig.objects.create(
            gf_name="Test Grafana Instance",
            gf_host=HOST,
            gf_token=TOKEN,
            gf_current=False,
        )
        gfconfig.save()

        self.client.post(
            os.path.join(reverse(self.config_update_url, kwargs={"gf_id": gfconfig.id}))
        )

        gfconfig = GFConfig.objects.all().first()
        self.assertEquals(gfconfig.gf_current, True)

    def test_config_post_event_exists_dashboard_created(self):
        self.create_venue_and_event(self.event_name)

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

        # check that dashboard was created with same name as event
        dashboard = self.grafana.get_dashboard_by_name(self.event_name)
        self.assertTrue(dashboard)
        self.assertEquals(dashboard["dashboard"]["title"], self.event_name)

    def test_config_post_event_exists_dashboard_created_with_sensor(self):
        # Create a sensor type and sensor
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

        self.create_venue_and_event(self.event_name)

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

        # check that dashboard was created with expected panel
        dashboard = self.grafana.get_dashboard_by_name(self.event_name)
        self.assertTrue(dashboard)
        self.assertEquals(dashboard["dashboard"]["title"], self.event_name)
        # panels should have been created
        # querying like this because the returned dashboard object may have no panels
        # attribute, so trying to retrieve dashboard["panels"] could throw a key error
        panels = dashboard["dashboard"].get("panels", None)
        self.assertTrue(panels)
        self.assertTrue(len(panels) == 1)
        panel = panels[0]
        self.assertEquals(panel["title"], self.test_sensor_name)

    def test_update_dashboard_panels_remove_all_single_gfconfig(self):
        # Create an event
        event = self.create_venue_and_event(self.event_name)

        # Create a dashboard
        self.grafana.create_dashboard(self.event_name)

        # Add a panel to the dashboard
        #   Create a sensor type and sensor
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
        #   Add a sensor panel
        self.grafana.add_panel(sensor, event)

        # Update dashboard with empty list of sensors
        self.client.post(
            reverse(
                self.config_update_dashboard_url, kwargs={"gf_id": self.gfconfig.id}
            ),
            data={"dashboard_name": self.event_name, "sensors": []},
        )

        # Query dashboard
        dashboard = self.grafana.get_dashboard_by_name(self.event_name)
        self.assertTrue(dashboard)

        # Retrieve current panels
        try:
            panels = dashboard["dashboard"]["panels"]
        except KeyError:
            panels = []

        # Confirm panels were deleted
        self.assertEquals(panels, [])

    def test_update_dashboard_panels_keep_all_panels_single_gfconfig(self):
        self.create_venue_and_event(self.event_name)

        # create a dashboard
        self.grafana.create_dashboard(self.event_name)

        # add a panel to the dashboard
        # Create a sensor type and sensor
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

        sensors = AGSensor.objects.all()
        sensor_ids = []
        for sensor in sensors:
            sensor_ids.append(sensor.id)

        self.client.post(
            reverse(
                self.config_update_dashboard_url, kwargs={"gf_id": self.gfconfig.id}
            ),
            data={"dashboard_name": self.event_name, "sensors": sensor_ids},
        )

        dashboard = self.grafana.get_dashboard_by_name(self.event_name)

        self.assertTrue(dashboard)

        # Retrieve current panels
        try:
            panels = dashboard["dashboard"]["panels"]
        except KeyError:
            panels = []

        self.assertEquals(len(panels), 1)

    def test_update_dashboard_panels_keep_subset_of_panels_single_gfconfig(self):
        self.create_venue_and_event(self.event_name)

        # create a dashboard
        self.grafana.create_dashboard(self.event_name)

        # add a panel to the dashboard
        # Create a sensor type and sensor
        sensor_type = AGSensorType.objects.create(
            name=self.test_sensor_type,
            processing_formula=0,
            format=self.test_sensor_format,
        )
        sensor_type.save()

        # Create 5 sensors
        for i in range(5):
            sensor = AGSensor.objects.create(
                name=self.test_sensor_name + "i", type_id=sensor_type
            )
            sensor.save()

        # Retrieve sensor ids for the first 2 sensors
        sensor_ids = []
        sensors = AGSensor.objects.all()
        for i in range(2):
            sensor_ids.append(sensors[i].id)

        # Post to update the dashboard with 2 sensor panels
        self.client.post(
            reverse(
                self.config_update_dashboard_url, kwargs={"gf_id": self.gfconfig.id}
            ),
            data={"dashboard_name": self.event_name, "sensors": sensor_ids},
        )

        dashboard = self.grafana.get_dashboard_by_name(self.event_name)

        self.assertTrue(dashboard)

        # Retrieve current panels
        try:
            panels = dashboard["dashboard"]["panels"]
        except KeyError:
            panels = []

        self.assertEquals(len(panels), 2)
        for i in range(2):
            self.assertEquals(panels[i]["title"], sensors[i].name)

    def test_reset_dashboard_panels_single_gfconfig(self):
        # update dashboard with a subset of panels, then restore all panels by using
        # reset
        self.create_venue_and_event(self.event_name)

        # create a dashboard
        self.grafana.create_dashboard(self.event_name)

        # add a panel to the dashboard
        # Create a sensor type and sensor
        sensor_type = AGSensorType.objects.create(
            name=self.test_sensor_type,
            processing_formula=0,
            format=self.test_sensor_format,
        )
        sensor_type.save()

        # Create 5 sensors
        for i in range(5):
            sensor = AGSensor.objects.create(
                name=self.test_sensor_name + "i", type_id=sensor_type
            )
            sensor.save()

        # Retrieve sensor ids for the first 2 sensors
        sensor_ids_partial = []
        sensors = AGSensor.objects.all()
        for i in range(2):
            sensor_ids_partial.append(sensors[i].id)

        # Post to update the dashboard with 2 sensor panels
        self.client.post(
            reverse(
                self.config_update_dashboard_url, kwargs={"gf_id": self.gfconfig.id}
            ),
            data={"dashboard_name": self.event_name, "sensors": sensor_ids_partial},
        )

        dashboard = self.grafana.get_dashboard_by_name(self.event_name)

        self.assertTrue(dashboard)

        # Retrieve current panels
        try:
            panels = dashboard["dashboard"]["panels"]
        except KeyError:
            panels = []

        self.assertEquals(len(panels), 2)

        sensor_ids = []
        sensors = AGSensor.objects.all()
        for sensor in sensors:
            sensor_ids.append(sensor.id)

        # Post to reset the dashboard with all sensor panels
        self.client.post(
            reverse(
                self.config_reset_dashboard_url, kwargs={"gf_id": self.gfconfig.id}
            ),
            data={"dashboard_name": self.event_name},
        )

        dashboard = self.grafana.get_dashboard_by_name(self.event_name)

        self.assertTrue(dashboard)

        # Retrieve current panels
        try:
            panels = dashboard["dashboard"]["panels"]
        except KeyError:
            panels = []

        self.assertEquals(len(panels), 5)
        for sensor in sensors:
            self.assertEquals(panels[i]["title"], sensor.name)

    def test_delete_dashboard_single_gfconfig(self):
        # update dashboard with a subset of panels, then restore all panels by using
        # reset
        self.create_venue_and_event(self.event_name)

        # create a dashboard
        self.grafana.create_dashboard(self.event_name)

        # Post to update the dashboard with 2 sensor panels
        self.client.post(
            reverse(
                self.config_delete_dashboard_url, kwargs={"gf_id": self.gfconfig.id}
            ),
            data={"dashboard_name": self.event_name},
        )

        dashboard = self.grafana.get_dashboard_by_name(self.event_name)

        # No dashboard should exist with this name
        self.assertFalse(dashboard)

    # @TODO Add tests to handle multiple GFConfigs
