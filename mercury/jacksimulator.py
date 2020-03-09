from mercury import models
from random import gauss
from django.utils import timezone
from time import sleep
from . import jack_common

event1 = {}

if models.AGEvent.objects.all().count() == 0:
    test_event_data1 = jack_common.test_event_data["event1"]
    models.AGEvent.objects.create(
        event_name=test_event_data1["agEventName"],
        event_date=test_event_data1["agEventDate"],
        event_description=test_event_data1["agEventDescription"],
        event_location=test_event_data1["agEventLocation"]
    )
else:
    event1 = models.AGEvent.objects.all().first()

sensor1 = {}
sensor2 = {}

if models.AGSensor.objects.all().count() == 0:
    sensor1 = models.AGSensor.objects.create(
        sensor_name="Temperature",
        sensor_processing_formula=0,
        sensor_format={
            "reading": {
                "unit": "Celsius",
                "format": "float"
            }
        }
    )
    sensor2 = models.AGSensor.objects.create(
        sensor_name="Temperature",
        sensor_processing_formula=0,
        sensor_format={
            "internal": {
                "unit": "Keivin",
                "format": "float"
            },
            "external": {
                "unit": "Keivin",
                "format": "float"
            }
        }
    )
else:
    sensor1 = models.AGSensor.objects.all()[0]
    sensor2 = models.AGSensor.objects.all()[1]


def createAMeasurement(timestamp):
    """Create a single measurement for a solo temperature sensor, marked with `reading`.

    Readings are around 23°C (+/- 3°C), shifted with Gaussian distribution.

    Arguments:

        timestamp {datetime} -- the exact moment this new measurement is read from the
        virtual sensor
    """
    models.AGMeasurement.objects.create(
        measurement_timestamp=timestamp,
        measurement_event=event1,
        measurement_sensor=sensor1,
        measurement_value={"reading": gauss(23, 3)},
    )


def createADualMeasurement(timestamp):
    """Create a single measurement for a dual temperature sensor, marked with `inner` and
    `outside`.

    `inner` readings are around 15°C (+/- 3°C), shifted with Gaussian distribution.

    `outside` readings are around 20°C (+/- 2°C), shifted with Gaussian distribution.

    Arguments:

        timestamp {datetime} -- the exact moment (up to microsecond precision) which this
        new reading is measured from the virtual sensor
    """
    models.AGMeasurement.objects.create(
        measurement_timestamp=timestamp,
        measurement_event=event1,
        measurement_sensor=sensor2,
        measurement_value={"internal": gauss(15, 3), "external": gauss(20, 2)},
    )


def createMeasurementsInThePastSeconds(seconds, frequencyInHz):
    """Create as many measurements from the past till current time as needed
    with the specified time range and frequency.

    Arguments:

        seconds {int} -- The time range in seconds for generated measurements

        frequencyInHz {int} -- sampling frequency for the simulated sensor group as a whole
    """
    startTime = timezone.now()
    earliestReading = startTime - timezone.timedelta(seconds=seconds)
    for count in range(int(seconds * frequencyInHz)):
        timeAtReading = earliestReading + timezone.timedelta(
            seconds=count / frequencyInHz + gauss(0, 1)
        )
        if gauss(0, 1) > 0.5:
            createAMeasurement(timeAtReading)
        else:
            createADualMeasurement(timeAtReading)
    endTime = timezone.now()
    print(endTime - startTime)


def createMeasurementsContinuously():
    while True:
        createMeasurementsInThePastSeconds(1, 2)
        sleep(1)


measurement1 = models.AGMeasurement.objects.create(
    measurement_event=event1,
    measurement_sensor=sensor1,
    measurement_value={"reading": gauss(22, 24)},
)
