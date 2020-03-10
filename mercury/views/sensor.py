import logging
from django.shortcuts import render
from django.views.generic import TemplateView
from ..event_check import require_event_code
from mercury.models import AGSensor
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
        post_sensor_name = request.POST.get("sensor-name")
        post_field_names = request.POST.getlist("field-name")
        post_field_types = request.POST.getlist("field-type")
        post_field_units = request.POST.getlist("field-unit")

        field_names = list()
        field_types = list()
        field_units = list()
        for i in range(len(post_field_names)):
            if post_field_names[i]:
                field_names.append(post_field_names[i])
                field_types.append(post_field_types[i])
                field_units.append(post_field_units[i])

        form_valid = True

        if not post_sensor_name:
            messages.error(
                request, ("Sensor name is missing."),
            )
            form_valid = False

        sensor = AGSensor.objects.filter(sensor_name=post_sensor_name)
        if sensor.count() > 0:
            messages.error(
                request, ("Sensor name already taken."),
            )
            form_valid = False

        if len(field_names) == 0:
            messages.error(
                request, ("Sensor must have at least 1 field."),
            )
            form_valid = False

        if check_if_duplicates(field_names):
            messages.error(
                request, ("Field names must be unique."),
            )
            form_valid = False

        sensor_format = {}
        for i in range(len(field_names)):
            if post_field_names[i]:
                sensor_format[field_names[i]] = {
                    "unit": field_units[i],
                    "format": field_types[i],
                }

        sensors = AGSensor.objects.all()

        if form_valid:
            sensor = AGSensor.objects.create(
                sensor_name=post_sensor_name,
                sensor_processing_formula=0,
                sensor_format=sensor_format,
            )
            context = {"sensors": sensors}
            sensor.save()
        else:
            context = {
                "sensors": sensors,
                "sensor_name": post_sensor_name,
                "sensor_format": sensor_format,
            }

        return render(request, self.template_name, context)
