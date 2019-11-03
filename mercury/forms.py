from django import forms
from mercury.models import SimulatedData

# for our slider
from django.forms.widgets import NumberInput


class RangeInput(NumberInput):
    input_type = "range"


class SimulatorForm(forms.ModelForm):
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
            "created_at",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"id": "post-name", "required": True, "placeholder": "Enter Name"}
            ),
            "owner": forms.TextInput(
                attrs={
                    "id": "post-owner",
                    "required": True,
                    "placeholder": "Enter Name of the owner",
                }
            ),
            "temperature": forms.NumberInput(
                attrs={"id": "post-temperature", "required": True}
            ),
            "acceleration_x": forms.NumberInput(
                attrs={"id": "post-acceleration-X", "required": True}
            ),
            "acceleration_y": forms.NumberInput(
                attrs={"id": "post-acceleration-Y", "required": True}
            ),
            "acceleration_z": forms.NumberInput(
                attrs={"id": "post-acceleration-Z", "required": True}
            ),
            "wheel_speed_fr": forms.NumberInput(
                attrs={"id": "post-wheel-speed-fr", "required": True}
            ),
            "wheel_speed_fl": forms.NumberInput(
                attrs={"id": "post-wheel-speed-fl", "required": True}
            ),
            "wheel_speed_br": forms.NumberInput(
                attrs={"id": "post-wheel-speed-br", "required": True}
            ),
            "wheel_speed_bl": forms.NumberInput(
                attrs={"id": "post-wheel-speed-bl", "required": True}
            ),
            "suspension_fr": forms.NumberInput(
                attrs={"id": "post-suspension-fr", "required": True}
            ),
            "suspension_fl": forms.NumberInput(
                attrs={"id": "post-suspension-fl", "required": True}
            ),
            "suspension_br": forms.NumberInput(
                attrs={"id": "post-suspension-br", "required": True}
            ),
            "suspension_bl": forms.NumberInput(
                attrs={"id": "post-suspension-bl", "required": True}
            ),
            "initial_fuel": forms.NumberInput(
                attrs={"id": "post-initial-fuel", "required": True}
            ),
            "fuel_decrease_rate": forms.NumberInput(
                attrs={"id": "post-fuel-decrease-rate", "required": True}
            ),
            "initial_oil": forms.NumberInput(
                attrs={"id": "post-initial-oil", "required": True}
            ),
            "oil_decrease_rate": forms.NumberInput(
                attrs={"id": "post-oil-decrease-rate", "required": True}
            ),
            "created_at": forms.DateTimeInput(
                attrs={"id": "post-created-at", "required": True}
            ),
        }


# User story: #95 Continuous Submission for simulator UI
# end