import logging
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from mercury.forms import GFConfigForm, GFConfigFormUpdate, DashboardSensorPanelsForm
from mercury.models import GFConfig
from ag_data.models import AGEvent, AGSensor
from mercury.grafanaAPI.grafana_api import Grafana
from django.contrib import messages
from ..event_check import require_event_code, require_event_code_function
import os
from django.conf import settings
from django.utils.safestring import mark_safe

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)

GITHUB_DOCS_ROOT = settings.GITHUB_DOCS_ROOT
CONFIGURE_GRAFANA_HELP_DOC = "configure_grafana.md"


# Deprecated
# Sets the GFConfig's current status to True
@require_event_code_function
def update_config(request, gf_id=None):
    GFConfig.objects.all().update(gf_current=False)
    GFConfig.objects.filter(id=gf_id).update(gf_current=True)
    return redirect("/gfconfig")


@require_event_code_function
def delete_config(request, gf_id=None):
    config = GFConfig.objects.get(id=gf_id)

    # Create Grafana class to handle this GF instance
    grafana = Grafana(config)

    try:
        grafana.validate_credentials()
        grafana.delete_all_datasources()
        grafana.delete_all_dashboards()
    except ValueError as error:
        messages.error(request, f"Grafana instance not deleted: {error}")
    else:
        messages.success(request, f"Grafana instance deleted successfully")

    config.delete()

    return redirect("/gfconfig")


@require_event_code_function
def configure_dashboard(request, gf_id=None):
    config = GFConfig.objects.get(id=gf_id)

    # Prepare a dict with details for this GFConfig (GFConfig object,
    # list of dashboards/forms
    config_info = dict()
    config_info["config"] = config

    # Create Grafana class to handle this GF instance
    grafana = Grafana(config)

    try:
        grafana.validate_credentials()
        existing_events = grafana.get_all_events()
        current_dashboards = grafana.get_all_dashboards()

    except ValueError as error:
        messages.error(request, f"Cannot connect to Grafana: {error}")
        existing_events = []
        current_dashboards = []

    # Assemble a list of dicts w/: url, sensors, initialized sensor form,
    # and dashboard name

    # Retrieve missing events to pass to the context
    all_events = list(AGEvent.objects.all())
    event_names = [event.name for event in all_events]
    missing_events = list(set(all_events) - set(existing_events))

    # Prepare an array of dashboards & their sensors to send to the template
    dashboards = []

    for dashboard in current_dashboards:

        # if this dashboard corresponds to an event
        if dashboard["title"] in event_names:

            dashboard_dict = dict()
            # Get all currently used panels to initialize the form
            existing_sensors = grafana.get_all_sensors(dashboard["title"])

            # Set initial form data so that only existing sensors are checked
            sensor_form = DashboardSensorPanelsForm(
                initial={"sensors": existing_sensors}
            )

            # Retrieve the URL for this dashboard or ""
            dashboard_url = grafana.get_dashboard_url_by_name(dashboard["title"])
            if dashboard_url is None:
                dashboard_url = ""

            # Store everything in a list of dicts
            dashboard_dict["sensor_form"] = sensor_form
            dashboard_dict["dashboard_url"] = dashboard_url
            dashboard_dict["sensors"] = AGSensor.objects.all()
            dashboard_dict["name"] = dashboard["title"]

            dashboards.append(dashboard_dict)

    config_info["dashboards"] = dashboards
    config_info["missing_events"] = missing_events

    context = {"config": config_info}
    return render(request, "gf_dashboards.html", context)


@require_event_code_function
def update_dashboard(request, gf_id=None):
    gfconfig = GFConfig.objects.filter(id=gf_id).first()

    if gfconfig:
        grafana = Grafana(gfconfig)
        dashboard_name = request.POST.get("dashboard_name")
        sensors = request.POST.getlist("sensors")
        sensor_objects = []
        for sensor in sensors:
            sensor = AGSensor.objects.filter(uuid=sensor).first()
            sensor_objects.append(sensor)
        try:
            grafana.update_dashboard_panels(dashboard_name, sensor_objects)
            msg = "Successfully updated dashboard: {}".format(dashboard_name)
            messages.success(request, msg)
        except ValueError as error:
            messages.error(request, error)
    else:
        messages.error(
            request, "Unable to update dashboard, Grafana instance not found"
        )
    return redirect("/gfconfig/configure/{}".format(gf_id))


@require_event_code_function
def reset_dashboard(request, gf_id=None):
    gfconfig = GFConfig.objects.filter(id=gf_id).first()

    if gfconfig:
        grafana = Grafana(gfconfig)
        dashboard_name = request.POST.get("dashboard_name")
        sensors = AGSensor.objects.all()
        try:
            grafana.update_dashboard_panels(dashboard_name, sensors)
            msg = "Successfully reset dashboard: {}".format(dashboard_name)
            messages.success(request, msg)
        except ValueError as error:
            messages.error(request, error)
    else:
        messages.error(request, "Unable to reset dashboard, Grafana instance not found")
    return redirect("/gfconfig/configure/{}".format(gf_id))


@require_event_code_function
def delete_dashboard(request, gf_id=None):
    gfconfig = GFConfig.objects.filter(id=gf_id).first()

    if gfconfig:
        grafana = Grafana(gfconfig)
        dashboard_name = request.POST.get("dashboard_name")
        # try to delete the dashboard
        if grafana.delete_dashboard_by_name(dashboard_name) is False:
            messages.error(request, "Unable to delete dashboard")
        else:
            msg = "Successfully deleted dashboard: {}".format(dashboard_name)
            messages.success(request, msg)
    else:
        messages.error(
            request, "Unable to delete dashboard, Grafana instance not found"
        )
    return redirect("/gfconfig/configure/{}".format(gf_id))


