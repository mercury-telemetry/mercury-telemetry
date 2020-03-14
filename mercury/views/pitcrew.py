from django.shortcuts import render
from django.views.generic import TemplateView

from ..event_check import require_event_code


class PitCrewView(TemplateView):
    template_name = "pitcrew.html"

    @require_event_code
    def get(self, request, **kwargs):
        return render(request, self.template_name, {})
