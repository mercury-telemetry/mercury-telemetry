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


def validate_add_sensor_inputs(sensor_name, request):
    """This validates the form before a user submits a new sensor to prevent bad
    inputs"""

    form_valid = True

    # no sensor name
    if not sensor_name:
        messages.error(request, "FAILED: Sensor name is missing or invalid.")
        form_valid = False

    # duplicated sensor name
    if AGSensor.objects.filter(name=sensor_name).count() > 0:
        messages.error(request, "FAILED: Sensor name is already taken.")
        form_valid = False

    return form_valid, request


def validate_add_sensor_type_inputs(type_name, field_name_list, request):
    """
    This validates the form before a user submits a new sensor type to prevent bad
    inputs
    """

    form_valid = True

    # no type name
    if not type_name:
        messages.error(request, "FAILED: Type name is missing or invalid.")
        form_valid = False

    # missing field names
    for name in field_name_list:
        if not name:
            messages.error(request, "FAILED: Type has missing field name(s).")
            form_valid = False

    # duplicated type name
    if AGSensorType.objects.filter(name=type_name).count() > 0:
        messages.error(request, "FAILED: Type name is already taken.")
        form_valid = False

    # duplicated field names
    if len(field_name_list) > len(set(field_name_list)):
        messages.error(request, "FAILED: Field names must be unique.")
        form_valid = False

    return form_valid, request


def validate_update_sensor_type_inputs(
    type_name, field_name_list, type_to_update, request
):
    """
    This validates the form before a user submits a new sensor type to prevent bad inputs
    """

    form_valid = True

    # no type name
    if not type_name:
        messages.error(request, "FAILED: Type name is missing or invalid.")
        form_valid = False

    # missing field names
    for name in field_name_list:
        if not name:
            messages.error(request, "FAILED: Type has missing field name(s).")
            form_valid = False

    # duplicated type name
    for sensor_type in AGSensorType.objects.all():
        if sensor_type.name == type_name and sensor_type != type_to_update:
            messages.error(request, "FAILED: Type name is already taken.")
            form_valid = False

    # duplicated field names
    if len(field_name_list) > len(set(field_name_list)):
        messages.error(request, "FAILED: Field names must be unique.")
        form_valid = False

    return form_valid, request


def delete_sensor(request, sensor_id):
    """This deletes a sensor from the database based on user button click"""

    valid_id = False
    for sensor in AGSensor.objects.all():
        if sensor.id == sensor_id:
            valid_id = True
    if valid_id:
        sensor_to_delete = AGSensor.objects.get(id=sensor_id)

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

        # delete the sensor
        sensor_to_delete.delete()
    else:
        messages.error(
            request, "FAILED: Cannot find sensor with ID " + str(sensor_id) + "."
        )
    return redirect("/sensor")


def delete_sensor_type(request, type_id):
    """This deletes a sensor type from the database based on user button click"""

    valid_id = False
    for sensor_type in AGSensorType.objects.all():
        if sensor_type.id == type_id:
            valid_id = True
    if valid_id:
        for (
            sensor
        ) in (
            AGSensor.objects.all()
        ):  # delete sensors with this type first to avoid foreignkey error
            sensor.delete()
        type_to_delete = AGSensorType.objects.get(id=type_id)
        type_to_delete.delete()
    else:
        messages.error(
            request, "FAILED: Cannot find sensor type with ID " + str(type_id) + "."
        )
    return redirect("/sensor")


def update_sensor(request, sensor_id):
    """This updates a sensor in the database based on user input"""

    sensor_to_update = AGSensor.objects.get(id=sensor_id)
    prev_name = sensor_to_update.name
    sensor_name = request.POST.get("edit-sensor-name")

    # reformat then validate name to avoid duplicated names or bad inputs like " "
    sensor_name = sensor_name.strip().lower()  # remove excess whitespace and CAPS
    valid, request = validate_add_sensor_inputs(sensor_name, request)

    if valid:

        sensor_to_update.name = sensor_name
        sensor_to_update.save()

        # update sensor panel in each grafana instance
        gfconfigs = GFConfig.objects.all()
        events = AGEvent.objects.all()

        for gfconfig in gfconfigs:
            grafana = Grafana(gfconfig)

            for event in events:
                # Update sensor panel in the active event of each grafana instance
                try:
                    grafana.update_panel(event, prev_name, sensor_to_update)
                except ValueError as error:
                    messages.error(request, error)

    return redirect("/sensor")


