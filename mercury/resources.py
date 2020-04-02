from import_export import resources
from ag_data.models import AGEvent, AGMeasurement


class EventResource(resources.ModelResource):
    class Meta:
        model = AGEvent
        exclude = ("uuid",)


class MeasurementResource(resources.ModelResource):
    class Meta:
        model = AGMeasurement
        exclude = ("uuid",)
