from django.forms import ModelForm
from mercury.models import Vehicle


class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = "__all__"
