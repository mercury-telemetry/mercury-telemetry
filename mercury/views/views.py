from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from ..forms import VehicleForm
import datetime


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, "index.html", context=None)


class AboutPageView(TemplateView):
    template_name = "about.html"
