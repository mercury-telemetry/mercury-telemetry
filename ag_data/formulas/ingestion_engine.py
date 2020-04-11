from ag_data import models
from ag_data.formulas.library.system import mercury_formulas as hgFormulas

from ag_data.utilities import MeasurementExchange


class MeasurementIngestionEngine:

    processing_formulas = {
        0: hgFormulas.fEmptyResult,
        2: hgFormulas.fMercurySimpleTemperatureSensor,
        4: hgFormulas.fMercuryDualTemperatureSensor,
        6: hgFormulas.fMercuryFlowSensor,
    }

    def saveMeasurement(self, rawMeasurement):

        assert isinstance(rawMeasurement, MeasurementExchange)

        formula = MeasurementIngestionEngine.processing_formulas.get(
            rawMeasurement.processing_formula, hgFormulas.fEmptyResult
        )

        value = {"reading": rawMeasurement.reading}

        value["result"] = formula(rawMeasurement)

        return models.AGMeasurement.objects.create(
            timestamp=rawMeasurement.timestamp,
            event_uuid=rawMeasurement.event,
            sensor_id=rawMeasurement.sensor,
            value=value,
        )