def update_sensor_type(request, type_id):
    """This updates a sensor type in the database based on user input"""

    type_to_update = AGSensorType.objects.get(id=type_id)
    type_name = request.POST.get("edit-type-name")
    field_names = request.POST.getlist("edit-field-names")
    field_types = request.POST.getlist("edit-data-types")
    field_units = request.POST.getlist("edit-units")

    # reformat then validate inputs to avoid duplicated names or bad inputs like " "
    type_name = type_name.strip().lower()  # remove excess whitespace and CAPS
    field_names = [string.strip().lower() for string in field_names]
    valid, request = validate_update_sensor_type_inputs(
        type_name, field_names, type_to_update, request
    )

    # create sensor format which is dictionary of dictionaries
    type_format = {}
    fields = zip(field_names, field_types, field_units)
    for field in fields:
        type_format[field[0]] = {"data_type": field[1], "unit": field[2]}

    if valid:
        type_to_update.name = type_name
        type_to_update.processing_formula = 0
        type_to_update.format = type_format
        type_to_update.save()

    return redirect("/sensor")


class CreateSensorView(TemplateView):
    """This is the view for creating a new event."""

    template_name = "sensor.html"

    @require_event_code
    def get(self, request, *args, **kwargs):
        sensors = AGSensor.objects.all()
        sensor_types = AGSensorType.objects.all()
        context = {"sensors": sensors, "sensor_types": sensor_types}
        return render(request, self.template_name, context)

    @require_event_code
    def post(self, request, *args, **kwargs):
        if "submit_new_type" in request.POST:
            type_name = request.POST.get("type-name")
            field_names = request.POST.getlist("field-names")
            field_types = request.POST.getlist("data-types")
            field_units = request.POST.getlist("units")

            # reformat then validate inputs to avoid duplicated names or bad inputs
            # like " "
            type_name = type_name.strip().lower()  # remove excess whitespace and CAPS
            field_names = [string.strip().lower() for string in field_names]
            valid, request = validate_add_sensor_type_inputs(
                type_name, field_names, request
            )

            # create sensor format which is dictionary of dictionaries
            type_format = {}
            fields = zip(field_names, field_types, field_units)
            for field in fields:
                type_format[field[0]] = {"data_type": field[1], "unit": field[2]}

            sensors = AGSensor.objects.all()  # for when we return context later
            if valid:
                new_type = AGSensorType.objects.create(
                    name=type_name, processing_formula=0, format=type_format
                )
                new_type.save()
                sensor_types = AGSensorType.objects.all()
                context = {"sensor_types": sensor_types, "sensors": sensors}
            else:
                sensor_types = AGSensorType.objects.all()
                context = {
                    "sensor_types": sensor_types,
                    "type_name": type_name,
                    "type_format": type_format,
                    "sensors": sensors,
                }

            return render(request, self.template_name, context)

        elif "submit_new_sensor" in request.POST:
            sensor_name = request.POST.get("sensor-name")
            sensor_type = request.POST.get("select-sensor-type")
            sensor_type = AGSensorType.objects.get(
                name=sensor_type
            )  # str --> AGSensorType

            # reformat then validate name to avoid duplicated names or bad inputs
            # like " "
            sensor_name = (
                sensor_name.strip().lower()
            )  # remove excess whitespace and CAPS
            valid, request = validate_add_sensor_inputs(sensor_name, request)

            sensor_types = (
                AGSensorType.objects.all()
            )  # for when we return context later

            sensors = AGSensor.objects.all()

            if valid:
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

                context = {"sensors": sensors, "sensor_types": sensor_types}
            else:
                sensors = AGSensor.objects.all()
                context = {
                    "sensors": sensors,
                    "sensor_name": sensor_name,
                    "sensor_type": sensor_type,
                    "sensor_types": sensor_types,
                }
            return render(request, self.template_name, context)
