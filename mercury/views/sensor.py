import logging
from django.shortcuts import render, reverse, redirect
from django.views.generic import TemplateView
from ..event_check import require_event_code
from mercury.models import AGSensor
import json

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


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

        # what is the difference between sensor_name
        # and sensor_description, currently treating as same thing
        # add math formula functionality - is 0 no formula?
        sensor_format = {}
        for i in range(len(post_field_names)):
            if post_field_names[i] != "":
                sensor_format[post_field_names[i]] = {
                    "unit": post_field_units[i],
                    "format": post_field_types[i],
                }

        sensor = AGSensor.objects.create(
            sensor_name=post_sensor_name,
            sensor_processing_formula=0,
            sensor_format=sensor_format
        )
        sensor.save()

        return redirect(reverse("mercury:sensor"))
