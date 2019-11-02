from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect

# from ..forms import VehicleForm, SuspensionForm
from ..forms import SimulatorForm
from mercury.models import SimulatedData
import datetime


# Modified by: Rajeev
# User story: #95 Continuous Submission for simulator UI
# begin
class SimulatorView(TemplateView):
    template_name = "simulator.html"
    form_class = SimulatorForm

    def post(self, request, *args, **kwargs):
        post_name = request.POST.get('the_name')
        post_owner = request.POST.get('the_owner')
        post_created_at = request.POST.get('the_created_at')
        post_temperature = request.POST.get('the_temperature')
        post_acceleration_x = request.POST.get('the_acceleration_x')
        post_acceleration_y = request.POST.get('the_acceleration_y')
        post_acceleration_z = request.POST.get('the_acceleration_z')
        post_wheel_speed_fr = request.POST.get('the_wheel_speed_fr')
        post_wheel_speed_fl = request.POST.get('the_wheel_speed_fl')
        post_wheel_speed_br = request.POST.get('the_wheel_speed_br')
        post_wheel_speed_bl = request.POST.get('the_wheel_speed_bl')
        post_suspension_fr = request.POST.get('the_suspension_fr')
        post_suspension_fl = request.POST.get('the_suspension_fl')
        post_suspension_br = request.POST.get('the_suspension_br')
        post_suspension_bl = request.POST.get('the_suspension_bl')
        post_initial_fuel = request.POST.get('the_initial_fuel')
        post_fuel_decrease_rate = request.POST.get('the_fuel_decrease_rate')
        post_initial_oil = request.POST.get('the_initial_oil')
        post_oil_decrease_rate = request.POST.get('the_oil_decrease_rate')
        sim_data = SimulatedData(name=post_name,
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
                                 oil_decrease_rate=post_oil_decrease_rate)
        sim_data.save()
        return HttpResponseRedirect("/simulator/")

        # form = self.form_class(request.POST)
        # if form.is_valid():
        #     form.save()
        #     return HttpResponseRedirect("/simulator/")
        # return render(request, self.template_name, {"form": form})
# Modified by: Rajeev
# User story: #95 Continuous Submission for simulator UI
# end

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial={"created_at": datetime.datetime.now()})
        return render(request, self.template_name, {"form": form})
