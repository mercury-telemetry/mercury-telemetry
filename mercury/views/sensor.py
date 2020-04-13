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
        sensor_name = request.POST.get("sensor-name")  # name = type name
        field_names = request.POST.getlist("field-names")
        field_types = request.POST.getlist("data-types")
        field_units = request.POST.getlist("units")
        sensor_name, field_names = remove_whitespace_caps(sensor_name, field_names)

        if "edit_sensor" in request.POST:
            new_name = request.POST.get("sensor-name-updated")
            new_name, field_names= remove_whitespace_caps(new_name, field_names)
            valid, request = validate_inputs(sensor_name, field_names, request)
            new_format = generate_sensor_format(field_names, field_types, field_units)
            if valid:
                sensor_to_update = AGSensor.objects.get(name=sensor_name)
                sensor_type_to_update = AGSensorType.objects.get(name=sensor_name)
                sensor_to_update.name = new_name
                sensor_type_to_update.name = new_name
                sensor_type_to_update.format = new_format
                sensor_to_update.save()
                sensor_type_to_update.save()

        if "submit_new_sensor" in request.POST:
            print("\n\n\n\n" + "HELLO")
            valid, request = validate_inputs(
                sensor_name, field_names, request, new=True
            )
            sensor_format = generate_sensor_format(
                field_names, field_types, field_units
            )
            if valid:
                """1) The structure of the models (database API) is confusing and we hide
                 the confusing details from the user. 2) Note that we have to first
                 create a sensor type, save it then create a sensor which takes
                 type as an input 3) Sensor types and sensors have the same name.
                 They are the same concept and should not be separated. Separating
                 sensors from sensor types will likely cause bad things to happen...
                 """
                new_type = AGSensorType.objects.create(
                    name=sensor_name, processing_formula=0, format=sensor_format
                )
                new_type.save()

                sensor_type = AGSensorType.objects.get(name=sensor_name)

                new_sensor = AGSensor.objects.create(
                    name=sensor_name, type_id=sensor_type
                )
                new_sensor.save()

                # Add a Sensor panel to the Active Event
                # Note: THIS IS A PLACEHOLDER - waiting to decide
                # how to implement Current GFConfig
                gfconfigs = GFConfig.objects.all()

                # Note: THIS IS A PLACEHOLDER - waiting to decide
                # how to implement Active Event
                active_events = AGEvent.objects.all()

                # Only add panel to active event
                if len(active_events) > 0:
                    active_event = active_events.first()

                    # Add panel to each grafana instance
                    for gfconfig in gfconfigs:

                        # Grafana instance using current GFConfig
                        grafana = Grafana(gfconfig)

                        # Add the Sensor Panel to the Active Event's dashboard
                        try:
                            grafana.add_panel(new_sensor, active_event)
                        except ValueError as error:
                            messages.error(
                                request,
                                f"Failed to add panel to active dashboard: {error}",
                            )

        # gather sensors and sensor types (which should be the same) and render them
        types = AGSensorType.objects.all()
        sensors = AGSensor.objects.all()
        context = {
            "sensor_types": types,
            "sensors": sensors,
        }
        return render(request, self.template_name, context)

