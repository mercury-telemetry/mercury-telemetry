from django.test import TestCase
from django.urls import reverse
from mercury.models import EventCodeAccess, GFConfig
from ag_data.models import AGSensor, AGSensorType, AGEvent, AGVenue
from ag_data import simulator
from mercury.grafanaAPI.grafana_api import Grafana
import requests
import os
import datetime
import random
import string


# default host and token, use this if user did not provide anything
HOST = "https://mercurytests.grafana.net"
# this token has Admin level permissions
TOKEN = (
    "eyJrIjoiUm81MzlOUlRhalhGUFJ5OVVMNTZGTTZIdT"
    "dvVURDSzIiLCJuIjoiYXBpX2tleSIsImlkIjoxfQ=="
)
# this token has Editor level permissions
EDITOR_TOKEN = (
    "eyJrIjoibHlrZ2JWY0pnQk94b1YxSGYzd0NJ"
    "ZUdZa3JBeWZIT3QiLCJuIjoiZWRpdG9yX2tleSIsImlkIjoxfQ=="
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

    def create_gfconfig(self):
        config = GFConfig.objects.create(gf_host=HOST, gf_token=TOKEN, gf_current=True,)
        config.save()
        return config

    def create_event(self):
        venue = AGVenue.objects.create(
            name=self.test_venue_data["name"],
            description=self.test_venue_data["description"],
            latitude=self.test_venue_data["latitude"],
            longitude=self.test_venue_data["longitude"],
        )
        venue.save()

        event = AGEvent.objects.create(
            name=self.test_event_data["name"],
            date=self.test_event_data["date"],
            description=self.test_event_data["description"],
            venue_uuid=venue.uuid,
        )
        event.save()

        return event

    def setUp(self):
        self.login_url = "mercury:EventAccess"
        self.sensor_url = "mercury:sensor"
        self.event_url = "mercury:events"
        test_code = EventCodeAccess(event_code="testcode", enabled=True)
        test_code.save()
        # Login
        self._get_with_event_code(self.sensor_url, self.TESTCODE)

        # Create fresh grafana object
        self.grafana = Grafana(HOST, TOKEN)

        # Create random name to be used for event and datasource
        letters = string.ascii_lowercase
        self.event_name = "".join(random.choice(letters) for i in range(10))
        self.datasource_name = "".join(random.choice(letters) for i in range(10))

        # Clear existing dashboard and datasource
        self.grafana.delete_dashboard_by_name(self.event_name)
        self.grafana.delete_datasource_by_name(self.datasource_name)

    def tearDown(self):
        # Create fresh grafana instance (in case test invalidated any tokens, etc.)
        self.grafana = Grafana(HOST, TOKEN)

        # Clear all of the created dashboards
        self.grafana.delete_dashboard_by_name(self.event_name)
        self.grafana.delete_datasource_by_name(self.datasource_name)

    def _get_with_event_code(self, url, event_code):
        self.client.get(reverse(self.login_url))
        self.client.post(reverse(self.login_url), data={"eventcode": event_code})
        response = self.client.get(reverse(url))
        session = self.client.session
        return response, session

    def test_get_dashboard_exists(self):
        dashboard = self.grafana.create_dashboard(self.event_name)

        self.assertTrue(dashboard)

        uid = dashboard["uid"]

        fetched_dashboard = self.grafana.get_dashboard_with_uid(uid)

        self.assertTrue(fetched_dashboard)
        self.assertTrue(fetched_dashboard["meta"])
        self.assertTrue(fetched_dashboard["meta"]["slug"], self.event_name.lower())
        self.assertTrue(fetched_dashboard["dashboard"])
        self.assertTrue(fetched_dashboard["dashboard"]["uid"], uid)
        self.assertTrue(fetched_dashboard["dashboard"]["title"], self.event_name)

    def test_get_dashboard_fail(self):
        letters = string.ascii_lowercase
        uid = "".join(random.choice(letters) for i in range(10))

        fetched_dashboard = self.grafana.get_dashboard_with_uid(uid)

        self.assertFalse(fetched_dashboard)

    def test_create_grafana_dashboard_success(self):
        dashboard = self.grafana.create_dashboard(self.event_name)

        self.assertTrue(dashboard)

    def test_create_grafana_dashboard_verify_new_dashboard_contents(self):
        dashboard = self.grafana.create_dashboard(self.event_name)

        self.assertTrue(dashboard)
        self.assertEquals(dashboard["status"], "success")
        self.assertEquals(dashboard["slug"], self.event_name.lower())
        uid = dashboard["uid"]

        # confirm new dashboard can be queried from the API
        endpoint = os.path.join(self.grafana.endpoints["dashboard_uid"], uid)
        headers = {"Content-Type": "application/json"}
        response = requests.get(
            url=endpoint, headers=headers, auth=("api_key", self.grafana.api_token)
        )

        self.assertEquals(response.json()["dashboard"]["uid"], uid)
        self.assertEquals(response.json()["dashboard"]["title"], self.event_name)

    def test_create_grafana_dashboard_fail_authorization(self):
        self.grafana.api_token = "abcde"  # invalidate API token

        expected_message = "Invalid API key"
        with self.assertRaisesMessage(ValueError, expected_message):
            self.grafana.create_dashboard(self.event_name)

    def test_create_grafana_dashboard_fail_permissions(self):
        self.grafana.api_token = EDITOR_TOKEN  # API token with Editor permissions

        expected_message = "Access denied - check API permissions"
        with self.assertRaisesMessage(ValueError, expected_message):
            self.grafana.create_dashboard(self.event_name)

    def test_validate_credentials_success(self):
        self.assertTrue(self.grafana.validate_credentials())

    def test_validate_credentials_fail_authorization(self):
        self.grafana.api_token = "abcde"  # invalidate API token

        expected_message = "Grafana API validation failed: Invalid API key"
        with self.assertRaisesMessage(ValueError, expected_message):
            self.grafana.validate_credentials()

    def test_validate_credentials_fail_permissions(self):
        self.grafana.api_token = EDITOR_TOKEN  # API token with Editor permissions

        expected_message = (
            "Grafana API validation failed: Access denied - " "check API permissions"
        )
        with self.assertRaisesMessage(ValueError, expected_message):
            self.grafana.validate_credentials()

    def test_create_grafana_dashboard_fail_duplicate_title(self):
        dashboard = self.grafana.create_dashboard(self.event_name)
        self.assertTrue(dashboard)

        expected_message = "Dashboard with the same name already exists"
        with self.assertRaisesMessage(ValueError, expected_message):
            self.grafana.create_dashboard(self.event_name)

    def test_delete_grafana_dashboard(self):
        dashboard = self.grafana.create_dashboard(self.event_name)
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

    def test_delete_grafana_dashboard_fail(self):
        letters = string.ascii_lowercase
        uid = "".join(random.choice(letters) for i in range(10))

        # should return false if dashboard doesn't exist
        deleted_dashboard = self.grafana.delete_dashboard(uid)
        self.assertFalse(deleted_dashboard)

    def test_add_panel(self):
        dashboard = self.grafana.create_dashboard(self.event_name)
        self.assertTrue(dashboard)
        uid = dashboard["uid"]

        self.sim.createOrResetASensorTypeFromPresets(0)
        self.sim.createASensorFromPresets(0)
        self.sim.createAVenueFromPresets(0)
        self.sim.createAnEventFromPresets(0)
        events = AGEvent.objects.all()
        event = events[0]

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

        self.grafana.add_panel(sensor, event, uid)

        dashboard_info = self.grafana.get_dashboard_with_uid(uid)

        self.assertTrue(dashboard_info)
        self.assertTrue(dashboard_info["dashboard"])
        self.assertTrue(dashboard_info["dashboard"]["panels"])
        self.assertTrue(len(dashboard_info["dashboard"]["panels"]) == 1)
        self.assertTrue(
            dashboard_info["dashboard"]["panels"][0]["title"] == sensor.name
        )

    def test_add_multiple_panels(self):
        dashboard = self.grafana.create_dashboard(self.event_name)
        self.assertTrue(dashboard)
        uid = dashboard["uid"]

        self.sim.createAVenueFromPresets(0)
        self.sim.createAnEventFromPresets(0)
        events = AGEvent.objects.all()
        event = events[0]

        dashboard_info = self.grafana.get_dashboard_with_uid(uid)
        try:
            panels = dashboard_info["dashboard"]["panels"]
        except KeyError:
            panels = []
        self.assertTrue(len(panels) == 0)

        sensor_type1 = AGSensorType.objects.create(
            name=self.test_sensor_type,
            processing_formula=0,
            format=self.test_sensor_format,
        )
        sensor_type1.save()

        # create and add panels for multiple sensors with the same type
        for i in range(10):
            sensor = AGSensor.objects.create(
                name="".join([self.test_sensor_name, str(i)]), type_id=sensor_type1
            )
            sensor.save()

            self.grafana.add_panel(sensor, event, uid)

        dashboard_info = self.grafana.get_dashboard_with_uid(uid)

        self.assertTrue(dashboard_info)
        self.assertTrue(dashboard_info["dashboard"])
        self.assertTrue(dashboard_info["dashboard"]["panels"])
        self.assertTrue(len(dashboard_info["dashboard"]["panels"]) == 10)

        for i in range(10):
            name = "".join([self.test_sensor_name, str(i)])
            self.assertTrue(dashboard_info["dashboard"]["panels"][i]["title"] == name)

    def test_add_panel_fail_invalid_uid(self):
        letters = string.ascii_lowercase
        uid = "".join(random.choice(letters) for i in range(10))

        self.sim.createOrResetASensorTypeFromPresets(0)
        self.sim.createASensorFromPresets(0)
        self.sim.createAVenueFromPresets(0)
        self.sim.createAnEventFromPresets(0)
        events = AGEvent.objects.all()
        event = events[0]

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

        expected_message = "Dashboard uid not found."
        with self.assertRaisesMessage(ValueError, expected_message):
            self.grafana.add_panel(sensor, event, uid)

    def test_create_postgres_datasource(self):
        # create datasource
        self.grafana.create_postgres_datasource(self.datasource_name)

        # confirm that the datasource exists
        endpoint = os.path.join(
            self.grafana.endpoints["datasource_name"], self.datasource_name,
        )
        headers = {"Content-Type": "application/json"}
        response = requests.get(
            url=endpoint, headers=headers, auth=("api_key", self.grafana.api_token)
        )

        self.assertEquals(response.json()["name"], self.datasource_name)

    def test_create_datasource_fail_authorization(self):
        self.grafana.api_token = "abcde"  # invalidate API token

        expected_message = "Invalid API key"
        with self.assertRaisesMessage(ValueError, expected_message):
            self.grafana.create_postgres_datasource(self.datasource_name)

    def test_create_datasource_fail_permissions(self):
        self.grafana.api_token = EDITOR_TOKEN  # API token with Editor permissions

        expected_message = "Access denied - check API permissions"
        with self.assertRaisesMessage(ValueError, expected_message):
            self.grafana.create_postgres_datasource(self.datasource_name)

    def test_delete_postgres_datasource(self):
        # create the datasource
        self.grafana.create_postgres_datasource(self.datasource_name)

        # deleted should be true if delete_datasource_by_name returns true
        deleted = self.grafana.delete_datasource_by_name(self.datasource_name)
        self.assertTrue(deleted)

        # figure out whether the datasource was actually deleted
        endpoint = os.path.join(
            self.grafana.endpoints["datasource_name"], self.datasource_name,
        )
        headers = {"Content-Type": "application/json"}
        response = requests.get(
            url=endpoint, headers=headers, auth=("api_key", self.grafana.api_token)
        )

        self.assertTrue(response.json()["message"])
        self.assertEquals(response.json()["message"], "Data source not found")

    def test_create_event_creates_dashboard_no_panels(self):
        # create a GFConfig object (if one doesn't exist no dashboard would be created)
        self.create_gfconfig()

        self.grafana.create_postgres_datasource(self.datasource_name)

        # create a venue
        venue = AGVenue.objects.create(
            name=self.event_name,
            description=self.test_venue_data["description"],
            latitude=self.test_venue_data["latitude"],
            longitude=self.test_venue_data["longitude"],
        )
        venue.save()

        # send a post request to create an event (should trigger the creation of a
        # grafana dashboard of the same namee
        response = self.client.post(
            reverse(self.event_url),
            data={
                "submit-event": "",
                "name": self.event_name,
                "date": self.test_event_data["date"],
                "description": self.test_event_data["description"],
                "venue_uuid": venue.uuid,
            },
        )

        # if there are spaces in the name, Grafana will replace them with dashes
        # for the slug, which is what you use to query the grafana api by dashboard name
        endpoint = os.path.join(
            self.grafana.hostname,
            "api/dashboards/db",
            self.event_name.lower().replace(" ", "-"),
        )

        response = requests.get(url=endpoint, auth=("api_key", self.grafana.api_token))

        # confirm that a dashboard was created with the expected name
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()["dashboard"]["title"], self.event_name)

    def test_create_event_creates_dashboard_with_panel(self):
        # create a GFConfig object (if one doesn't exist no dashboard would be created)
        self.create_gfconfig()

        self.grafana.create_postgres_datasource(self.datasource_name)

        # create a venue
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

        # send a post request to create an event (should trigger the creation of a
        # grafana dashboard of the same namee
        response = self.client.post(
            reverse(self.event_url),
            data={
                "submit-event": "",
                "name": self.event_name,
                "date": self.test_event_data["date"],
                "description": self.test_event_data["description"],
                "venue_uuid": venue.uuid,
            },
        )

        # if there are spaces in the name, Grafana will replace them with dashes
        # for the slug, which is what you use to query the grafana api by dashboard name
        endpoint = os.path.join(
            self.grafana.hostname,
            "api/dashboards/db",
            self.event_name.lower().replace(" ", "-"),
        )

        response = requests.get(url=endpoint, auth=("api_key", self.grafana.api_token))

        # confirm that a dashboard was created with the expected name
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.json()["dashboard"]["title"], self.event_name)

        # confirm that the sql query for the created panel contains the event UUID
        dashboard_info = self.grafana.get_dashboard_with_uid(
            response.json()["dashboard"]["uid"]
        )

        # confirm that a the new dashboard can be queried and has panel with correct
        # title
        self.assertTrue(dashboard_info)
        self.assertTrue(dashboard_info["dashboard"])
        self.assertTrue(dashboard_info["dashboard"]["panels"])
        self.assertTrue(len(dashboard_info["dashboard"]["panels"]) == 1)
        self.assertTrue(
            dashboard_info["dashboard"]["panels"][0]["title"] == sensor.name
        )
