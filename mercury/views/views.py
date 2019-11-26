from django.shortcuts import render
from django.views.generic import TemplateView
from mercury.models import EventCodeAccess
from django.http import HttpResponseRedirect
from django.contrib import messages
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        if request.session.get("event_code_active") and request.session.get(
            "event_code_known"
        ):
            return render(request, "index.html", context=None)
        else:
            return render(
                request,
                "login.html",
                context={
                    "no_session_message": (
                        "You do not appear to have an "
                        "active session. Please login again."
                    )
                },
            )


class EventAccess(TemplateView):
    def post(self, request, *args, **kwargs):
        event_code = request.POST.get("eventcode")
        event_code_objects = EventCodeAccess.objects.filter(
            event_code=event_code, enabled=True
        )
        if event_code_objects:
            request.session["event_code_known"] = True
            return HttpResponseRedirect("index")
        else:
            messages.error(request, "Invalid Event Code")
            return HttpResponseRedirect("/")

    def get(self, request, **kwargs):
        log.debug(dir(request.session))
        event_code_objects = EventCodeAccess.objects.filter(enabled=True)
        if event_code_objects:
            request.session["event_code_active"] = True
            return render(request, "login.html", context=None)
        else:
            return render(request, "index.html", context=None)
