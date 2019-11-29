import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from mercury.models import EventCodeAccess
from ..event_check import require_event_code

log = logging.getLogger(__name__)
log.setLevel(logging.ERROR)


class HomePageView(TemplateView):
    @require_event_code
    def get(self, request, **kwargs):
        return render(request, "index.html", context=None)


class Logout(TemplateView):
    def get(self, request, *args, **kwargs):
        items = ["event_code_known", "event_code_active"]
        for item in items:
            try:
                del request.session[item]
            except:  # noqa E722
                pass
        return HttpResponseRedirect(reverse("mercury:EventAccess"))


class EventAccess(TemplateView):
    def post(self, request, *args, **kwargs):
        """This method checks the submitted event code to see if it matches
        the latest (ongoing) event"""
        event_code = request.POST.get("eventcode")
        event_code_objects = EventCodeAccess.objects.filter(
            event_code=event_code, enabled=True
        )
        if event_code_objects:
            request.session["event_code_known"] = True
            return HttpResponseRedirect("index")
        else:
            request.session["event_code_known"] = False
            messages.error(request, f"Event Code '{event_code}' is invalid!")
            return HttpResponseRedirect(reverse("mercury:EventAccess"))

    def get(self, request, **kwargs):
        """This method checks for an active (enabled) event and directs the user
        to the login page if an event is ongoing. Otherwise, the user is sent
        to the main page."""
        event_code_objects = EventCodeAccess.objects.filter(enabled=True)
        if event_code_objects:
            request.session["event_code_active"] = True
            if request.session.get("event_code_known"):
                return HttpResponseRedirect("index")
            else:
                return render(request, "login.html", context={"active_event": True})
        else:
            request.session["event_code_active"] = False
            return HttpResponseRedirect("index")
