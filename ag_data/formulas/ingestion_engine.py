from ag_data import models
from ag_data.formulas.library.system import mercury_formulas as hgFormulas


class MeasurementIngestionEngine:

    event = None

    processingFormulas = {
        0: hgFormulas.fPass,
        2: hgFormulas.fMercurySimpleTemperatureSensor,
        4: hgFormulas.fMercuryDualTemperatureSensor,
        6: hgFormulas.fMercuryFlowSensor,
    }

    def saveMeasurement(self, measurementDict):
        timestamp = measurementDict["measurement_timestamp"]
        sensor_id = measurementDict["measurement_sensor"]
        value = measurementDict["measurement_values"]

        sensor = models.AGSensor.objects.get(pk=sensor_id)
        sensor_type = sensor.type_id
        processing_formula = sensor_type.processing_formula

        formula = MeasurementIngestionEngine.processingFormulas.get(
            processing_formula, None
        )

        result = None

        if formula:
            result = formula(timestamp, sensor, value)

        value = {"reading": value}

        if result is not None:
            value["result"] = result
        else:
            value["result"] = {}

        models.AGMeasurement.objects.create(
            timestamp=timestamp, event_uuid=self.event, sensor_id=sensor, value=value
        )
