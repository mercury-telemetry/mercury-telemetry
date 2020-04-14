from ag_data import models


def fEmptyResult(measurement):

    return {}


fMercurySimpleTemperatureSensor = fEmptyResult


def fMercuryDualTemperatureSensor(measurement):
    mean = measurement.reading["internal"] / 2 + measurement.reading["external"] / 2
    diff = measurement.reading["internal"] - measurement.reading["external"]

    return {"mean": mean, "diff": diff}


def fMercuryFlowSensor(measurement):
    result = {}

    measurements = models.AGMeasurement.objects.filter(sensor_id=measurement.sensor.id)

    if measurements.count() == 0:
        result = {"gasLevel": 100}
    else:
        latest = measurements.latest("timestamp")
        timeElapsed = measurement.timestamp - latest.timestamp

        lastResult = latest.value["result"]["gasLevel"]

        if lastResult is not None:
            result = {
                "gasLevel": lastResult
                - measurement.reading["volumetricFlow"] * timeElapsed.total_seconds()
            }

    return result


processing_formulas = {
    0: fEmptyResult,
    2: fMercurySimpleTemperatureSensor,
    4: fMercuryDualTemperatureSensor,
    6: fMercuryFlowSensor,
}
