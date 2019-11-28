from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


class StopwatchView(TemplateView):
    template_name = "stopwatch.html"

    def get(self, request, **kwargs):

        if not (
            request.session.get("event_code_active")
            and request.session.get("event_code_known")
        ):
            messages.error(request, ("You do not have an active session. "
                                     "Please submit the active event code."))
            return HttpResponseRedirect(reverse("mercury:EventAccess"))

        else:
            return render(request, self.template_name, {})
