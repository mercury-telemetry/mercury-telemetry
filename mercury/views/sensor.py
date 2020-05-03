import logging
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from ..event_check import require_event_code, require_event_code_function
from ag_data.models import AGSensor, AGSensorType, AGEvent, AGMeasurement
from mercury.models import GFConfig
from django.contrib import messages
from mercury.grafanaAPI.grafana_api import Grafana

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


def validate_inputs(sensor_name, field_names, request, new=False):
    """This validates the form before a user submits a new or updated sensor to
    prevent bad inputs"""

    form_valid = True

    if new:
        # duplicated sensor name
        if AGSensorType.objects.filter(name=sensor_name).count() > 0:
            messages.error(request, "FAILED: Sensor (type) name is already taken.")
            form_valid = False

        if AGSensor.objects.filter(name=sensor_name).count() > 0:
            messages.error(request, "FAILED: Sensor name is already taken.")
            form_valid = False

    # no sensor name
    if not sensor_name:
        messages.error(request, "FAILED: Sensor name is missing or invalid.")
        form_valid = False

    # missing field names
    for name in field_names:
        if not name:
            messages.error(request, "FAILED: Sensor has missing field name(s).")
            form_valid = False

    # duplicated field names
    if len(field_names) > len(set(field_names)):
        messages.error(request, "FAILED: Field names must be unique.")
        form_valid = False

    return form_valid, request


@require_event_code_function
def delete_sensor(request, sensor_name):
    """This deletes a sensor from the database based on a button click"""
    sensor_to_delete = AGSensor.objects.get(name=sensor_name)
    sensor_type_to_delete = AGSensorType.objects.get(name=sensor_name)
    if sensor_type_to_delete:

        # delete any sensor panels from grafana
        gfconfigs = GFConfig.objects.all()
        events = AGEvent.objects.all()

        # delete panl from every dashboard of all grafana instances
        for gfconfig in gfconfigs:
            grafana = Grafana(gfconfig)

            # Delete sensor from each event panel
            for event in events:
                try:
                    grafana.delete_panel(sensor_to_delete.name, event)
                except ValueError as error:
                    messages.error(request, error)

        sensor_to_delete.delete()
        sensor_type_to_delete.delete()
    else:
        messages.error(request, sensor_name, " not found!!!")
    return redirect("/sensor")


def remove_whitespace_caps(name, field_list):
    name = name.strip().lower()  # remove excess whitespace and CAPS
    return_list = [string.strip().lower() for string in field_list]
    return name, return_list


def generate_sensor_format(field_names, field_data_types, units):
    """ Return proper JSON format for sensor based on form submission.
        Format structure is a dictionary of dictionaries """
    sensor_format = {}
    fields = zip(field_names, field_data_types, units)
    for field in fields:
        sensor_format[field[0]] = {"data_type": field[1], "unit": field[2]}
    return sensor_format


