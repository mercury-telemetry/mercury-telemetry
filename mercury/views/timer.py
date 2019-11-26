from django.shortcuts import render
from django.views.generic import TemplateView


class TimerView(TemplateView):
    template_name = "timer.html"
