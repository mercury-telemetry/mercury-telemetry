from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

# from ..forms import VehicleForm, SuspensionForm
from ..forms import SimulatorForm
import datetime

# from mercury.models import Vehicle,SuspensionSensor


class SimulatorView(TemplateView):
    template_name = "simulator.html"
    form_class = SimulatorForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/simulator/")
        return render(request, self.template_name, {"form": form})

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={"created_at": datetime.datetime.now()})
        return render(request, self.template_name, {"form": form})
