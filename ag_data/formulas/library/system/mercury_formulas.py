#
# Formulas for Mercury's built-in and natively supported sensor types
# Sample processing formulas with primary sensors and fictional Mercury-branded sensors
#

from ag_data import models


def fEmptyResult(measurement):

    return {}


def fMercurySimpleTemperatureSensor(measurement):

    # This Simple Temperature Sensor decides it wants its own formula, even though it does
    # nothing more than the fEmptyResult function.

    return {}


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
