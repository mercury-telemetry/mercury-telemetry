def identity(**kwargs):
    return kwargs


simple_temperature_sensor = identity


def dual_temperature_sensor(internal, external):
    return {"mean": (internal + external) / 2, "diff": internal - external}


def flow_sensor(prevGasLevel, prevTimestamp, volumetricFlow, timestamp):
    if prevGasLevel is not None and prevTimestamp is not None:
        time_elapsed = timestamp - prevTimestamp
        return {
            "gasLevel": prevGasLevel - volumetricFlow * time_elapsed.total_seconds()
        }
    else:
        return {"gasLevel": 100}


processing_formulas = {
    0: identity,
    2: simple_temperature_sensor,
    4: dual_temperature_sensor,
    6: flow_sensor,
}
