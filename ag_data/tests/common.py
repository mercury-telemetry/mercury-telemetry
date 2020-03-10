from ag_data.models import AGEvent

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

test_sensor_data = [
    {
        "agSensorName": "Simple Temperature Sensor",
        "agSensorFormula": 0,
        "agSensorFormat": {"reading": {"unit": "Celsius", "format": "float"}},
    },
    {
        "agSensorName": "Dual Temperature Sensor",
        "agSensorFormula": 0,
        "agSensorFormat": {
            "internal": {"unit": "Keivin", "format": "float"},
            "external": {"unit": "Keivin", "format": "float"},
        },
    },
]


def create_event(event_data):
    return AGEvent(
        event_name=event_data["agEventName"],
        event_date=event_data["agEventDate"],
        event_description=event_data["agEventDescription"],
    )
