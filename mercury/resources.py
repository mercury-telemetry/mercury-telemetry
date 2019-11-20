from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from mercury.models import TemperatureSensor


class TemperatureSensorResource(ModelResource):
    """This class exposes an API for the SimulatedData object with the resource name
    defined below as the 'resource_name'."""

    class Meta:
        queryset = TemperatureSensor.objects.all()
        resource_name = "tempdata"
        authorization = Authorization()
