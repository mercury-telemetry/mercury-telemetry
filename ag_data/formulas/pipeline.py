from ag_data.models import AGMeasurement
from ag_data.formulas import formulas


def preprocess(sensor, formula, timestamp, measurement):
    measurement = measurement.copy()
    if formulas.flow_sensor == formula:
        measurement["timestamp"] = timestamp
        measurement["prevGasLevel"] = None
        measurement["prevTimestamp"] = None

        measurements = AGMeasurement.objects.filter(sensor_id=sensor.id)
        if measurements:
            latest = measurements.latest("timestamp")
            if latest:
                measurement["prevGasLevel"] = latest.value["result"]["gasLevel"]
                measurement["prevTimestamp"] = latest.timestamp
    return measurement


class FormulaPipeline:
    def __init__(self, event=None):
        self.event = event

    def save_measurement(self, sensor, timestamp, measurement) -> AGMeasurement:

        assert self.event is not None

        formula = formulas.formula_map.get(
            sensor.type_id.processing_formula, formulas.identity
        )

        preprocessed = preprocess(sensor, formula, timestamp, measurement)
        result = formula(**preprocessed)

        return AGMeasurement.objects.create(
            timestamp=timestamp,
            event_uuid=self.event,
            sensor_id=sensor,
            value={"raw": measurement, "result": result},
        )
