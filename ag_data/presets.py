test_venue_data = [
    {
        "agVenueName": "Washington Square Park",
        "agVenueDescription": "Sunnyside Daycare's Butterfly Room.",
        "agVenueLatitude": 40.730812,
        "agVenueLongitude": -73.997456,
    },
    {
        "agVenueName": "Central Park",
        "agVenueDescription": "Muddy Puddles",
        "agVenueLatitude": 40.794692,
        "agVenueLongitude": -73.959156,
    },
]

test_event_data = [
    {
        "agEventName": "Sunny Day Test Drive",
        "agEventDate": "2020-02-02T20:21:22",
        "agEventDescription": "A very progressive test run at "
        "Sunnyside Daycare's Butterfly Room.",
    },
    {
        "agEventName": "Peppa Pig Muddy Puddles",
        "agEventDate": "2020-03-01T00:34:57",
        "agEventDescription": "George, "
        "if you jump in muddy puddles, you must wear your boots.",
    },
]

presets_sensor_types = [
    {
        "agSensorTypeID": 0,
        "agSensorTypeName": "Simple Temperature Sensor",
        "agSensorTypeFormula": 0,
        "agSensorTypeFormat": {"reading": {"unit": "Celsius", "format": "float"}},
    },
    {
        "agSensorTypeID": 1,
        "agSensorTypeName": "Dual Temperature Sensor",
        "agSensorTypeFormula": 0,
        "agSensorTypeFormat": {
            "internal": {"unit": "Keivin", "format": "float"},
            "external": {"unit": "Keivin", "format": "float"},
        },
    },
]

test_sensor_data = [
    {"agSensorName": "Simple Temperature Sensor", "agSensorType": 0},
    {"agSensorName": "Sample Dual Temperature", "agSensorType": 1},
]
