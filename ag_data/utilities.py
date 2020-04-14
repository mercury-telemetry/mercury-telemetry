import attr

from django.utils import timezone

from ag_data import models


@attr.s
class MeasurementExchange(object):
    event = attr.ib(kw_only=True, validator=attr.validators.instance_of(models.AGEvent))
    timestamp = attr.ib(
        kw_only=True, validator=attr.validators.instance_of(timezone.datetime)
    )
    sensor = attr.ib(
        kw_only=True, validator=attr.validators.instance_of(models.AGSensor)
    )
    reading = attr.ib(kw_only=True, validator=attr.validators.instance_of(dict))

    @property
    def sensor_type(self):
        return self.sensor.type_id

    @property
    def processing_formula(self):
        return self.sensor_type.processing_formula
