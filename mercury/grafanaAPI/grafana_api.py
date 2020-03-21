import os
import json
import requests
from mercury.models import GFConfig

TOKEN = "eyJrIjoiRTQ0cmNGcXRybkZlUUNZWmRvdFI0UlMwdFVYVUt3bzgiLCJuIjoia2V5IiwiaWQiOjF9"
HOST = "https://dbc291.grafana.net"
DASHBOARD_UID = "9UF7VluWz"
DB_GRAFANA_NAME = "Heroku PostgreSQL (sextants-telemetry)"
DB_HOSTNAME = "ec2-35-168-54-239.compute-1.amazonaws.com:5432"
DB_NAME = "d76k4515q6qv"
DB_USERNAME = "qvqhuplbiufdyq"
DB_PASSWORD = "f45a1cfe8458ff9236ead8a7943eba31dcef761471e0d6d62b043b4e3d2e10e5"


class Grafana:
    def __init__(self, host=None, token=None):
        gf_config = GFConfig.objects.filter(gf_current=True).first()
        if gf_config:
            self.hostname = gf_config.gf_host
            self.api_token = gf_config.gf_token
            self.uid = gf_config.gf_host
            self.database_hostname = gf_config.gf_host
            self.database_name = gf_config.gf_db_name
            self.database_username = gf_config.gf_db_username
            self.database_password = gf_config.gf_db_pw
            self.database_grafana_name = gf_config.gf_db_grafana_name
        else:
            # for test purposes, a test case should init this class with credentials
            self.api_token = token
            self.hostname = host
            self.uid = DASHBOARD_UID
            self.database_hostname = DB_HOSTNAME
            self.database_name = DB_NAME
            self.database_username = DB_USERNAME
            self.database_password = DB_PASSWORD
            self.database_grafana_name = DB_GRAFANA_NAME

        # self.uid = "XwC1wLXZz"  # needs to come from dashboard
        self.uid = "9UF7VluWz"

        self.temp_file = "dashboard_output.json"
        self.auth_url = "api/auth/keys"
        self.dashboard_post_url = "api/dashboards/db"
        self.dashboard_uid_url = "api/dashboards/uid"
        self.dashboard_get_url = "api/dashboards"
        self.home_dashboard_url = "api/dashboards/home"
        self.search_url = "api/search?"
        self.datasource_name_url = "api/datasources/name"

        self.search_endpoint = os.path.join(self.hostname, self.search_url)
        self.datasource_name_endpoint = os.path.join(
            self.hostname, self.datasource_name_url
        )

        self.dashboard_uid_endpoint = os.path.join(
            self.hostname, self.dashboard_uid_url
        )
        self.auth_endpoint = os.path.join(self.hostname, self.auth_url)
        self.dashboard_post_endpoint = os.path.join(
            self.hostname, self.dashboard_post_url
        )
        self.dashboard_get_endpoint = os.path.join(
            self.hostname, self.dashboard_get_url
        )
        self.home_dashboard_endpoint = os.path.join(
            self.hostname, self.home_dashboard_url
        )

        # Default panel sizes
        self.base_panel_width = 15
        self.base_panel_height = 12

    def delete_all_dashboards(self):
        tag_search_endpoint = os.path.join(self.search_endpoint)
        headers = {"Content-Type": "application/json"}
        response = requests.get(
            url=tag_search_endpoint, auth=("api_key", self.api_token), headers=headers
        )

        dashboards = response.json()
        if len(dashboards) > 0:
            for dashboard in dashboards:
                self.delete_dashboard(dashboard["uid"])

    # Locates dashboard and deletes if exists. Returns true if successful else false.
    def delete_dashboard(self, uid):
        dashboard_endpoint = os.path.join(self.dashboard_uid_endpoint, uid)
        response = requests.delete(
            url=dashboard_endpoint, auth=("api_key", self.api_token)
        )

        if "deleted" not in response.json()["message"]:
            return False
        return True

    # TODO: Handle error case where title is already taken
    # Create a new Grafana dashboard. returns an object with details on new
    # dashboard or error message(s)
    # Example success output
    # eg {  'id': 4,
    #       'slug':
    #       'sensors',
    #       'status':
    #       'success',
    #       'uid': 'GjrBC6uZz',
    #       'url': '/d/GjrBC6uZz/sensors',
    #       'version': 1
    # }
    # Returns true if the dashboard was created, false otherwise
    def create_dashboard(self, title="Sensors"):
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

        response = requests.post(
            url=self.dashboard_post_endpoint,
            auth=("api_key", self.api_token),
            json=dashboard_base,
        )

        post_output = response.json()

        try:
            post_output["id"]
            return post_output
        except KeyError:
            if "Access denied" in post_output["message"]:
                raise ValueError("Access denied - check hostname and API token")
            elif "A dashboard with the same name in the folder already exists" in \
                    post_output["message"]:
                return None
            else:
                raise ValueError("Create_dashboard() failed: " + post_output["message"])

    # Returns true if datasource was deleted, false otherwise
    def delete_datasource_by_name(self, name):
        headers = {"Content-Type": "application/json"}
        endpoint = os.path.join(self.hostname, "api/datasources/name", name)
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

    def create_postgres_datasource(self):
        db = {
            "id": None,
            "orgId": None,
            "name": self.database_grafana_name,
            "type": "postgres",
            "access": "proxy",
            "url": self.database_hostname,
            "password": self.database_password,
            "user": self.database_username,
            "database": self.database_name,
            "basicAuth": False,
            "jsonData": {"postgresVersion": 903, "sslmode": "require"},
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(
            url=os.path.join(self.hostname, "api/datasources"),
            headers=headers,
            json=db,
            auth=("api_key", self.api_token),
        )

        datasource = response.json()
        try:
            if datasource["message"] == "Datasource added":
                return datasource
            elif "Access denied" in datasource["message"]:
                raise ValueError("Access denied - check hostname and API token")
            else:
                raise ValueError(
                    "Create_postgres_datasource() failed: " + datasource["message"]
                )
        except KeyError:
            raise ValueError("Create_postgres_datasource() failed: " + datasource)

    def get_dashboard_with_uid(self, uid):
        """
        Retrieves dashboard dict for given dashboard uid

        :param uid: uid of the target dashboard
        :return: dict of the current dashboard
        """
        headers = {"Content-Type": "application/json"}
        endpoint = os.path.join(self.dashboard_uid_endpoint, uid)
        response = requests.get(
            url=endpoint, headers=headers, auth=("api_key", self.api_token)
        )

        if "dashboard" in response.json():
            return response.json()
        else:
            print(response.json())
            return None

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
            "datasource": self.database_grafana_name,
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

    def delete_grafana_panels(self, uid):
        """

        Deletes all panels from dashboard with given uid.

        :param uid: uid of dashboard to delete
        :return: None.
        """

        # Retrieve current dashboard dict
        self.get_dashboard_with_uid(uid)

        # Create updated dashboard dict with empty list of panels
        panels = []
        updated_dashboard = self.create_dashboard_update_dict(dashboard_info, panels)

        # POST updated dashboard with empty list of panels
        authorization = f"Bearer {self.api_token}"
        authorization = f"Bearer {self.api_token}"
        headers = {"Content-Type": "application/json", "Authorization": authorization}
        requests.post(
            self.dashboard_post_endpoint,
            data=json.dumps(updated_dashboard),
            headers=headers,
        )

    def add_grafana_panel(self, sensor, uid):
        """
        :param sensor: Sensor object's sensor type will be used to create the
        SQL query for the new panel.
        :param uid: UID of the target dashboard
        :return: New panel with SQL query based on sensor type
        will be added to dashboard.
        """

        if not sensor:
            return

        # Retrieve id, title, and fields from AGSensor object
        sensor_id = sensor.id
        title = sensor.name
        field_dict = sensor.type_id.format
        field_array = []
        for field in field_dict:
            field_array.append(field)

        # Retrieve current dashboard structure
        dashboard_info = self.get_dashboard_with_uid(uid)

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
        WHERE $__timeFilter(\"timestamp\") AND sensor_id_id={sensor_id}\n
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
        requests.post(
            self.dashboard_post_endpoint,
            data=json.dumps(updated_dashboard),
            headers=headers,
            auth=("api_key", self.api_token),
        )
