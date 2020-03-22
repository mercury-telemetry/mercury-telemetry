import logging
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from ..event_check import require_event_code

from ag_data.models import AGSensor, AGSensorType

from django.contrib import messages

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


def validate_add_sensor_type_inputs(type_name, field_name_list, request):
    """This validates the form before a user submits a new sensor type to prevent bad inputs"""

    form_valid = True

    # no type name
    if not type_name:
        messages.error(request, "Type name is missing or invalid.")
        form_valid = False

    # missing field names
    for name in field_name_list:
        if not name:
            messages.error(request, "Type has missing field name(s).")
            form_valid = False

    # duplicated type name
    if AGSensorType.objects.filter(name=type_name).count() > 0:
        messages.error(request, "Type name is already taken.")
        form_valid = False

    # duplicated field names
    if len(field_name_list) > len(set(field_name_list)):
        messages.error(request, "Field names must be unique.")
        form_valid = False

    return form_valid, request

def validate_add_sensor_inputs(sensor_name, request):
    """This validates the form before a user submits a new sensor to prevent bad inputs"""

    form_valid = True

    # no sensor name
    if not sensor_name:
        messages.error(request, "Sensor name is missing or invalid.")
        form_valid = False

    # duplicated sensor name
    if AGSensor.objects.filter(name=sensor_name).count() > 0:
        messages.error(request, "Sensor name is already taken.")
        form_valid = False

    return form_valid, request

def delete_sensor(request, sensor_id):
    """This deletes a sensor from the database based on user button click"""

    sensor_to_delete = AGSensor.objects.get(id=sensor_id)
    sensor_to_delete.delete()
    return redirect("/sensor")

def delete_sensor_type(request, type_id):
    """This deletes a sensor type from the database based on user button click"""
    for sensor in AGSensor.objects.all(): #delete sensors with this type first to avoid foreignkey error
        sensor.delete()
    type_to_delete = AGSensorType.objects.get(id=type_id)
    type_to_delete.delete()
    return redirect("/sensor")

def update_sensor(request, sensor_id):
    """This updates a sensor in the database based on user input"""

    sensor_to_update = AGSensor.objects.get(id=sensor_id)

    sensor_name = request.POST.get("edit-sensor-name")
    # reformat then validate name to avoid duplicated names or bad inputs like " "
    sensor_name = sensor_name.strip().lower()  # remove excess whitespace and CAPS
    valid, request = validate_add_sensor_inputs(sensor_name, request)

    sensor_types = AGSensorType.objects.all() #for when we return context later
    if valid:
        sensor_to_update.name = sensor_name
        sensor_type = request.POST.get("edit-select-sensor-type")
        sensor_to_update.type_id = AGSensorType.objects.get(name=sensor_type)
        sensor_to_update.save()
        sensors = AGSensor.objects.all()
        context = {
            "sensors": sensors,
            "sensor_types": sensor_types,
            }
    else:
        sensors = AGSensor.objects.all()
        context = {
            "sensors": sensors,
            "sensor_name": sensor_name,
            "sensor_type": sensor_type,
            "sensor_types": sensor_types,
        }
    return render(request, "sensor.html", context)


def update_sensor_type(request, type_id):
    """This updates a sensor type in the database based on user input"""
    #Currently causing a strange URL bug, need to debug

    type_to_update = AGSensorType.objects.get(id=type_id)
    type_name = request.POST.get("edit-type-name")
    field_names = request.POST.getlist("edit-field-names")
    field_types = request.POST.getlist("edit-data-types")
    field_units = request.POST.getlist("edit-units")

    # reformat then validate inputs to avoid duplicated names or bad inputs like " "
    type_name = type_name.strip().lower()  # remove excess whitespace and CAPS
    field_names = [string.strip().lower() for string in field_names]
    valid, request = validate_add_sensor_type_inputs(type_name, field_names, request)

    # create sensor format which is dictionary of dictionaries
    type_format = {}
    fields = zip(field_names, field_types, field_units)
    for field in fields:
        type_format[field[0]] = {"data_type": field[1], "unit": field[2]}

    sensors = AGSensor.objects.all() #for when we return context later
    if valid:
        type_to_update.name=type_name
        type_to_update.processing_formula=0
        type_to_update.format=type_format
        type_to_update.save()
        sensor_types = AGSensorType.objects.all()
        context = {
            "sensor_types": sensor_types,
            "sensors": sensors,
            }
    else:
        sensor_types = AGSensorType.objects.all()
        context = {
            "sensor_types": sensor_types,
            "type_name": type_name,
            "type_format": type_format,
            "sensors": sensors,
        }

    return render(request, "sensor.html", context)


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
        if ("submit_new_type" in request.POST):
            type_name = request.POST.get("type-name")
            field_names = request.POST.getlist("field-names")
            field_types = request.POST.getlist("data-types")
            field_units = request.POST.getlist("units")

            # reformat then validate inputs to avoid duplicated names or bad inputs like " "
            type_name = type_name.strip().lower()  # remove excess whitespace and CAPS
            field_names = [string.strip().lower() for string in field_names]
            valid, request = validate_add_sensor_type_inputs(type_name, field_names, request)

            # create sensor format which is dictionary of dictionaries
            type_format = {}
            fields = zip(field_names, field_types, field_units)
            for field in fields:
                type_format[field[0]] = {"data_type": field[1], "unit": field[2]}


            sensors = AGSensor.objects.all() #for when we return context later
            if valid:
                new_type = AGSensorType.objects.create(name=type_name, processing_formula=0, format=type_format)
                new_type.save()
                sensor_types = AGSensorType.objects.all()
                context = {
                    "sensor_types": sensor_types,
                    "sensors": sensors,
                    }
            else:
                sensor_types = AGSensorType.objects.all()
                context = {
                    "sensor_types": sensor_types,
                    "type_name": type_name,
                    "type_format": type_format,
                    "sensors": sensors,
                }

            return render(request, self.template_name, context)
            
        elif ("submit_new_sensor" in request.POST):
            sensor_name = request.POST.get("sensor-name")
            sensor_type = request.POST.get("select-sensor-type")
            sensor_type = AGSensorType.objects.get(name=sensor_type) #str --> AGSensorType 

            # reformat then validate name to avoid duplicated names or bad inputs like " "
            sensor_name = sensor_name.strip().lower()  # remove excess whitespace and CAPS
            valid, request = validate_add_sensor_inputs(sensor_name, request)

            sensor_types = AGSensorType.objects.all() #for when we return context later
            if valid:
                new_sensor = AGSensor.objects.create(name=sensor_name, type_id=sensor_type)
                new_sensor.save()
                sensors = AGSensor.objects.all()
                context = {
                    "sensors": sensors,
                    "sensor_types": sensor_types,
                    }
            else:
                sensors = AGSensor.objects.all()
                context = {
                    "sensors": sensors,
                    "sensor_name": sensor_name,
                    "sensor_type": sensor_type,
                    "sensor_types": sensor_types,
                }
            return render(request, self.template_name, context)