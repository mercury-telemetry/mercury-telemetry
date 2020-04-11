import attr

from django.utils import timezone

from ag_data import models
from ag_data.formulas.library.system import mercury_formulas as hgFormulas


class MeasurementIngestionEngine:

    processing_formulas = {
        0: hgFormulas.fEmptyResult,
        2: hgFormulas.fMercurySimpleTemperatureSensor,
        4: hgFormulas.fMercuryDualTemperatureSensor,
        6: hgFormulas.fMercuryFlowSensor,
    }

    def saveMeasurement(self, measurementDict, event):
        timestamp = measurementDict["measurement_timestamp"]
        sensor_id = measurementDict["measurement_sensor"]
        rawValue = measurementDict["measurement_values"]

        sensor = models.AGSensor.objects.get(pk=sensor_id)
        sensor_type = sensor.type_id
        processing_formula = sensor_type.processing_formula

        formula = MeasurementIngestionEngine.processing_formulas.get(
            processing_formula, hgFormulas.fEmptyResult
        )

        value = {"reading": rawValue}

        value["result"] = formula(timestamp, sensor, rawValue)

        return models.AGMeasurement.objects.create(
            timestamp=timestamp, event_uuid=event, sensor_id=sensor, value=value
        )


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
