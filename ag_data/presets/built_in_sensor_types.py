built_in_sensor_types = [
    {
        "agSensorTypeID": 0,
        "agSensorTypeName": "Coin Side Sensor",
        "agSensorTypeFormula": 0,
        "agSensorTypeFormat": {"side": {"unit": "", "format": "bool"}},
    },
    {
        "agSensorTypeID": 2,
        "agSensorTypeName": "Simple Temperature Sensor",
        "agSensorTypeFormula": 2,
        "agSensorTypeFormat": {"reading": {"unit": "Celsius", "format": "float"}},
    },
    {
        "agSensorTypeID": 4,
        "agSensorTypeName": "Dual Temperature Sensor",
        "agSensorTypeFormula": 4,
        "agSensorTypeFormat": {
            "internal": {"unit": "Keivin", "format": "float"},
            "external": {"unit": "Keivin", "format": "float"},
        },
    },
    {
        "agSensorTypeID": 6,
        "agSensorTypeName": "Gas Flow Sensor",
        "agSensorTypeFormula": 6,
        "agSensorTypeFormat": {"volumetricFlow": {"unit": "cc/sec", "format": "float"}},
    },
    {
        "agSensorTypeID": 8,
        "agSensorTypeName": "Gaussian Random Number Emitter",
        "agSensorTypeFormula": 0,
        "agSensorTypeFormat": {"sample": {"unit": "", "format": "float"}},
    },
]
