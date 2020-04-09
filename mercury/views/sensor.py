import logging
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from ..event_check import require_event_code
from ag_data.models import AGSensor, AGSensorType, AGEvent
from mercury.models import GFConfig
from django.contrib import messages
from mercury.grafanaAPI.grafana_api import Grafana

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


def validate_inputs(sensor_name, field_names, request):
    """This validates the form before a user submits a new or updated sensor to
    prevent bad inputs"""

    form_valid = True

    # no sensor name
    if not sensor_name:
        messages.error(request, "FAILED: Sensor name is missing or invalid.")
        form_valid = False

    # duplicated sensor name
    if AGSensorType.objects.filter(name=sensor_name).count() > 0:
        messages.error(request, "FAILED: Sensor name is already taken.")
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


def delete_sensor(request, sensor_name):
    """This deletes a sensor from the database based on a button click"""
    sensor_to_delete = AGSensor.objects.get(name=sensor_name)
    sensor_type_to_delete = AGSensorType.objects.get(name=sensor_name)
    if sensor_type_to_delete:
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
        context = {"sensors": sensors, "sensor_types": sensor_types}
        return render(request, self.template_name, context)

    @require_event_code
    def post(self, request, *args, **kwargs):
        if "edit_sensor" in request.POST:
            sensor_name = request.POST.get("edit-sensor-name")  # name = type name
            field_names = request.POST.getlist("edit-field-names")
            field_types = request.POST.getlist("edit-data-type")
            field_units = request.POST.getlist("edit-units")

            sensor_name, field_names = remove_whitespace_caps(sensor_name, field_names)
            new_format = generate_sensor_format(field_names, field_types, field_units)
            valid, request = validate_inputs(sensor_name, field_names, request)
            if valid:
                sensor_to_update = AGSensorType.objects.get(name=sensor_name)
                sensor_to_update.format = new_format
                sensor_to_update.save()

        if "submit_new_sensor" in request.POST:
            type_name = request.POST.get("type-name")
            field_names = request.POST.getlist("field-names")
            field_types = request.POST.getlist("data-types")
            field_units = request.POST.getlist("units")

            # reformat then validate inputs to avoid duplicated names or bad inputs
            # like " "
            type_name, field_names = remove_whitespace_caps(type_name, field_names)
            sensor_name = type_name  # need this due to structure of models (Sensor and Sensor Type)
            valid, request = validate_inputs(type_name, field_names, request)
            type_format = generate_sensor_format(field_names, field_types, field_units)

            if valid:
                # Create new type and new sensor as required by models
                # Hide this confusing detail from users
                new_type = AGSensorType.objects.create(
                    name=type_name, processing_formula=0, format=type_format
                )
                new_type.save()

                sensor_type = AGSensorType.objects.get(name=type_name)

                new_sensor = AGSensor.objects.create(
                    name=sensor_name, type_id=sensor_type
                )
                new_sensor.save()

                # Add a Sensor panel to the Active Event
                # Check that Grafana is already configured
                # and that an Active Event exists
                # Note: THIS IS A PLACEHOLDER - waiting to decide
                # how to implement Current GFConfig
                gf_configs = GFConfig.objects.filter(gf_current=True)
                # Note: THIS IS A PLACEHOLDER - waiting to decide
                # how to implement Active Event
                active_events = AGEvent.objects.all()
                if len(gf_configs) > 0 and len(active_events) > 0:
                    gf_config = gf_configs.first()
                    active_event = active_events.first()
                    # Grafana instance using current GFConfig
                    grafana = Grafana(gf_config)

                    # Add the Sensor Panel to the Active Event's dashboard
                    try:
                        grafana.add_panel(new_sensor, active_event)
                    except ValueError as error:
                        messages.error(
                            request, f"Failed to add panel to active dashboard: {error}"
                        )

        # gather sensors and sensor types (which should be the same) and render them
        types = AGSensorType.objects.all()
        sensors = AGSensor.objects.all()
        context = {
            "sensor_types": types,
            "sensors": sensors,
        }
        return render(request, self.template_name, context)
