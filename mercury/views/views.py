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
    """This is the view for the homepage of the app."""

    @require_event_code
    def get(self, request, **kwargs):
        return render(request, "index.html", context=None)


class Logout(TemplateView):
    """This view has a GET method that clears the session event code. It
    will bring the user back to the login page."""

    def get(self, request, *args, **kwargs):
        try:
            del request.session["event_code_active"]
        except KeyError:  # noqa
            pass

        if request.session.get("event_code_known"):
            message = "You have been successfully logged out."
            del request.session["event_code_known"]
        else:
            message = "You are already logged out."
        messages.info(request, message)
        return HttpResponseRedirect(reverse("mercury:EventAccess"))


class EventAccess(TemplateView):
    """This is the view for the login page. It checks the DB to see if an event
    is currently active, and redirects to the hompage if not."""

    def post(self, request, *args, **kwargs):
        """This method checks the submitted event code to see if it matches
        the latest (i.e. active) event."""

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
