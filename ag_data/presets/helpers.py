from ag_data import models
from ag_data.presets import sample_user_data
from ag_data import utilities


def createVenueFromPresetAtIndex(index):
    """Create a venue from available presets of venues

    Arguments:

        index {int} -- the index of the sensor preset to use.

    Raises:

        Exception: an exception raises when the index is not valid in presets.
    """

    if index > len(sample_user_data.sample_venues) - 1:
        raise Exception(
            "Cannot find requested venue (index " + str(index) + ") from presets"
        )
    else:
        pass

    preset = sample_user_data.sample_venues[index]

    venue = models.AGVenue.objects.create(
        name=preset["agVenueName"],
        description=preset["agVenueDescription"],
        latitude=preset["agVenueLatitude"],
        longitude=preset["agVenueLongitude"],
    )

    return venue


def createEventFromPresets(venue, index):
    """Create an event from available presets of events

    Arguments:

        index {int} -- the index of the sensor preset to use.

    Raises:

        Exception: an exception raises when the index is not valid in presets.

        Assertion: an assertion error raises when there is no venue prior to the
        creation of the event.
    """

    if index > len(sample_user_data.sample_events) - 1:
        raise Exception(
            "Cannot find requested event (index " + str(index) + ") from presets"
        )
    else:
        pass

    preset = sample_user_data.sample_events[index]

    utilities.assertVenue(venue)

    event = models.AGEvent.objects.create(
        name=preset["agEventName"],
        date=preset["agEventDate"],
        description=preset["agEventDescription"],
        venue_uuid=venue,
    )

    return event


def createSensorFromPresetAtIndex(index):
    """Create a sensor from available presets of sensors

    Arguments:

        index {int} -- the index of the sensor preset to use.

        cascadeCreation {bool=False} -- whether or not to create a corresponding sensor
        type which the chosen sensor preset needs (default: {False})

    Raises:

        Exception: an exception raises when the index is not valid in presets.
    """

    if index > len(sample_user_data.sample_sensors) - 1:
        raise Exception(
            "Cannot find requested sensor (index " + str(index) + ") from presets"
        )
    else:
        pass

    preset = sample_user_data.sample_sensors[index]

    sensorType = models.AGSensorType.objects.get(pk=preset["agSensorType"])
    utilities.assertSensorType(sensorType)

    sensor = models.AGSensor.objects.create(
        name=preset["agSensorName"], type_id=sensorType
    )

    return sensor
