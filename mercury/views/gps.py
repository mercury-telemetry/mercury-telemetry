from django.shortcuts import render
from django.views.generic import TemplateView

from mercury.event_check import require_event_code


class CreateGPSView(TemplateView):
    """This is the view for creating a new event."""

    template_name = "gps.html"

    @require_event_code
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
