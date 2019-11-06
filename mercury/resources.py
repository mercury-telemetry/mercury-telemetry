from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from mercury.models import SimulatedData


class SimulatedDataResource(ModelResource):
    """This class exposes an API for the SimulatedData object with the resource name
    defined below as the 'resource_name'."""

    class Meta:
        queryset = SimulatedData.objects.all()
        resource_name = "simdata"
        authorization = Authorization()
