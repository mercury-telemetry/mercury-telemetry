import logging
from django.shortcuts import render
from django.views.generic import TemplateView
from ..event_check import require_event_code

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


class CreateSensorView(TemplateView):
    """This is the view for creating a new event."""

    template_name = "sensor.html"

    @require_event_code
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)
