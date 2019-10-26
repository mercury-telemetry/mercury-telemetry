from django import forms
from mercury.models import SimulatedData

# for our slider
from django.forms.widgets import NumberInput
class RangeInput(NumberInput):
    input_type = 'range'


class SimulatorForm(forms.ModelForm):
    name = forms.CharField(max_length=150, strip=True)
    owner = forms.CharField(max_length=150, strip=True)

    temperature = forms.FloatField()

    acceleration_x = forms.FloatField()
    acceleration_y = forms.FloatField()
    acceleration_z = forms.FloatField()

    wheel_speed_fr = forms.FloatField()
    wheel_speed_fl = forms.FloatField()
    wheel_speed_br = forms.FloatField()
    wheel_speed_bl = forms.FloatField()

    suspension_fr = forms.FloatField()
    suspension_fl = forms.FloatField()
    suspension_br = forms.FloatField()
    suspension_bl = forms.FloatField()

    # Fuel Supply Panel
    #initial_fuel = forms.FloatField()
    fuel_decrease_rate = forms.FloatField()

    # Oil Supply/Level Panel
    initial_oil = forms.FloatField()
    oil_decrease_rate = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super(SimulatorForm, self).__init__(*args, **kwargs)
        # snip the other fields for the sake of brevity
        # Adding content to the form
        self.fields['oil_decrease_rate'].help_text = "oil_decrease_rate here"
        self.fields['oil_decrease_rate'].label = "Oil Decrease Rate"
        self.fields['oil_decrease_rate'].widget = RangeInput(attrs={'max': 1,'min': 0, 'step': 0.1})
    class Meta:
        model = SimulatedData
        # fields = "__all__"

        widgets = {
            'initial_fuel': RangeInput(attrs={'max': 1,
                                        'min': 0,
                                        'step': 0.1}),

        }

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
            "initial_fuel",
            "fuel_decrease_rate",
            "initial_oil",
            "oil_decrease_rate",
            "created_at",]




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
