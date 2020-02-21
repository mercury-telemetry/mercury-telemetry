import datetime

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from mercury.models import (
    TemperatureSensor,
    AccelerationSensor,
    WheelSpeedSensor,
    SuspensionSensor,
    FuelLevelSensor,
)
from ..event_check import require_event_code
from ..forms import (
    TemperatureForm,
    AccelerationForm,
    WheelSpeedForm,
    SuspensionForm,
    FuelLevelForm,
)


class SimulatorView(TemplateView):
    template_name = "simulator.html"

    @require_event_code
    def post(self, request, *args, **kwargs):
        """Used by AJAX method in the simulator.js file to save data
        from the simulator UI."""
        if request.POST.get("created_at_temp"):
            post_created_at = request.POST.get("created_at_temp")
            post_temperature = request.POST.get("temperature")

            temp_data = TemperatureSensor(
                created_at=post_created_at, temperature=post_temperature
            )
            temp_data.save()

        if request.POST.get("created_at_accel"):
            post_created_at = request.POST.get("created_at_accel")
            post_acceleration_x = request.POST.get("acceleration_x")
            post_acceleration_y = request.POST.get("acceleration_y")
            post_acceleration_z = request.POST.get("acceleration_z")

            accel_data = AccelerationSensor(
                created_at=post_created_at,
                acceleration_x=post_acceleration_x,
                acceleration_y=post_acceleration_y,
                acceleration_z=post_acceleration_z,
            )
            accel_data.save()

        if request.POST.get("created_at_ws"):
            post_created_at = request.POST.get("created_at_ws")
            post_wheel_speed_fr = request.POST.get("wheel_speed_fr")
            post_wheel_speed_fl = request.POST.get("wheel_speed_fl")
            post_wheel_speed_br = request.POST.get("wheel_speed_br")
            post_wheel_speed_bl = request.POST.get("wheel_speed_bl")

            ws_data = WheelSpeedSensor(
                created_at=post_created_at,
                wheel_speed_fr=post_wheel_speed_fr,
                wheel_speed_fl=post_wheel_speed_fl,
                wheel_speed_br=post_wheel_speed_br,
                wheel_speed_bl=post_wheel_speed_bl,
            )
            ws_data.save()

        if request.POST.get("created_at_ss"):
            post_created_at = request.POST.get("created_at_ss")
            post_suspension_fr = request.POST.get("suspension_fr")
            post_suspension_fl = request.POST.get("suspension_fl")
            post_suspension_br = request.POST.get("suspension_br")
            post_suspension_bl = request.POST.get("suspension_bl")

            ss_data = SuspensionSensor(
                created_at=post_created_at,
                suspension_fr=post_suspension_fr,
                suspension_fl=post_suspension_fl,
                suspension_br=post_suspension_br,
                suspension_bl=post_suspension_bl,
            )
            ss_data.save()

        if request.POST.get("created_at_fl"):
            post_created_at = request.POST.get("created_at_fl")
            post_current_fuel_level = request.POST.get("current_fuel_level")

            fl_data = FuelLevelSensor(
                created_at=post_created_at, current_fuel_level=post_current_fuel_level
            )
            fl_data.save()

        return HttpResponse(status=201)

    @require_event_code
    def get(self, request, *args, **kwargs):
        """This method will render the Simulator form when the
        HTTP GET method is used."""
        now = datetime.datetime.now()
        initial_data = {"created_at": now}
        form_temp = TemperatureForm(initial=initial_data)
        form_accel = AccelerationForm(initial=initial_data)
        form_ws = WheelSpeedForm(initial=initial_data)
        form_ss = SuspensionForm(initial=initial_data)
        form_fl = FuelLevelForm(initial=initial_data)
        context = {
            "form_temp": form_temp,
            "form_accel": form_accel,
            "form_ws": form_ws,
            "form_ss": form_ss,
            "form_fl": form_fl,
        }
        return render(request, self.template_name, context)
