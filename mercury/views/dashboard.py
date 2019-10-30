from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect  # noqa
from ..models import SimulatedData


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        all_data = SimulatedData.objects.all()
        return render(request, self.template_name, {"all_data": all_data})


class DashboardLiveView(TemplateView):
    template_name = "dashboard-live.html"

    def get(self, request, *args, **kwargs):
        all_data = SimulatedData.objects.all()
        return render(request, self.template_name, {"all_data": all_data})
