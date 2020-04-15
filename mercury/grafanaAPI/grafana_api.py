import os
import json
import requests
import string
import random
from ag_data.models import AGSensor, AGEvent

TOKEN = "eyJrIjoiRTQ0cmNGcXRybkZlUUNZWmRvdFI0UlMwdFVYVUt3bzgiLCJuIjoia2V5IiwiaWQiOjF9"
HOST = "https://dbc291.grafana.net"
DB_HOSTNAME = "ec2-35-168-54-239.compute-1.amazonaws.com:5432"
DB_NAME = "d76k4515q6qv"
DB_USERNAME = "qvqhuplbiufdyq"
DB_PASSWORD = "f45a1cfe8458ff9236ead8a7943eba31dcef761471e0d6d62b043b4e3d2e10e5"


class Grafana:
    def __init__(self, gf_config=None):
        """

        Initialize parameters needed to use the API: hostname, admin-level API token,
        and the following postgres credentials:
        - hostname
        - grafana_name
        - name
        - username
        - password
        Initialize Grafana API endpoints based on hostname.

        :param host: Grafana hostname, e.g. https://dbc291.grafana.net
        :param token: API key with admin-level permissions
        """
        if gf_config:
            self.hostname = gf_config.gf_host
            self.api_token = gf_config.gf_token
            self.database_hostname = gf_config.gf_db_host
            self.database_name = gf_config.gf_db_name
            self.database_username = gf_config.gf_db_username
            self.database_password = gf_config.gf_db_pw
        else:
            # for test purposes
            self.hostname = HOST
            self.api_token = TOKEN
            self.database_hostname = DB_HOSTNAME
            self.database_name = DB_NAME
            self.database_username = DB_USERNAME
            self.database_password = DB_PASSWORD

        # Grafana API endpoints constructed with hostname + url
        self.endpoints = {
            "dashboards": os.path.join(self.hostname, "api/dashboards/db"),
            "dashboard_uid": os.path.join(self.hostname, "api/dashboards/uid"),
            "datasources": os.path.join(self.hostname, "api/datasources"),
            "datasource_name": os.path.join(self.hostname, "api/datasources/name"),
        }

        # Default panel sizes
        self.base_panel_width = 15
        self.base_panel_height = 12

    def create_safe_string(self, input):
        """
        Reformats the input string to be lowercase and with spaces replaced by '-'.
        :param input: string
        :return: reformatted string
        """
        return input.strip().lower().replace(" ", "-")

    def generate_random_string(self, length):
        """
        Generates a random string of letters of given length.
        :param length: Target length for the random string
        :return: Random string
        """
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for i in range(length))

    def validate_credentials(self):
        """
        Validates current set of grafana API credentials (hostname and API token).
        Attempts to create and delete a dashboard. If there is any failure,
        a ValueError will be raised which can be caught by the caller. If the
        dashboard is created successfully, True is returned.
        :return: True if a dashboard could be created using these API credentials,
        False otherwise.
        """
        dashboard_name = self.generate_random_string(10)

        try:
            self.create_dashboard(dashboard_name)
        except ValueError as error:
            raise ValueError(f"Grafana API validation failed: {error}")

        self.delete_dashboard_by_name(dashboard_name)

        return True

    def get_all_dashboards(self):
        """
        :return: A list of all existing dashboards (excluding the home dashboard).
        If an empty list is returned, there are no dashboards except for the home
        dashboard.
        """

        endpoint = os.path.join(self.hostname, "api/search/")
        response = requests.get(url=endpoint, auth=("api_key", self.api_token))
        json = response.json()
        return json

    def get_dashboard_by_name(self, event_name):
        """
        :param event_name: Event name used for the target dashboard.
        :return: Returns a JSON response from the API with basic details if a
        dashboard was found with this name, including a JSON representation of the
        dashboard and its panels, False otherwise.
        """
        # If there are spaces in the name, the GF API will replace them with dashes
        # to generate the "slug". A slug can be used to query the API.
        formatted_event_name = self.create_safe_string(event_name)

        endpoint = os.path.join(
            self.hostname, "api/dashboards/db", formatted_event_name
        )
        response = requests.get(url=endpoint, auth=("api_key", self.api_token))

        if "dashboard" in response.json():
            return response.json()
        else:
            return None

    def get_dashboard_url_by_name(self, name):
        search_name = self.create_safe_string(name)

        dashboard = self.get_dashboard_by_name(search_name)
        if dashboard:
            endpoint = dashboard["meta"]["url"].strip("/")
            url = os.path.join(self.hostname, endpoint)
        else:
            url = None

        return url

    def get_dashboard_with_uid(self, uid):
        """
        :param uid: uid of the target dashboard
        :return:
        Returns dashboard dictionary for given uid or None if no dashboard was found.
        e.g. {
            'meta':
                {
                    ...
                    'slug': 'bar',
                    'url': '/d/nJ1Yj49Zk/bar',
                    'version': 1,
                    'folderId': 0,
                    ...
                },
            'dashboard': {
                'id': 623,
                'schemaVersion': None,
                'tags': ['templated'],
                'timezone': 'browser',
                'title': 'Bar',
                'uid': 'nJ1Yj49Zk',
                'version': 1
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        endpoint = os.path.join(self.endpoints["dashboard_uid"], uid)
        response = requests.get(
            url=endpoint, headers=headers, auth=("api_key", self.api_token)
        )

        if "dashboard" in response.json():
            return response.json()
        else:
            return None

    def create_dashboard(self, title="Sensors"):
        """
        :param title: Name for the new dashboard.
        :return: Returns dictionary of dashboard metadata if dashboard was created.
        E.g.
        {   'id': 4,
            'slug': 'sensors',
            'status': 'success',
            'uid': 'GjrBC6uZz',
            'url': '/d/GjrBC6uZz/sensors',
            'version': 1
        }
        Raises ValueError otherwise:
        - Access denied - check API permissions
        - Invalid API key
        - Dashboard with the same name already exists
        """

        # Grafana API expects a dashboard object of this structure to be posted
        # to create a new dashboard
        dashboard_base = {
            "dashboard": {
                "id": None,
                "uid": None,
                "title": title,
                "tags": ["templated"],
                "timezone": "browser",
                "schemaVersion": None,
                "version": 0,
            },
            "folderId": 0,
            "overwrite": False,
        }

        # Prepare post request
        response = requests.post(
            url=self.endpoints["dashboards"],
            auth=("api_key", self.api_token),
            json=dashboard_base,
        )

        # Convert response to json
        post_output = response.json()

        # This will contain either a "message" if there was an error or an object
        # describing the new dashboard:
        #
        # { 'message': 'Invalid API key'}
        #
        # { 'id': 4,
        #   'slug': 'sensors',
        #   'status': 'success',
        #   'uid': 'GjrBC6uZz',
        #   'url': '/d/GjrBC6uZz/sensors',
        #   'version': 1
        # }

        id = post_output.get("id")  # Set to None if post_output has no "id"

        # If a dashboard was created, return the metadata
        if id:
            return post_output
        # If a dashboard wasn't created, inspect the error message and throw
        # a ValueError
        else:
            # Set to None if post_output has no "message"
            error_message = post_output.get("message")

            # Raise appropriate ValueError depending on the error message
            # If this is a novel error, raise a generic message
            if error_message:
                if "Access denied" in error_message:
                    raise ValueError("Access denied - check API permissions")
                elif "Invalid API key" in error_message:
                    raise ValueError("Invalid API key")
                elif (
                    "A dashboard with the same name in the folder already exists"
                    in error_message
                ):
                    raise ValueError("Dashboard with the same name already exists")
                else:
                    raise ValueError("Create_dashboard() failed: " + error_message)

    def delete_dashboard(self, uid):
        """
        Deletes the dashboard with target uid.

        :param uid: UID of the target dashboard.
        :return: Returns True if the dashboard was deleted successfully. Returns
        False otherwise (e.g. if the operation fails OR if no dashboard with the UID
        exists).
        """
        # Send a DELETE request to the delete api endpoint for the target uid
        dashboard_endpoint = os.path.join(self.endpoints["dashboard_uid"], uid)
        response = requests.delete(
            url=dashboard_endpoint, auth=("api_key", self.api_token)
        )

        # Response will contain "deleted" if the dashboard was deleted
        if "deleted" in response.json()["message"]:
            return True
        return False

    def delete_dashboard_by_name(self, name):
        search_name = self.create_safe_string(name)
        endpoint = os.path.join(self.hostname, "api/dashboards/db", search_name)
        response = requests.get(url=endpoint, auth=("api_key", self.api_token))

        dashboard = response.json().get("dashboard")
        if dashboard:
            return self.delete_dashboard(dashboard["uid"])
        else:
            return False

    def create_postgres_datasource(self, title="Datasource"):
        """
        Creates a new postgres datasource with the provided credentials:
        - Grafana name
        - Hostname
        - Database name
        - Username
        - Password
        :return:

        Returns an object with the datasource metadata if the datasource was created.

        Raises a ValueError if the request returns an error message, e.g.:
        - Access denied - check hostname and API token
        - Datasource with the same name already exists

        """
        if self.database_password == "":
            require_ssl = "disable"
        else:
            require_ssl = "require"

        db = {
            "id": None,
            "orgId": None,
            "name": title,
            "type": "postgres",
            "access": "proxy",
            "url": self.database_hostname,
            "password": self.database_password,
            "user": self.database_username,
            "database": self.database_name,
            "basicAuth": False,
            "isDefault": True,
            "jsonData": {"postgresVersion": 903, "sslmode": require_ssl},
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(
            url=self.endpoints["datasources"],
            headers=headers,
            json=db,
            auth=("api_key", self.api_token),
        )

        datasource = response.json()

        message = datasource.get("message")
        if message is None:
            raise ValueError("Response contains no message")
        if "Datasource added" in message:
            return datasource
        elif "Data source with same name already exists" in message:
            raise ValueError("Datasource with the same name already exists")
        elif "Permission denied" in message:
            raise ValueError("Access denied - check API permissions")
        elif "Invalid API key" in message:
            raise ValueError("Invalid API key")
        else:
            raise ValueError(f"Create_postgres_datasource() failed: {message}")

    def delete_datasource_by_name(self, name):
        """

        :param name: Name of the database to delete
        :return: Returns True if datasource was deleted, False otherwise
        """
        headers = {"Content-Type": "application/json"}
        endpoint = os.path.join(self.endpoints["datasource_name"], name)
        response = requests.delete(
            url=endpoint, headers=headers, auth=("api_key", self.api_token)
        )
        json = response.json()
        try:
            if json["message"] == "Data source deleted":
                return True
            else:
                return False
        except (KeyError, TypeError):
            return False

    def update_dashboard_title(self, event, title):
        """
        :param event: Event to update
        :param title: New title of the dashboard
        :return:
        If a dashboard exists with that title, the title is updated.
        Returns False if no update was performed
        Raises ValueError if there is an error updating the dashboard.
        Returns JSON response if status = "success"
        """

        if event.name == title:
            return False

        dashboard = self.get_dashboard_by_name(event.name)

        if dashboard is None:
            return False

        # Retrieve current panels
        try:
            panels = dashboard["dashboard"]["panels"]
        except (KeyError, TypeError):
            panels = []

        # Create updated dashboard dict with updated list of panels
        updated_dashboard = self.create_dashboard_update_dict(
            dashboard, panels, True, title
        )

        # POST updated dashboard
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            self.endpoints["dashboards"],
            data=json.dumps(updated_dashboard),
            headers=headers,
            auth=("api_key", self.api_token),
        )

        try:
            if response.json()["status"] != "success":
                raise ValueError(f"Event dashboard {event.name} not updated to {title}")
            return response.json()
        except KeyError as error:
            raise ValueError(f"Event dashboard {event.name} not updated: {error}")

    def create_panel_query(self, sensor, event):
        field_dict = sensor.type_id.format
        field_array = []
        for field in field_dict:
            field_array.append(field)

        # Build fields portion of SELECT query (select each field)
        fields_query = ""
        if len(field_array):
            for i in range(0, len(field_array) - 1):
                fields_query += f"value->'{field_array[i]}' AS {field_array[i]},\n"
            fields_query += f"value->'{field_array[-1]}' AS {field_array[-1]}"

        # Build SQL query
        panel_sql_query = f"""
                SELECT \"timestamp\" AS \"time\",
                {fields_query}
                FROM ag_data_agmeasurement
                WHERE $__timeFilter(\"timestamp\") AND sensor_id_id={sensor.id} AND
                "event_uuid_id"='{event.uuid}' \n
                ORDER BY timestamp
                """
        return panel_sql_query

    def add_panel(self, sensor, event):
        """

        Adds a new panel for the sensor based on its SensorType.
        The database for the new panel will be whichever database is currently in
        GFConfig. The dashboard for the new panel will be the dashboard with the
        same name as the event.
        The panel will be placed in the next available slot on the dashboard.

        :param sensor: AGSensor object for this panel (panel will only display sensor
         data for this sensor type.
        :param event: Event object for this panel (panel will only display sensor
        data for this event)

        :return: New panel with SQL query based on sensor type
        will be added to dashboard.
        """

        # Retrieve id, title, and fields from AGSensor object
        sensor_id = sensor.id
        title = sensor.name
        field_dict = sensor.type_id.format
        field_array = []
        for field in field_dict:
            field_array.append(field)

        # Find dashboard uid for event
        dashboard_info = self.get_dashboard_by_name(event.name)

        if dashboard_info is None:
            raise ValueError("Dashboard not found for this event.")

        # Retrieve current panels
        try:
            panels = dashboard_info["dashboard"]["panels"]
        except (KeyError, TypeError):
            panels = []

        # If first panel
        if len(panels) == 0:
            new_panel_id = 0  # id = 0
            x = 0  # col = 0
            y = 0  # row = 0
        # Otherwise, determine (a) left/right col and (b) row
        else:
            row = (len(panels) + 1) % 2
            y = row * self.base_panel_height

            # even-numbered panels are in right col
            if (len(panels) + 1) % 2 == 0:
                x = self.base_panel_width
            # other panels in left col
            else:
                x = 0

            new_panel_id = panels[-1]["id"] + 1

        # Build fields portion of SELECT query (select each field)
        fields_query = ""
        if len(field_array):
            for i in range(0, len(field_array) - 1):
                fields_query += f"value->'{field_array[i]}' AS {field_array[i]},\n"
            fields_query += f"value->'{field_array[-1]}' AS {field_array[-1]}"

        # Build SQL query
        panel_sql_query = f"""
        SELECT \"timestamp\" AS \"time\",
        {fields_query}
        FROM ag_data_agmeasurement
        WHERE $__timeFilter(\"timestamp\") AND sensor_id_id={sensor_id} AND
        "event_uuid_id"='{event.uuid}' \n
        """

        # Build a panel dict for the new panel
        panel = self.create_panel_dict(
            new_panel_id, field_array, panel_sql_query, title, x, y
        )

        # Add new panel to list of panels
        panels.append(panel)

        # Create updated dashboard dict with updated list of panels
        updated_dashboard = self.create_dashboard_update_dict(dashboard_info, panels)

        # POST updated dashboard
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            self.endpoints["dashboards"],
            data=json.dumps(updated_dashboard),
            headers=headers,
            auth=("api_key", self.api_token),
        )

        try:
            if response.json()["status"] != "success":
                raise ValueError(f"Sensor panel not added: {sensor.name}")
        except KeyError as error:
            raise ValueError(f"Sensor panel not added: {error}")

    def update_panel(self, event, current_sensor_name, new_sensor):
        # Retrieve current panels
        dashboard_info = self.get_dashboard_by_name(event.name)

        if dashboard_info is None:
            return False

        try:
            panels = dashboard_info["dashboard"]["panels"]
        except (KeyError, TypeError):
            panels = []

        if not panels:
            return False

        # Find the target panel and update it
        for panel in panels:
            if panel["title"] == current_sensor_name:
                panel["title"] = new_sensor.name
                panel["targets"][0]["rawSql"] = self.create_panel_query(
                    new_sensor, event
                )

        # Create updated dashboard dict with updated list of panels
        updated_dashboard = self.create_dashboard_update_dict(dashboard_info, panels)

        # POST updated dashboard
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            self.endpoints["dashboards"],
            data=json.dumps(updated_dashboard),
            headers=headers,
            auth=("api_key", self.api_token),
        )

        try:
            if response.json()["status"] != "success":
                raise ValueError(f"Sensor panel not updated: {new_sensor.name}")
        except KeyError as error:
            raise ValueError(f"Sensor panel not updated: {error}")

    def delete_panel(self, panel_name, event):

        # Retrieve current panels
        dashboard_info = self.get_dashboard_by_name(event.name)

        if dashboard_info is None:
            return False

        try:
            panels = dashboard_info["dashboard"]["panels"]
        except (KeyError, TypeError):
            panels = []

        # Build list of new panels, excluding any panel with title = name
        if not panels:
            return False

        new_panels = [
            panel for panel in panels if panel["title"].lower() != panel_name.lower()
        ]

        # Create updated dashboard dict with updated list of panels
        updated_dashboard = self.create_dashboard_update_dict(
            dashboard_info, new_panels
        )

        # POST updated dashboard
        headers = {"Content-Type": "application/json"}
        response = requests.post(
            self.endpoints["dashboards"],
            data=json.dumps(updated_dashboard),
            headers=headers,
            auth=("api_key", self.api_token),
        )

        try:
            if response.json()["status"] != "success":
                raise ValueError(f"Sensor panel not deleted: {panel_name}")
        except KeyError as error:
            raise ValueError(f"Sensor panel not deleted: {error}")

    def delete_all_panels_by_dashboard_name(self, name):
        """

        Deletes all panels from dashboard with given name.

        :param name: name of dashboard to delete
        :return: None.
        """

        # Retrieve current dashboard dict
        dashboard_info = self.get_dashboard_by_name(name)

        # Create updated dashboard dict with empty list of panels
        panels = []
        updated_dashboard = self.create_dashboard_update_dict(dashboard_info, panels)

        # POST updated dashboard
        headers = {"Content-Type": "application/json"}
        requests.post(
            self.endpoints["dashboards"],
            data=json.dumps(updated_dashboard),
            headers=headers,
            auth=("api_key", self.api_token),
        )

    # TODO For each sensor in sensors, check if the sensor is already found in the
    #  dashboard. If it isn't, add a new panel. If it already exists, check what is
    #  different - avoid overwriting style changes
    def update_dashboard_panels(self, dashboard_name, sensors=[]):
        """
        Updates the dashboard with title=`dashboard_name` so that it displays sensor
        panels based on the ones in `sensors`. If `sensors` is empty, panels will be
        cleared from the dashboard.

        :param dashboard_name: Name of dashboard to reset.
        :param sensors: Optional list of sensors, if provided sensor panels will be
        added.
        :return: N/a.
        """
        # remove all panels
        self.delete_all_panels_by_dashboard_name(dashboard_name)

        # retrieve event object
        event = AGEvent.objects.filter(name=dashboard_name).first()

        if event:
            # add new set of panels if provided
            for sensor in sensors:
                self.add_panel(sensor, event)
        else:
            raise ValueError(
                "Unable to locate event with dashboard name: " + dashboard_name
            )

    def get_all_events(self):
        dashboards = self.get_all_dashboards()

        events = []

        for dashboard in dashboards:
            dashboard_title = dashboard["title"]
            event = AGEvent.objects.filter(name=dashboard_title).first()
            if event:
                events.append(event)

        return events

    def get_all_sensors(self, dashboard_name):
        """

        :param dashboard_name: Name of the target dashboard
        :return: Returns a list of all sensor objects which currently exist as panels
        in the dashboard.

        """
        # Retrieve the current dashboard
        dashboard = self.get_dashboard_by_name(dashboard_name)

        try:
            dashboard = dashboard["dashboard"]
            panels = dashboard["panels"]
        except (KeyError, TypeError):
            panels = []

        sensor_names = []
        for panel in panels:
            sensor_names.append(panel["title"])

        sensors = []
        for name in sensor_names:
            sensor = AGSensor.objects.filter(name=name).first()
            sensors.append(sensor)

        return sensors

    # Helper method for add_panel
    def create_panel_dict(self, panel_id, fields, panel_sql_query, title, x, y):
        """
        Creates a panel dict which can be added to an updated dashboard dict and
        posted to the Create/Update Dashboard API endpoint

        :param panel_id: id for the new panel
        :param fields: array of field names
        :param panel_sql_query: SQL query for new panel
        :param title: title of new panel
        :param x: coordinates of new panel
        :param y: coordinates of new panel
        :return:
        """
        if len(fields) == 0:
            return  # error
        first_field = fields[0]

        panel = {
            "aliasColors": {},
            "bars": False,
            "dashLength": 10,
            "dashes": False,
            "datasource": "Datasource",
            "fill": 1,
            "fillGradient": 0,
            "gridPos": {"h": 9, "w": 12, "x": x, "y": y},
            "hiddenSeries": False,
            "id": panel_id,
            "legend": {
                "avg": False,
                "current": False,
                "max": False,
                "min": False,
                "show": True,
                "total": False,
                "values": False,
            },
            "lines": True,
            "linewidth": 1,
            "nullPointMode": "null",
            "options": {"dataLinks": []},
            "percentage": False,
            "pointradius": 2,
            "points": False,
            "renderer": "flot",
            "seriesOverrides": [],
            "spaceLength": 10,
            "stack": False,
            "steppedLine": False,
            "targets": [
                {
                    "format": "table",
                    "group": [],
                    "metricColumn": f"value->'{first_field}'",  # handle this
                    "rawQuery": True,
                    "rawSql": panel_sql_query,
                    "refId": "A",
                    "select": [[{"params": ["sensor_id_id"], "type": "column"}]],
                    "table": "ag_data_agmeasurement",
                    "timeColumn": "sensor_id_id",
                    "timeColumnType": "int4",
                    "where": [
                        {"name": "$__unixEpochFilter", "params": [], "type": "macro"}
                    ],
                }
            ],
            "thresholds": [],
            "timeFrom": None,
            "timeRegions": [],
            "timeShift": None,
            "title": title,
            "tooltip": {"shared": None, "sort": 0, "value_type": "individual"},
            "type": "graph",
            "xaxis": {
                "buckets": None,
                "mode": "time",
                "name": None,
                "show": True,
                "values": [],
            },
            "yaxes": [
                {
                    "format": "short",
                    "label": None,
                    "logBase": 1,
                    "max": None,
                    "min": None,
                    "show": True,
                },
                {
                    "format": "short",
                    "label": None,
                    "logBase": 1,
                    "max": None,
                    "min": None,
                    "show": True,
                },
            ],
            "yaxis": {"align": False, "alignLevel": None},
        }
        return panel

    # Helper method for add_panel
    def create_dashboard_update_dict(
        self, dashboard_info, panels, overwrite=True, title=None
    ):
        """
        Creates dashboard update dict with the provided dashboard_info dict and
        panels array. Can be posted to Create/Update Dashboard API endpoint to either
        create or update a dashboard.

        :param dashboard_info: dict of current dashboard
        :param panels: array of panels to add to dashboard
        :param overwrite: True if updating an existing dashboard
        :return: dict which can be posted to Create/Update Dashboard API endpoint
        """

        try:
            # Extract attributes from existing dashboard
            id = dashboard_info["dashboard"]["id"]
            uid = dashboard_info["dashboard"]["uid"]
            title = title if title else dashboard_info["dashboard"]["title"]
            schema_version = dashboard_info["dashboard"]["schemaVersion"]
            # style = dashboard_info["dashboard"]["style"]
            tags = dashboard_info["dashboard"]["tags"]
            # templating = dashboard_info["dashboard"]["templating"]
            version = dashboard_info["meta"]["version"]
            folder_id = dashboard_info["meta"]["folderId"]
        except (KeyError, TypeError):
            raise ValueError(f"dashboard_info object is invalid: {dashboard_info}")

        # Prepare updated_dashboard object
        updated_dashboard = {
            "dashboard": {
                "id": id,
                "uid": uid,
                "title": title,
                "version": version,
                "panels": panels,
                "refresh": False,
                "schemaVersion": schema_version,
                "style": "dark",
                "tags": tags,
                "templating": {"list": []},
                "folderId": folder_id,
                "overwrite": overwrite,
            }
        }

        return updated_dashboard
