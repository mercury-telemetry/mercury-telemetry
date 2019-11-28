from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from mercury.models import (
    TemperatureSensor,
    AccelerationSensor,
    WheelSpeedSensor,
    SuspensionSensor,
    FuelLevelSensor,
)


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get(self, request, *args, **kwargs):
        temp_data = TemperatureSensor.objects.all().order_by("-created_at")
        accel_data = AccelerationSensor.objects.all().order_by("-created_at")
        ws_data = WheelSpeedSensor.objects.all().order_by("-created_at")
        ss_data = SuspensionSensor.objects.all().order_by("-created_at")
        fl_data = FuelLevelSensor.objects.all().order_by("-created_at")
        context = {
            "temp_data": temp_data,
            "accel_data": accel_data,
            "ws_data": ws_data,
            "ss_data": ss_data,
            "fl_data": fl_data,
        }
        if request.session.get("event_code_active") and request.session.get(
            "event_code_known"
        ):
            return render(request, self.template_name, context)
        else:
            messages.error(
                request,
                (
                    "You do not have an active session. "
                    "Please submit the active event code."
                ),
            )
            return HttpResponseRedirect(reverse("mercury:EventAccess"))
