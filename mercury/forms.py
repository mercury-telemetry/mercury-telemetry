from django import forms

# from mercury.models import Vehicle, SuspensionSensor
from mercury.models import SimulatedData

# from django.forms.widgets import NumberInput
# for our slider
# class RangeInput(NumberInput):
#     input_type = 'range'


class SimulatorForm(forms.ModelForm):
    name = forms.CharField(max_length=150, strip=True)
    owner = forms.CharField(max_length=150, strip=True)

    temperature = forms.IntegerField()

    acceleration_x = forms.IntegerField()
    acceleration_y = forms.IntegerField()
    acceleration_z = forms.IntegerField()

    wheel_speed_fr = forms.IntegerField()
    wheel_speed_fl = forms.IntegerField()
    wheel_speed_br = forms.IntegerField()
    wheel_speed_bl = forms.IntegerField()

    suspension_fr = forms.IntegerField()
    suspension_fl = forms.IntegerField()
    suspension_br = forms.IntegerField()
    suspension_bl = forms.IntegerField()

    class Meta:
        model = SimulatedData
        # fields = "__all__"

        fields = [
            "name",
            "owner",
            "temperature",
            "acceleration_x",
            "acceleration_y",
            "acceleration_z",
            "wheel_speed_fr",
            "wheel_speed_fl",
            "wheel_speed_br",
            "wheel_speed_bl",
            "suspension_fr",
            "suspension_fl",
            "suspension_br",
            "suspension_bl",
            "created_at",
        ]

#
# class VehicleForm(ModelForm):
#
#     class Meta:
#         model = Vehicle
#         fields = "__all__"
#
#
# class SuspensionForm(ModelForm):
#     class Meta:
#         model = SuspensionSensor
#         fields = ['compression']
#         widgets = {
#             'compression' : RangeInput(attrs={'max': 100000,
#             'min':10000,
#             'step':5000}),
#         }
