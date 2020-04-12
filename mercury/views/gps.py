from django.shortcuts import render
from django.views.generic import TemplateView

from ag_data.models import AGActiveEvent
from mercury.event_check import require_event_code


class CreateGPSView(TemplateView):
    """This is the view for creating a new event."""

    template_name = "gps.html"

    @require_event_code
    def get(self, request, *args, **kwargs):
        active_event_object = AGActiveEvent.objects.all()
        active_event = None
        if len(active_event_object) > 0:
            active_event = active_event_object[0].agevent

        context = {
            "active_event": active_event,
        }

        return render(request, self.template_name, context)

