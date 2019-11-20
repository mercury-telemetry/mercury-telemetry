from django.shortcuts import render
from django.views.generic import TemplateView
from mercury.models import EventCodeAccess
from django.http import HttpResponseRedirect
from django.contrib import messages


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, "index.html", context=None)


class EventAccess(TemplateView):
    def post(self, request, *args, **kwargs):
        print("in EventAccess post method")
        event_code = request.POST.get("eventcode")
        event_code_objects = EventCodeAccess.objects.filter(
            event_code=event_code, enabled=True
        )
        if event_code_objects:
            return HttpResponseRedirect("index")
        else:
            messages.error(request, "Invalid Event Code")
            return HttpResponseRedirect("/")

    def get(self, request, **kwargs):
        print("in EventAccess get method")
        event_code_objects = EventCodeAccess.objects.filter(enabled=True)
        if event_code_objects:
            return render(request, "login.html", context=None)
        else:
            return render(request, "index.html", context=None)
