from django import forms
from mercury.models import SimulatedData

# for our slider
from django.forms.widgets import NumberInput


class RangeInput(NumberInput):
    input_type = "range"


class SimulatorForm(forms.ModelForm):
    # name = forms.CharField(max_length=150, strip=True)
    # owner = forms.CharField(max_length=150, strip=True)

    # temperature = forms.FloatField()

    # acceleration_x = forms.FloatField()
    # acceleration_y = forms.FloatField()
    # acceleration_z = forms.FloatField()

    # wheel_speed_fr = forms.FloatField()
    # wheel_speed_fl = forms.FloatField()
    # wheel_speed_br = forms.FloatField()
    # wheel_speed_bl = forms.FloatField()

    # suspension_fr = forms.FloatField()
    # suspension_fl = forms.FloatField()
    # suspension_br = forms.FloatField()
    # suspension_bl = forms.FloatField()

    # # Fuel Supply Panel
    # initial_fuel = forms.FloatField()
    # fuel_decrease_rate = forms.FloatField()

    # # Oil Supply/Level Panel
    # initial_oil = forms.FloatField()
    # oil_decrease_rate = forms.FloatField()

    # def __init__(self, *args, **kwargs):
    #     super(SimulatorForm, self).__init__(*args, **kwargs)

    #     # acceleration_x
    #     self.fields[
    #         "acceleration_x"
    #     ].help_text = "Choose an acceleration values in m/s2"
    #     self.fields["acceleration_x"].label = "Acceleration in the X direction"
    #     # acceleration_y
    #     self.fields[
    #         "acceleration_y"
    #     ].help_text = "Choose an acceleration values in m/s2"
    #     self.fields["acceleration_y"].label = "Acceleration in the Y direction"
    #     # acceleration_z
    #     self.fields[
    #         "acceleration_z"
    #     ].help_text = "Choose an acceleration values in m/s2"
    #     self.fields["acceleration_z"].label = "Acceleration in the Z direction"

    #     # wheel_speed_fr
    #     self.fields["wheel_speed_fr"].help_text = "Enter Wheel Speed in m/s"
    #     self.fields["wheel_speed_fr"].label = "Wheel Speed for FR (Front Right)"
    #     # wheel_speed_fl
    #     self.fields["wheel_speed_fl"].help_text = "Enter Wheel Speed in m/s"
    #     self.fields["wheel_speed_fl"].label = "Wheel Speed for FL (Front Left)"
    #     # wheel_speed_bl
    #     self.fields["wheel_speed_bl"].help_text = "Enter Wheel Speed in m/s"
    #     self.fields["wheel_speed_bl"].label = "Wheel Speed for BL (Back Left)"
    #     # wheel_speed_fl
    #     self.fields["wheel_speed_br"].help_text = "Enter Wheel Speed in m/s"
    #     self.fields["wheel_speed_br"].label = "Wheel Speed for BR (Back Right)"

    #     # suspension_fr
    #     self.fields["suspension_fr"].help_text = "Enter Suspension/Compression in cm"
    #     self.fields["suspension_fr"].label = "Suspension/Compression for FR"
    #     # suspension_fl
    #     self.fields["suspension_fl"].help_text = "Enter Suspension/Compression in cm"
    #     self.fields["suspension_fl"].label = "Suspension/Compression for FL"
    #     # suspension_bl
    #     self.fields["suspension_bl"].help_text = "Enter Suspension/Compression in cm"
    #     self.fields["suspension_bl"].label = "Suspension/Compression for BL"
    #     # suspension_br
    #     self.fields["suspension_br"].help_text = "Enter Suspension/Compression in cm"
    #     self.fields["suspension_br"].label = "Suspension/Compression for BR"

    #     # initial_fuel
    #     self.fields["initial_fuel"].help_text = "Enter fuel amount in gallons"
    #     self.fields["initial_fuel"].label = "Initial Fuel Supply"

    #     # fuel_decrease_rate
    #     self.fields[
    #         "fuel_decrease_rate"
    #     ].help_text = "Choose from 0 to 1 (Steps of 0.1)"
    #     self.fields["fuel_decrease_rate"].label = "Fuel Decrease Rate"
    #     self.fields["fuel_decrease_rate"].widget = RangeInput(
    #         attrs={"max": 1, "min": 0, "step": 0.1}
    #     )

    #     # initial_oil
    #     self.fields["initial_oil"].help_text = "Enter fuel amount"
    #     self.fields["initial_oil"].label = "Initial Oil Supply"

    #     # fuel_decrease_rate
    #     self.fields["oil_decrease_rate"].help_text = "Choose from 0 to 1 (Steps of 0.1)"
    #     self.fields["oil_decrease_rate"].label = "Oil Decrease Rate"
    #     self.fields["oil_decrease_rate"].widget = RangeInput(
    #         attrs={"max": 1, "min": 0, "step": 0.1}
    #     )

    # Created by: Rajeev
    # User story: #95 Continuous Submission for simulator UI
    # begin

    class Meta:
        model = SimulatedData
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
            "created_at"
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={'id': 'post-name', 'required': True, 'placeholder': 'Enter Name'}
            ),

            'owner': forms.TextInput(
                attrs={'id': 'post-owner', 'required': True,
                       'placeholder': 'Enter Name of the owner'}
            ),

            'temperature': forms.NumberInput(
                attrs={'id': 'post-temperature', 'required': True}
            ),

            'acceleration_x': forms.NumberInput(
                attrs={'id': 'post-acceleration-X', 'required': True}
            ),

            'acceleration_y': forms.NumberInput(
                attrs={'id': 'post-acceleration-Y', 'required': True}
            ),

            'acceleration_z': forms.NumberInput(
                attrs={'id': 'post-acceleration-Z', 'required': True}
            ),

            'wheel_speed_fr': forms.NumberInput(
                attrs={'id': 'post-wheel-speed-fr', 'required': True}
            ),

            'wheel_speed_fl': forms.NumberInput(
                attrs={'id': 'post-wheel-speed-fl', 'required': True}
            ),

            'wheel_speed_br': forms.NumberInput(
                attrs={'id': 'post-wheel-speed-br', 'required': True}
            ),

            'wheel_speed_bl': forms.NumberInput(
                attrs={'id': 'post-wheel-speed-bl', 'required': True}
            ),

            'suspension_fr': forms.NumberInput(
                attrs={'id': 'post-suspension-fr', 'required': True}
            ),

            'suspension_fl': forms.NumberInput(
                attrs={'id': 'post-suspension-fl', 'required': True}
            ),

            'suspension_br': forms.NumberInput(
                attrs={'id': 'post-suspension-br', 'required': True}
            ),

            'suspension_bl': forms.NumberInput(
                attrs={'id': 'post-suspension-bl', 'required': True}
            ),

            'initial_fuel': forms.NumberInput(
                attrs={'id': 'post-initial-fuel', 'required': True}
            ),

            'fuel_decrease_rate': forms.NumberInput(
                attrs={'id': 'post-fuel-decrease-rate', 'required': True}
            ),

            'initial_oil': forms.NumberInput(
                attrs={'id': 'post-initial-oil', 'required': True}
            ),

            'oil_decrease_rate': forms.NumberInput(
                attrs={'id': 'post-oil-decrease-rate', 'required': True}
            ),

            'created_at': forms.DateTimeInput(
                attrs={'id': 'post-created-at', 'required': True}
            )
        }
# User story: #95 Continuous Submission for simulator UI
# end

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
