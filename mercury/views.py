# howdy/views.py
from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, "index.html", context=None)


class AboutPageView(TemplateView):
    template_name = "about.html"


class SimulatorView(TemplateView):
    template_name = "simulator.html"


class DashboardView(TemplateView):
    template_name = "dashboard.html"
