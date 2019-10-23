from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from ..forms import VehicleForm
import datetime


class DashboardView(TemplateView):
    template_name = "dashboard.html"