@require_event_code_function
def create_dashboard(request, gf_id=None):
    gfconfig = GFConfig.objects.filter(id=gf_id).first()
    event_name = request.POST.get("selected_event_name")
    event = AGEvent.objects.filter(name=event_name).first()
    sensors = AGSensor.objects.all()

    if gfconfig and event:

        grafana = Grafana(gfconfig)

        try:
            grafana.create_dashboard(event.name)
            for sensor in sensors:
                grafana.add_panel(sensor, event)
            msg = "Successfully created dashboard: {}".format(event_name)
            messages.success(request, msg)
        except ValueError as error:
            messages.error(f"Unable to add dashboard to Grafana: {error}")

    return redirect("/gfconfig/configure/{}".format(gf_id))


def make_auth_url(gf_host, gf_username, gf_password):
    auth_http = "http://{}:{}@{}"
    auth_https = "https://{}:{}@{}"
    if gf_host.startswith("https"):
        auth_url = auth_https.format(gf_username, gf_password, gf_host[8:])
    elif gf_host.startswith("http"):
        auth_url = auth_http.format(gf_username, gf_password, gf_host[7:])
    else:
        auth_url = auth_http.format(gf_username, gf_password, gf_host)
    return auth_url


class GFConfigView(TemplateView):
    template_name = "gf_configs.html"

    @require_event_code
    def get(self, request, *args, **kwargs):
        # Retrieve all available GFConfigs
        current_configs = GFConfig.objects.all().order_by("id")

        # Initialize GFConfig Form and update form
        config_form = GFConfigForm(
            initial={"gf_name": "Local", "gf_host": "http://localhost:3000"}
        )
        config_form_update = GFConfigFormUpdate()

        configure_grafana_github_url = os.path.join(
            GITHUB_DOCS_ROOT, CONFIGURE_GRAFANA_HELP_DOC
        )

        # Pass dashboard data for each GFConfig and a GFConfig form to the template
        """
        The context contains:
        config_form: GFConfigForm object
        configs : [
            {
                "dashboards": [{
                    "sensor_form": DashboardSensorPanelsForm object
                    "url": ...
                    "sensors": QuerySet(Sensor object)
                    "name": "blah"
                }]
                "config": GFConfig object,
                "missing_events": QuerySet of AGEvents without dashboards
            },
            {...}
        ]
        """
        context = {
            "config_form": config_form,
            "configs": current_configs,
            "config_form_update": config_form_update,
            "configure_grafana_github_url": configure_grafana_github_url,
        }
        return render(request, self.template_name, context)

    @require_event_code
    def post(self, request, *args, **kwargs):
        if "submit" not in request.POST:
            return

        DB = settings.DATABASES
        gf_host = request.POST.get("gf_host")
        gf_name = request.POST.get("gf_name")
        gf_username = request.POST.get("gf_username")
        gf_password = request.POST.get("gf_password")
        gf_token = request.POST.get("gf_token")

        # check whether gf_host already in use
        existing_host = GFConfig.objects.filter(gf_host=gf_host)
        if "update-config" not in request.POST and existing_host:
            messages.error(
                request, "Hostname {} already in use".format(gf_host),
            )
            return redirect("/gfconfig")

        configure_grafana_github_url = os.path.join(
            GITHUB_DOCS_ROOT, CONFIGURE_GRAFANA_HELP_DOC
        )

        # user providing username/pasword, generate API key automatically
        if not gf_token:
            auth_url = make_auth_url(gf_host, gf_username, gf_password)
            try:
                gf_token = Grafana.create_api_key(
                    auth_url, "mercury-auto-admin", "Admin"
                )
            except ValueError as error:
                messages.error(
                    request,
                    mark_safe(
                        "Failed to create API token: {}. If this "
                        "problem persists, please provide "
                        "an admin API key directly with the 'Use API "
                        "Key' option in the `Add Grafana Host` form. "
                        'See <a target="_blank" '
                        'href="{}">Configure Grafana: How to Create an '
                        "API Token </a> to learn how to create an "
                        "API "
                        "key.".format(
                            error,
                            configure_grafana_github_url
                            + "#c-how-to-create-an-api-token",
                        )
                    ),
                )
                return redirect("/gfconfig")

        # the user is submitting an update form with username/password
        if "update-config" in request.POST and gf_username and gf_password:
            existing_host.update(
                gf_username=gf_username, gf_password=gf_password, gf_token=gf_token
            )
            messages.success(request, "Updated Grafana host: {}".format(gf_host))
            return redirect("/gfconfig")

        # new gfconfig record
        config_data = GFConfig(
            gf_name=gf_name,
            gf_host=gf_host,
            gf_username=gf_username,
            gf_password=gf_password,
            gf_token=gf_token,
            gf_db_host=DB["default"]["HOST"] + ":" + str(DB["default"]["PORT"]),
            gf_db_name=DB["default"]["NAME"],
            gf_db_username=DB["default"]["USER"],
            gf_db_pw=DB["default"]["PASSWORD"],
        )

        # Create Grafana instance with host and token
        grafana = Grafana(config_data)

        try:
            grafana.validate_credentials()
        except ValueError as error:
            messages.error(request, error)
            return redirect("/gfconfig")

        # the user is submitting an update form with a validated API key
        if "update-config" in request.POST:
            existing_host.update(gf_token=gf_token)
            messages.success(request, "Updated Grafana host: {}".format(gf_host))
            return redirect("/gfconfig")

        try:
            grafana.create_postgres_datasource()
        except ValueError as error:
            messages.error(request, error)

        try:
            config_data.gf_current = True
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
            messages.warning(request, f"Warning: {error}")

        messages.success(request, "Created Grafana Host: {}".format(gf_name))
        return redirect("/gfconfig")
