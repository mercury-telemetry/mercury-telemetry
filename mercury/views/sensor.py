import logging
from django.shortcuts import render
from django.views.generic import TemplateView
from ..event_check import require_event_code

from ag_data.models import AGSensor, AGSensorType

from django.contrib import messages

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


def validate_add_sensor_type_inputs(type_name, field_name_list, request):
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

    # duplicated sensor name
    if AGSensor.objects.filter(name=type_name).count() > 0:
        messages.error(request, "Type name is already taken.")
        form_valid = False

    # duplicated field names
    if len(field_name_list) > len(set(field_name_list)):
        messages.error(request, "Field names must be unique.")
        form_valid = False

    return form_valid, request


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
        id_num = request.POST.get("type-id-num")
        type_name = request.POST.get("type-name")
        field_names = request.POST.getlist("field-names")
        field_types = request.POST.getlist("data-types")
        field_units = request.POST.getlist("units")
        print("\n\n FIELD TYPES: " + str(field_types) + "\n\n")

        # reformat then validate inputs to avoid duplicated names or bad inputs like " "
        type_name = type_name.strip().lower()  # remove excess whitespace and CAPS
        field_names = [string.strip().lower() for string in field_names]
        valid, request = validate_add_sensor_type_inputs(type_name, field_names, request)

        # create sensor format which is dictionary of dictionaries
        type_format = {}
        fields = zip(field_names, field_types, field_units)
        for field in fields:
            type_format[field[0]] = {"data_type": field[1], "unit": field[2]}

        # Left over from when this was for old models, not sure if it's valuable later:
        # sensor = AGSensorType(name='Homer_Simpson', processing_formula=0, format=type_format)
        # sensor.save()

        if valid:
            new_type = AGSensorType.objects.create(name=type_name, id=id_num, processing_formula = 0, format= type_format)
            new_type.save()
            sensor_types = AGSensorType.objects.all()
            context = {"sensor_types": sensor_types}
        else:
            sensor_types = AGSensorType.objects.all()
            context = {
                "sensors": sensor_types,
                "type_name": type_name,
                "type_format": type_format,
            }

        return render(request, self.template_name, context)