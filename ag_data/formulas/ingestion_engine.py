from ag_data import models
from ag_data.formulas.library.system import mercury_formulas as hgFormulas


class MeasurementIngestionEngine:

    processingFormulas = {
        0: hgFormulas.fPass,
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

        formula = MeasurementIngestionEngine.processingFormulas.get(
            processing_formula, hgFormulas.fPass
        )

        value = {"reading": rawValue}

        value["result"] = formula(timestamp, sensor, value)

        models.AGMeasurement.objects.create(
            timestamp=timestamp, event_uuid=event, sensor_id=sensor, value=value
        )