class CreateSensorView(TemplateView):
    """This is the view for creating a new ...."""

    template_name = "sensor.html"

    @require_event_code
    def get(self, request, *args, **kwargs):
        sensors = AGSensor.objects.all()
        sensor_types = AGSensorType.objects.all()

        graph_types = AGSensorType.GRAPH_CHOICES

        context = {
            "sensors": sensors,
            "sensor_types": sensor_types,
            "graph_types": graph_types,
        }
        return render(request, self.template_name, context)

    @require_event_code
    def post(self, request, *args, **kwargs):
        sensor_name = request.POST.get("sensor-name")  # name = type name
        field_names = request.POST.getlist("field-names")
        field_types = request.POST.getlist("data-types")
        field_units = request.POST.getlist("units")
        sensor_name, field_names = remove_whitespace_caps(sensor_name, field_names)
        graph_type = request.POST.get("sensor-graph-type")

        if "edit_sensor" in request.POST:
            new_name = request.POST.get("sensor-name-updated")
            new_name, field_names = remove_whitespace_caps(new_name, field_names)
            new = True
            if new_name == sensor_name:
                new = False
            valid, request = validate_inputs(new_name, field_names, request, new)
            if graph_type == "map" and len(field_names) != 2:
                messages.error(
                    request,
                    "Map panels must have exactly 2 fields for "
                    "latitude and longitude GPS coordinates. Update "
                    "the sensor fields or change the Graph Type.",
                )
                valid = False
            if graph_type == "gauge" and len(field_names) != 1:
                messages.error(
                    request,
                    "Gauge panels must have exactly 1 field. Update "
                    "the sensor fields or change the Graph Type.",
                )
                valid = False
            new_format = generate_sensor_format(field_names, field_types, field_units)
            if valid:
                sensor_to_update = AGSensor.objects.get(name=sensor_name)
                prev_name = sensor_to_update.name

                sensor_type_to_update = AGSensorType.objects.get(name=sensor_name)
                prev_format = sensor_type_to_update.format
                prev_graph_type = sensor_type_to_update.graph_type
                sensor_to_update.name = new_name
                sensor_type_to_update.name = new_name
                sensor_type_to_update.format = new_format
                sensor_type_to_update.graph_type = graph_type
                sensor_to_update.save()
                sensor_type_to_update.save()

                # update sensor panel in each grafana instance
                gfconfigs = GFConfig.objects.all()
                events = AGEvent.objects.all()

                name_changed = True if new_name != prev_name else False
                format_changed = True if new_format != prev_format else False
                graph_type_changed = True if graph_type != prev_graph_type else False

                if name_changed and not (format_changed or graph_type_changed):
                    for gfconfig in gfconfigs:
                        grafana = Grafana(gfconfig)

                        for event in events:
                            # Update sensor panel in each event dashboard
                            # instance
                            try:
                                grafana.update_panel_title(event, prev_name, new_name)
                            except ValueError as error:
                                messages.error(request, error)
                    messages.success(
                        request, f"Grafana panels updated based on sensor changes"
                    )

                elif format_changed or graph_type_changed:
                    if format_changed:
                        # Delete any existing measurement data for the sensor
                        AGMeasurement.objects.filter(
                            sensor_id=sensor_to_update.uuid
                        ).delete()

                    for gfconfig in gfconfigs:
                        grafana = Grafana(gfconfig)

                        for event in events:
                            # Update sensor panel in each event dashboard
                            # instance
                            try:
                                grafana.update_panel_sensor(
                                    event, prev_name, sensor_to_update
                                )
                            except ValueError as error:
                                messages.error(request, error)
                    messages.success(
                        request, f"Grafana panels updated based on sensor changes"
                    )
                else:
                    messages.error(request, f"No changes detected - no updates made")

        if "submit_new_sensor" in request.POST:
            valid, request = validate_inputs(
                sensor_name, field_names, request, new=True
            )
            sensor_format = generate_sensor_format(
                field_names, field_types, field_units
            )
            graph_type = request.POST.get("sensor-graph-type")
            if graph_type == "map" and len(field_names) != 2:
                messages.error(
                    request,
                    "Map panels must have exactly 2 fields for "
                    "latitude and longitude GPS coordinates. Update "
                    "the sensor fields or change the Graph Type.",
                )
                valid = False
            if graph_type == "gauge" and len(field_names) != 1:
                messages.error(
                    request,
                    "Gauge panels must have exactly 1 field. Update "
                    "the sensor fields or change the Graph Type.",
                )
                valid = False

            if valid:
                """1) The structure of the models (database API) is confusing and we hide
                 the confusing details from the user. 2) Note that we have to first
                 create a sensor type, save it then create a sensor which takes
                 type as an input 3) Sensor types and sensors have the same name.
                 They are the same concept and should not be separated. Separating
                 sensors from sensor types will likely cause bad things to happen...
                 """
                new_type = AGSensorType.objects.create(
                    name=sensor_name,
                    processing_formula=0,
                    format=sensor_format,
                    graph_type=graph_type,
                )
                new_type.save()

                sensor_type = AGSensorType.objects.get(name=sensor_name)

                new_sensor = AGSensor.objects.create(
                    name=sensor_name, type_id=sensor_type
                )
                new_sensor.save()

                # Add Sensor panel to the Active Event dashboard in each Grafana
                # instances
                gfconfigs = GFConfig.objects.all()

                # Retrieve the events
                events = AGEvent.objects.all()

                for event in events:
                    # Add panel to each grafana instance
                    for gfconfig in gfconfigs:
                        # Grafana instance using current GFConfig
                        grafana = Grafana(gfconfig)

                        # Add the Sensor Panel to each event
                        try:
                            grafana.add_panel(new_sensor, event)
                        except ValueError as error:
                            messages.error(
                                request,
                                f"Failed to add panel to active dashboard: {error}",
                            )
                        else:
                            messages.success(
                                request,
                                "Sensor panel added to Grafana for the active event",
                            )

        # gather sensors and sensor types (which should be the same) and render them
        types = AGSensorType.objects.all()
        sensors = AGSensor.objects.all()
        graph_types = AGSensorType.GRAPH_CHOICES
        context = {
            "sensor_types": types,
            "sensors": sensors,
            "graph_types": graph_types,
        }
        return render(request, self.template_name, context)
