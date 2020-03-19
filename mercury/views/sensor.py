import logging
from django.shortcuts import render
from django.views.generic import TemplateView
from ..event_check import require_event_code
from mercury.models import AGSensor
from django.contrib import messages

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


def validate_add_sensor_inputs(sensor_name, field_name_list, request):
    form_valid = True

    # no sensor name
    if not sensor_name:
        messages.error(request, "Sensor name is missing or invalid.")
        form_valid = False

    # missing field names
    for name in field_name_list:
        if not name:
            messages.error(request, "Sensor has missing field name(s).")
            form_valid = False

    # duplicated sensor name
    if AGSensor.objects.filter(sensor_name=sensor_name).count() > 0:
        messages.error(request, "Sensor name is already taken.")
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
        context = {"sensors": sensors}
        return render(request, self.template_name, context)

    @require_event_code
    def post(self, request, *args, **kwargs):
        id_num = request.POST.get("sensor-id-num")
        sensor_name = request.POST.get("sensor-name")
        field_names = request.POST.getlist("field-names")
        field_types = request.POST.getlist("data-types")
        field_units = request.POST.getlist("units")

        # reformat then validate inputs to avoid duplicated names or bad inputs like " "
        sensor_name = sensor_name.strip().lower()  # remove excess whitespace and CAPS
        field_names = [string.strip().lower() for string in field_names]
        valid, request = validate_add_sensor_inputs(sensor_name, field_names, request)

        # create sensor format which is dictionary of dictionaries
        sensor_format = {}
        fields = zip(field_names, field_types, field_units)
        for field in fields:
            sensor_format[field[0]] = {"data_type": field[1], "unit": field[2]}

        if valid:
            sensor = AGSensor.objects.create(
                sensor_id=id_num,
                sensor_name=sensor_name,
                sensor_processing_formula=0,
                sensor_format=sensor_format,
            )  # processing formula needs to be adapted
            sensor.save()
            sensors = AGSensor.objects.all()
            context = {"sensors": sensors}
        else:
            sensors = AGSensor.objects.all()
            context = {
                "sensors": sensors,
                "sensor_name": sensor_name,
                "sensor_format": sensor_format,
            }

        return render(request, self.template_name, context)
