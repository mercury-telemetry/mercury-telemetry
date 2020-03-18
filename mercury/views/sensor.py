import logging
from django.shortcuts import render
from django.views.generic import TemplateView
from ..event_check import require_event_code
from mercury.models import AGSensor
from mercury.models import FuelLevelSensor
from django.contrib import messages

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


def check_if_duplicates(elements):
    """Check if given list contains any duplicates"""
    if len(elements) == len(set(elements)):
        return False
    else:
        return True


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

        # error checking. Note that sensor name, field name and id number are required by the HTML form. See sensor.HTML
        form_valid = True
        if len(AGSensor.objects.filter(sensor_name=sensor_name)) > 0:
            messages.error(request, "Sensor name is already taken.")
            form_valid = False
        if check_if_duplicates(field_names):
            messages.error(request, "Field names must be unique.")
            form_valid = False

        # create sensor format which is dictionary of dictionaries
        sensor_format = {}
        fields = zip(field_names, field_types, field_units)
        for field in fields:
            sensor_format[field[0]] = {"data_type": field[1], "unit": field[2]}

        if form_valid:
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
