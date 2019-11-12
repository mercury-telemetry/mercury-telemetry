from django.shortcuts import render
from django.views.generic import TemplateView
from ..models import SimulatedData


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        all_data = SimulatedData.objects.all().order_by("-created_at")
        return render(request, self.template_name, {"all_data": all_data})
