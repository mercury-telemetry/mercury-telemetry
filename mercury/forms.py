"""This module defines the ModelForms (or Forms) that are used by the rendering
engine to accept input for various features of the site"""
from django import forms
from ag_data.models import AGEvent, AGVenue, AGSensor
from mercury.models import GFConfig


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
        default_data = {"gf_name": "Local", "gf_host": "http://localhost:3000"}


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


class CANForm(forms.Form):
    """This simple form is used just to accept a CAN message on the CAN UI."""

    can_msg = forms.CharField(label="CAN Message")
