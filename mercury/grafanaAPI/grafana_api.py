import os
import json
import requests
from mercury.models import GFConfig

TOKEN = "eyJrIjoiV2NmTWF1aVZUb3F4aWNGS25qcXA3VU9ZbkdEelgxb1EiLCJuIjoia2V5IiwiaWQiOjF9"
HOST = "https://daisycrego.grafana.net"


class Grafana:
    def __init__(self):
        gf_config = GFConfig.objects.filter(gf_current=True).first()
        if gf_config:
            self.api_token = gf_config.gf_token
            self.hostname = gf_config.gf_host
        else:
            self.api_token = TOKEN
            self.hostname = HOST

        self.temp_file = "dashboard_output.json"
        self.auth_url = "api/auth/keys"
        self.dashboard_post_url = "api/dashboards/db"
        self.dashboard_get_url = "api/dashboards"
        self.home_dashboard_url = "api/dashboards/home"
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

        self.datasource = "Heroku PostgreSQL (sextants-telemetry)"  # needs to come
        # from dashboard after configuring postgres
        # self.uid = "XwC1wLXZz"  # needs to come from dashboard
        self.uid = "9UF7VluWz"

        # Default panel sizes
        self.base_panel_width = 15
        self.base_panel_height = 12

    # Still working on this
    def create_dashboard_get_uid(self):

        # Retrieve current dashboard
        os.system(
            f'curl -H "Authorization: Bearer {self.api_token}" '
            f"{self.home_dashboard_endpoint} > {self.temp_file}"
        )

        with open(f"{self.temp_file}") as f:
            dashboard_info = json.load(f)

        print(dashboard_info["dashboard"]["uid"])

        """
        dashboard_info["dashboard"]["uid"] = None
        dashboard_info["dashboard"]["title"] = "Sensors - TEST"
        updated_dashboard = self.create_dashboard_update_dict(dashboard_info, [], False)
        # POST updated dashboard with new panel
        authorization = f"Bearer {self.api_token}"
        headers = {"Content-Type": "application/json", "Authorization": authorization}

        requests.post(self.dashboard_post_endpoint, data=json.dumps(updated_dashboard),
                      headers=headers)
        """

    # Still working on this
    def get_api_token(self, endpoint="http://admin:admin@localhost:3000/api/auth/keys"):
        os.system(
            f"curl '{self.auth_endpoint}' - X POST - H \"Content-Type: "
            f'application/json"  - d {{"role":"Admin","name":"grafana_key"}}'
        )

    # Still working on this
    def configure_postgres_db(self):
        pass

    def get_dashboard_with_uid(self, dashboard_uid):
        """
        Retrieves dashboard dict for given dashboard uid

        :param dashboard_uid: uid of the target dashboard
        :return: dict of the current dashboard
        """
        # Retrieve current dashboard
        os.system(
            f'curl -H "Authorization: Bearer {self.api_token}" '
            f"{self.dashboard_get_endpoint}/uid/"
            f"{dashboard_uid} > {self.temp_file}"
        )

        with open(f"{self.temp_file}") as f:
            dashboard_dict = json.load(f)

        return dashboard_dict

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
            "datasource": self.datasource,
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

        # Extract attributes from existing dashboard
        id = dashboard_info["dashboard"]["id"]
        uid = dashboard_info["dashboard"]["uid"]
        title = dashboard_info["dashboard"]["title"]
        schema_version = dashboard_info["dashboard"]["schemaVersion"]
        style = dashboard_info["dashboard"]["style"]
        tags = dashboard_info["dashboard"]["tags"]
        templating = dashboard_info["dashboard"]["templating"]
        version = dashboard_info["meta"]["version"]
        folder_id = dashboard_info["meta"]["folderId"]

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
                "style": style,
                "tags": tags,
                "templating": templating,
                "folderId": folder_id,
                "overwrite": overwrite,
            }
        }

        return updated_dashboard

    def delete_grafana_panels(self, dashboard_uid):
        """

        Deletes all panels from dashboard with given uid.

        :param dashboard_uid: uid of dashboard to delete
        :return: None.
        """

        # Retrieve current dashboard dict
        dashboard_info = self.get_dashboard_with_uid(dashboard_uid)

        # Create updated dashboard dict with empty list of panels
        panels = []
        updated_dashboard = self.create_dashboard_update_dict(dashboard_info, panels)

        # POST updated dashboard with empty list of panels
        authorization = f"Bearer {self.api_token}"
        headers = {"Content-Type": "application/json", "Authorization": authorization}
        requests.post(
            self.dashboard_post_endpoint,
            data=json.dumps(updated_dashboard),
            headers=headers,
        )

    def add_grafana_panel(self, sensor, dashboard_uid):
        """
        :param sensor: Sensor object's sensor type will be used to create the
        SQL query for the new panel.
        :param dashboard_uid: UID of the target dashboard
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
        dashboard_info = self.get_dashboard_with_uid(dashboard_uid)

        # Retrieve current panels
        panels = dashboard_info["dashboard"]["panels"]

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
        authorization = f"Bearer {self.api_token}"
        headers = {"Content-Type": "application/json", "Authorization": authorization}
        requests.post(
            self.dashboard_post_endpoint,
            data=json.dumps(updated_dashboard),
            headers=headers,
        )
