"""This module defines the ModelForms (or Forms) that are used by the rendering
engine to accept input for various features of the site"""
from django import forms
from ag_data.models import AGEvent, AGVenue, AGSensor
from mercury.models import (
    GFConfig,
    TemperatureSensor,
    AccelerationSensor,
    WheelSpeedSensor,
    SuspensionSensor,
    FuelLevelSensor,
)


class VenueForm(forms.ModelForm):
    class Meta:
        model = AGVenue
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"id": "post-event-name", "required": True}),
            "description": forms.TextInput(
                attrs={"id": "post-event-description", "required": True}
            ),
            "latitude": forms.TextInput(
                attrs={"id": "post-event-latitude", "required": True}
            ),
            "longitude": forms.TextInput(
                attrs={"id": "post-event-longitude", "required": True}
            ),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = AGEvent
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"id": "name", "required": True}),
            "date": forms.DateTimeInput(
                attrs={"id": "date", "required": True, "type": "datetime-local"}
            ),
            "description": forms.Textarea(
                attrs={"id": "description", "required": False}
            ),
        }


class GFConfigForm(forms.ModelForm):
    class Meta:
        model = GFConfig
        fields = ["gf_name", "gf_host", "gf_token"]
        labels = {
            "gf_name": "Label",
            "gf_host": "Hostname",
            "gf_token": "API Token",
        }
        default_data = {'gf_name': 'Local', 'gf_host': 'http://localhost:3000'}


class CustomModelChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s" % (obj.name)


class DashboardSensorPanelsForm(forms.ModelForm):
    class Meta:
        model = AGSensor
        exclude = ["id", "name", "type_id"]

    sensors = CustomModelChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=AGSensor.objects.all(), label=""
    )


class TemperatureForm(forms.ModelForm):
    class Meta:
        model = TemperatureSensor
        fields = "__all__"
        widgets = {
            "created_at": forms.DateTimeInput(
                attrs={"id": "post-created-at-temp", "required": True}
            ),
            "temperature": forms.NumberInput(
                attrs={"id": "post-temperature", "required": True}
            ),
        }


class AccelerationForm(forms.ModelForm):
    class Meta:
        model = AccelerationSensor
        fields = "__all__"
        widgets = {
            "created_at": forms.DateTimeInput(
                attrs={"id": "post-created-at_accel", "required": True}
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
        }


class WheelSpeedForm(forms.ModelForm):
    class Meta:
        model = WheelSpeedSensor
        fields = "__all__"
        widgets = {
            "created_at": forms.DateTimeInput(
                attrs={"id": "post-created-at_ws", "required": True}
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
        }


class SuspensionForm(forms.ModelForm):
    class Meta:
        model = SuspensionSensor
        fields = "__all__"
        widgets = {
            "created_at": forms.DateTimeInput(
                attrs={"id": "post-created-at_ss", "required": True}
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
        }


class FuelLevelForm(forms.ModelForm):
    class Meta:
        model = FuelLevelSensor
        fields = "__all__"
        widgets = {
            "created_at": forms.DateTimeInput(
                attrs={"id": "post-created-at_fl", "required": True}
            ),
            "current_fuel_level": forms.NumberInput(
                attrs={"id": "post-current-fuel-level", "required": True}
            ),
        }


class CANForm(forms.Form):
    """This simple form is used just to accept a CAN message on the CAN UI."""

    can_msg = forms.CharField(label="CAN Message")
