from ag_data.models import AGMeasurement, AGActiveEvent
from ag_data.formulas import formulas
from ag_data.error_record import record


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

        event = self.event
        if not event:
            active = AGActiveEvent.objects.first()
            if active:
                event = active.agevent

        try:
            if event:
                formula = formulas.formula_map.get(
                    sensor.type_id.processing_formula, formulas.identity
                )

                preprocessed = preprocess(sensor, formula, timestamp, measurement)
                result = formula(**preprocessed)

                return AGMeasurement.objects.create(
                    timestamp=timestamp,
                    event_uuid=event,
                    sensor_id=sensor,
                    value={"raw": measurement, "result": result},
                )
            else:
                raise TypeError

        except TypeError:
            # Currently no active event, error should be recorded
            data = {
                "sensor": sensor,
                "timestamp": timestamp,
                "measurement": measurement,
            }
            record.save_error(
                raw_data=str(data),
                error_code=record.ERROR_CODE["NO_ACT_EVENT"],
                error_description="Currently no active event",
            )


shared_instance = FormulaPipeline()
