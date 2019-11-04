from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse

from ..forms import SimulatorForm
from mercury.models import SimulatedData
import datetime


class SimulatorView(TemplateView):
    template_name = "simulator.html"

    def post(self, request, *args, **kwargs):
        """Used by AJAX method in the main.js file to save data from the simulator UI"""
        post_name = request.POST.get("name")
        post_owner = request.POST.get("owner")
        post_created_at = request.POST.get("created_at")
        post_temperature = request.POST.get("temperature")
        post_acceleration_x = request.POST.get("acceleration_x")
        post_acceleration_y = request.POST.get("acceleration_y")
        post_acceleration_z = request.POST.get("acceleration_z")
        post_wheel_speed_fr = request.POST.get("wheel_speed_fr")
        post_wheel_speed_fl = request.POST.get("wheel_speed_fl")
        post_wheel_speed_br = request.POST.get("wheel_speed_br")
        post_wheel_speed_bl = request.POST.get("wheel_speed_bl")
        post_suspension_fr = request.POST.get("suspension_fr")
        post_suspension_fl = request.POST.get("suspension_fl")
        post_suspension_br = request.POST.get("suspension_br")
        post_suspension_bl = request.POST.get("suspension_bl")
        post_initial_fuel = request.POST.get("initial_fuel")
        post_fuel_decrease_rate = request.POST.get("fuel_decrease_rate")
        post_initial_oil = request.POST.get("initial_oil")
        post_oil_decrease_rate = request.POST.get("oil_decrease_rate")
        sim_data = SimulatedData(
            name=post_name,
            owner=post_owner,
            created_at=post_created_at,
            temperature=post_temperature,
            acceleration_x=post_acceleration_x,
            acceleration_y=post_acceleration_y,
            acceleration_z=post_acceleration_z,
            wheel_speed_fr=post_wheel_speed_fr,
            wheel_speed_fl=post_wheel_speed_fl,
            wheel_speed_br=post_wheel_speed_br,
            wheel_speed_bl=post_wheel_speed_bl,
            suspension_fr=post_suspension_fr,
            suspension_fl=post_suspension_fl,
            suspension_br=post_suspension_br,
            suspension_bl=post_suspension_bl,
            initial_fuel=post_initial_fuel,
            fuel_decrease_rate=post_fuel_decrease_rate,
            initial_oil=post_initial_oil,
            oil_decrease_rate=post_oil_decrease_rate,
        )
        sim_data.save()
        return HttpResponse(status=201)

    def get(self, request, *args, **kwargs):
        """This method will render the Simulator form when GET is used"""
        form = SimulatorForm(initial={"created_at": datetime.datetime.now()})
        return render(request, self.template_name, {"form": form})
