#
# Formulas for Mercury's built-in and natively supported sensor types
# Sample processing formulas with primary sensors and fictional Mercury-branded sensors
#

from ag_data import models


def fEmptyResult(timestamp, sensor, measurement_payload):
    result = {}

    return result


def fMercurySimpleTemperatureSensor(timestamp, sensor, measurement_payload):
    result = {}

    # This Simple Temperature Sensor decides it wants its own formula, even though it does
    # nothing more than the fEmptyResult function.

    return result


def fMercuryDualTemperatureSensor(timestamp, sensor, measurement_payload):
    mean = measurement_payload["internal"] / 2 + measurement_payload["external"] / 2
    diff = measurement_payload["internal"] - measurement_payload["external"]

    result = {"mean": mean, "diff": diff}

    return result


def fMercuryFlowSensor(timestamp, sensor, measurement_payload):
    result = {}

    latest = models.AGMeasurement.objects.filter(sensor_id=sensor.id)

    if latest.count() == 0:
        result = {"gasLevel": 100}
    else:
        latest = latest.latest("timestamp")
        timeElapsed = timestamp - latest.timestamp

        lastResult = latest.value["result"]["gasLevel"]

        if lastResult is not None:
            result = {
                "gasLevel": lastResult
                - measurement_payload["volumetricFlow"]
                * (timeElapsed.microseconds / 1000000)
            }

    return result
