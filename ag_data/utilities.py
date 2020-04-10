from ag_data import models
from ag_data.presets.built_in_content import built_in_sensor_types


def createOrResetAllBuiltInSensorTypes():
    for index in range(len(built_in_sensor_types)):
        sensorType = createOrResetBuiltInSensorTypeAtPresetIndex(index)
        assertSensorType(sensorType)


def createOrResetBuiltInSensorTypeAtPresetIndex(index):
    """Create a sensor type object from available presets of sensor types

        The sensor type record is a prerequisite for any sensor whose type is set to this.
        The sensor type ID is also hardcoded in the database. Therefore, for the same sensor
        type, if this method is called when the record exists, it will update the record.

        Arguments:

            index {int} -- the index of the sensor type preset to use.

        Raises:

            Exception: an exception raises when the index is not valid in presets.
        """

    if index > len(built_in_sensor_types) - 1:
        raise Exception(
            "Cannot find requested sensor type (index " + str(index) + ") from presets"
        )
    else:
        pass

    preset = built_in_sensor_types[index]

    # If the sensor type record does not exist in the table, create the record.
    record = models.AGSensorType.objects.filter(id=preset["agSensorTypeID"])

    sensorType = None

    if record.count() == 0:
        sensorType = models.AGSensorType.objects.create(
            id=preset["agSensorTypeID"],
            name=preset["agSensorTypeName"],
            processing_formula=preset["agSensorTypeFormula"],
            format=preset["agSensorTypeFormat"],
        )
    else:
        record = record.first()
        record.name = preset["agSensorTypeName"]
        record.processing_formula = preset["agSensorTypeFormula"]
        record.format = preset["agSensorTypeFormat"]
        record.save()
        sensorType = record

    return sensorType


def createCustomSensorType(name, processing_formula, format):
    sensorType = models.AGSensorType.objects.create(
        id=getNextAvailableSensorTypeID(),
        name=name,
        processing_formula=processing_formula,
        format=format,
    )

    return sensorType


def assertVenue(venue):
    assert isinstance(venue, models.AGVenue), "Not an instance of AGVenue."


def assertEvent(event):
    assert isinstance(event, models.AGEvent), "Not an instance of AGEvent"


def assertSensorType(sensorType):
    assert isinstance(
        sensorType, models.AGSensorType
    ), "Not an instance of AGSensorType."


def assertSensor(sensor):
    assert isinstance(sensor, models.AGSensor), "Not an instance of AGSensor."


def getNextAvailableSensorTypeID():
    sensorTypeWithMaxID = models.AGSensorType.objects.latest("id")
    maxID = sensorTypeWithMaxID.id
    if maxID % 2 == 0:
        maxID = maxID + 1
    else:
        maxID = maxID + 2

    return maxID
