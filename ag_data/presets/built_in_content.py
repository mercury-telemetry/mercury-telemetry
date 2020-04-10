built_in_sensor_types = [
    {
        "agSensorTypeID": 0,
        "agSensorTypeName": "Coin Side Sensor",
        "agSensorTypeFormula": 0,
        "agSensorTypeFormat": {
            "reading": {"side": {"unit": "", "format": "bool"}, "result": {}}
        },
    },
    {
        "agSensorTypeID": 2,
        "agSensorTypeName": "Simple Temperature Sensor",
        "agSensorTypeFormula": 2,
        "agSensorTypeFormat": {
            "reading": {"unit": "Celsius", "format": "float"},
            "result": {},
        },
    },
    {
        "agSensorTypeID": 4,
        "agSensorTypeName": "Dual Temperature Sensor",
        "agSensorTypeFormula": 4,
        "agSensorTypeFormat": {
            "reading": {
                "internal": {"unit": "Keivin", "format": "float"},
                "external": {"unit": "Keivin", "format": "float"},
            },
            "result": {
                "mean": {"unit": "Keivin", "format": "float"},
                "diff": {"unit": "Keivin", "format": "float"},
            },
        },
    },
    {
        "agSensorTypeID": 6,
        "agSensorTypeName": "Gas Flow Sensor",
        "agSensorTypeFormula": 6,
        "agSensorTypeFormat": {
            "reading": {"volumetricFlow": {"unit": "cc/sec", "format": "float"}},
            "result": {"gasLevel": {"unit": "%", "format": "float"}},
        },
    },
    {
        "agSensorTypeID": 8,
        "agSensorTypeName": "Gaussian Random Number Emitter",
        "agSensorTypeFormula": 0,
        "agSensorTypeFormat": {
            "reading": {"sample": {"unit": "", "format": "float"}},
            "result": {},
        },
    },
]
