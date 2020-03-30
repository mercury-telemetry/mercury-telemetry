import os
import json
import requests
import string
import random

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
            self.database_hostname = gf_config.gf_host
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
        endpoint = os.path.join(
            self.hostname, "api/dashboards/db", name.lower().replace(" ", "-")
        )
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
            "jsonData": {"postgresVersion": 903, "sslmode": "require"},
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
        except KeyError:
            return False

    def add_panel(self, sensor, event, dashboard_uid):
        """

        Adds a new panel for the sensor based on its SensorType.
        The database for the new panel will be whichever database is currently in
        GFConfig. The panel will be placed in the next available slot on the dashboard.

        :param sensor: AGSensor object for this panel (panel will only display sensor
         data for this sensor type.
        :param event: Event object for this panel (panel will only display sensor
        data for this event)
        :param dashboard_uid: UID of the target dashboard

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

        # Retrieve current dashboard structure
        dashboard_info = self.get_dashboard_with_uid(dashboard_uid)

        if dashboard_info is None:
            raise ValueError("Dashboard uid not found.")

        # Retrieve current panels
        try:
            panels = dashboard_info["dashboard"]["panels"]
        except KeyError:
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

    def delete_all_panels(self, uid):
        """

        Deletes all panels from dashboard with given uid.

        :param uid: uid of dashboard to delete
        :return: None.
        """

        # Retrieve current dashboard dict
        dashboard_info = self.get_dashboard_with_uid(uid)

        # Create updated dashboard dict with empty list of panels
        panels = []
        updated_dashboard = self.create_dashboard_update_dict(dashboard_info, panels)

        # POST updated dashboard with empty list of panels
        headers = {"Content-Type": "application/json"}
        requests.post(
            self.urls["dashboard_post"],
            data=json.dumps(updated_dashboard),
            headers=headers,
            auth=("api_key", self.api_token),
        )

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
            "datasource": self.database_name,
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
    def create_dashboard_update_dict(self, dashboard_info, panels, overwrite=True):
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
            title = dashboard_info["dashboard"]["title"]
            schema_version = dashboard_info["dashboard"]["schemaVersion"]
            # style = dashboard_info["dashboard"]["style"]
            tags = dashboard_info["dashboard"]["tags"]
            # templating = dashboard_info["dashboard"]["templating"]
            version = dashboard_info["meta"]["version"]
            folder_id = dashboard_info["meta"]["folderId"]
        except KeyError:
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