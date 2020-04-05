import logging
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from mercury.forms import GFConfigForm, DashboardSensorPanelsForm
from mercury.models import GFConfig
from ag_data.models import AGEvent, AGSensor
from mercury.grafanaAPI.grafana_api import Grafana
from django.contrib import messages
from django.conf import settings

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


# Sets the GFConfig's current status to True
def update_config(request, gf_id=None):
    GFConfig.objects.all().update(gf_current=False)
    GFConfig.objects.filter(id=gf_id).update(gf_current=True)
    return redirect("/gfconfig")


def delete_config(request, gf_id=None):
    GFConfig.objects.get(id=gf_id).delete()
    return redirect("/gfconfig")


class GFConfigView(TemplateView):

    template_name = "gf_configs.html"

    def get(self, request, *args, **kwargs):
        # Retrieve all available GFConfigs
        configs = GFConfig.objects.all().order_by("id")

        # Initialize a GFConfig Form
        config_form = GFConfigForm()

        # Prepare an array of dashboards & their sensors to send to the template
        dashboards = []

        # @TODO Provide a set of dashboards per GFConfig, have multiple views in
        # @TODO the template, 1 per GFConfig.
        config = configs[0]

        # Create Grafana class to handle this GF instance
        grafana = Grafana(config)
        # Get an array of all dashboards
        current_dashboards = grafana.get_all_dashboards()
        # Assemble a list of dicts w/: url, sensors, initialized sensor form,
        # and dashboard name
        for dashboard in current_dashboards:
            dashboard_dict = dict()

            # Get all currently used panels to initialize the form
            existing_sensors = grafana.get_all_sensors(dashboard["title"])

            # Set initial form data so that only existing sensors are checked
            sensor_form = DashboardSensorPanelsForm(
                initial={"sensors": existing_sensors}
            )

            # Retrieve the URL for this dashboard or ""
            url = grafana.get_dashboard_url_by_name(dashboard["title"])
            if url is None:
                url = ""

            # Store everything in a list of dicts
            dashboard_dict["sensor_form"] = sensor_form
            dashboard_dict["url"] = url
            dashboard_dict["sensors"] = AGSensor.objects.all()
            dashboard_dict["name"] = dashboard["title"]

            dashboards.append(dashboard_dict)

        # Pass dashboard data list, GFConfigs, and GFConfig form to the template
        context = {
            "config_form": config_form,
            "configs": configs,
            "dashboards": dashboards,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if "submit" in request.POST:
            DB = settings.DATABASES
            config_data = GFConfig(
                gf_name=request.POST.get("gf_name"),
                gf_host=request.POST.get("gf_host"),
                gf_token=request.POST.get("gf_token"),
                gf_db_host=DB["default"]["HOST"] + ":" + str(DB["default"]["PORT"]),
                gf_db_name=DB["default"]["NAME"],
                gf_db_username=DB["default"]["USER"],
                gf_db_pw=DB["default"]["PASSWORD"],
            )

            # Create Grafana instance with host and token
            grafana = Grafana(config_data)
            try:
                grafana.validate_credentials()
                config_data.gf_current = True
                # Only save the config if credentials were validated
                config_data.save()

                # If any events exist, add a dashboard for each event
                # If any sensors exist, add them to each event dashboard
                events = AGEvent.objects.all()
                sensors = AGSensor.objects.all()
                for event in events:
                    grafana.create_dashboard(event.name)
                    for sensor in sensors:
                        grafana.add_panel(sensor, event)

            except ValueError as error:
                messages.error(request, f"Grafana initial set up failed: {error}")

            try:
                grafana.create_postgres_datasource()
            except ValueError as error:
                messages.error(request, f"Datasource couldn't be created. {error}")

            configs = GFConfig.objects.all().order_by("id")
            config_form = GFConfigForm(request.POST)
            context = {"config_form": config_form, "configs": configs}
            return render(request, self.template_name, context)
