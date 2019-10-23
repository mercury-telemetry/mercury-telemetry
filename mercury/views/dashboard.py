from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect  # noqa
from ..models import Vehicle


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        all_vehicles = Vehicle.objects.all()
        return render(request, self.template_name, {"all_vehicles": all_vehicles})
