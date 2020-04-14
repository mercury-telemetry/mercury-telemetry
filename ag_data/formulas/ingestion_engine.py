from ag_data import models
from ag_data.formulas.library.system.mercury_formulas import (
    processing_formulas,
    fEmptyResult,
)

from ag_data.utilities import MeasurementExchange


class MeasurementIngestionEngine:
    def saveMeasurement(
        self, rawMeasurement: MeasurementExchange
    ) -> models.AGMeasurement:

        assert isinstance(rawMeasurement, MeasurementExchange)

        formula = processing_formulas.get(
            rawMeasurement.processing_formula, fEmptyResult
        )

        value = {"reading": rawMeasurement.reading}

        value["result"] = formula(rawMeasurement)

        return models.AGMeasurement.objects.create(
            timestamp=rawMeasurement.timestamp,
            event_uuid=rawMeasurement.event,
            sensor_id=rawMeasurement.sensor,
            value=value,
        )
