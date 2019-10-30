from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from mercury.models import SimulatedData


class SimulatedDataResource(ModelResource):
    class Meta:
        queryset = SimulatedData.objects.all()
        resource_name = "simdata"
        authorization = Authorization()
