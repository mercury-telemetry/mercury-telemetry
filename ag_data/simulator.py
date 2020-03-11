from random import gauss
from time import sleep

from django.utils import timezone

from ag_data import models
from ag_data import presets


class Simulator:

    venue = None
    event = None
    sensorType = None
    sensor = None

    def createAVenueFromPresets(self, index):
        """Create a venue from available presets of venues

        Arguments:

            index {int} -- the index of the sensor preset to use.

        Raises:

            Exception: an exception raises when the index is not valid in presets.
        """

        if index > len(presets.venue_presets) - 1:
            raise Exception(
                "Cannot find requested venue (index " + str(index) + ") from presets"
            )
        else:
            pass

        preset = presets.venue_presets[index]

        self.venue = models.AGVenue.objects.create(
            name=preset["agVenueName"],
            description=preset["agVenueDescription"],
            latitude=preset["agVenueLatitude"],
            longitude=preset["agVenueLongitude"],
        )

    def createAnEventFromPresets(self, index):
        """Create an event from available presets of events

        Arguments:

            index {int} -- the index of the sensor preset to use.

        Raises:

            Exception: an exception raises when the index is not valid in presets.

            Assertion: an assertion error raises when there is no venue prior to the
            creation of the event.
        """

        if index > len(presets.event_presets) - 1:
            raise Exception(
                "Cannot find requested event (index " + str(index) + ") from presets"
            )
        else:
            pass

        preset = presets.event_presets[index]

        self.assertVenue()

        self.event = models.AGEvent.objects.create(
            name=preset["agEventName"],
            date=preset["agEventDate"],
            description=preset["agEventDescription"],
            venue_uuid=self.venue,
        )

    def createOrResetASensorTypeFromPresets(self, index):
        """Create a sensor type object from available presets of sensor types

        The sensor type record is a prerequisite for any sensor whose type is set to this.
        The sensor type ID is also hardcoded in the database. Therefore, for the same sensor
        type, if this method is called when the record exists, it will update the record.

        Arguments:

            index {int} -- the index of the sensor type preset to use.

        Raises:

            Exception: an exception raises when the index is not valid in presets.
        """

        if index > len(presets.type_id_presets) - 1:
            raise Exception(
                "Cannot find requested sensor type (index "
                + str(index)
                + ") from presets"
            )
        else:
            pass

        preset = presets.type_id_presets[index]

        # If the sensor type record does not exist in the table, create the record.
        record = models.AGSensorType.objects.filter(id=preset["agSensorTypeID"])

        if record.count() == 0:
            self.sensorType = models.AGSensorType.objects.create(
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

    def createASensorFromPresets(self, index, cascadeCreation=False):
        """Create a sensor from available presets of sensors

        Arguments:

            index {int} -- the index of the sensor preset to use.

            cascadeCreation {bool=False} -- whether or not to create a corresponding sensor
            type which the chosen sensor preset needs (default: {False})

        Raises:

            Exception: an exception raises when the index is not valid in presets.
        """

        if index > len(presets.sensor_presets) - 1:
            raise Exception(
                "Cannot find requested sensor (index " + str(index) + ") from presets"
            )
        else:
            pass

        preset = presets.sensor_presets[index]

        if cascadeCreation:
            self.createOrResetASensorTypeFromPresets(preset["agSensorType"])
        else:
            self.assertSensorType()

        self.sensor = models.AGSensor.objects.create(
            name=preset["agSensorName"], type_id=self.sensorType
        )

    def logSingleMeasurement(self, timestamp):
        """Create a single measurement for simulated sensor, from supported presets:

        - (index `0`) For a solo temperature sensor, the measurement is marked with
        `reading`. Readings are around 23°C (+/- 3°C), shifted with Gaussian distribution.

        - (index `1`) For a dual temperature sensor, the measurement is marked with `inner`
        and `outside`. `inner` readings are around 15°C (+/- 3°C), shifted with Gaussian
        distribution. `outside` readings are around 20°C (+/- 2°C), shifted with Gaussian
        distribution.

        Arguments:

            timestamp {datetime} -- the exact moment this new measurement is read from the
            virtual sensor

        Raises:

            Exception: an exception raises when the simulator does not have valid event or
            sensor.
        """

        self.assertVenue()
        self.assertEvent()
        self.assertSensor()

        if self.checkSensorFormat(0):
            return models.AGMeasurement.objects.create(
                timestamp=timestamp,
                measurement_event=self.event,
                sensor_id=self.sensor,
                value={"reading": gauss(23, 3)},
            )
        elif self.checkSensorFormat(1):
            return models.AGMeasurement.objects.create(
                timestamp=timestamp,
                measurement_event=self.event,
                sensor_id=self.sensor,
                value={"internal": gauss(15, 3), "external": gauss(20, 2)},
            )

    def checkSensorFormat(self, index):
        return (
            self.sensor.type_id.format
            == presets.type_id_presets[index]["agSensorTypeFormat"]
        )

    def logMeasurementsInThePastSeconds(
        self, seconds, frequencyInHz, printProgress=True
    ):
        """Create as many measurements from the past till current time as needed
        with the specified time range and frequency.

        Arguments:

            seconds {int} -- The time range in seconds for generated measurements

            frequencyInHz {int} -- sampling frequency for the simulated sensor
        """

        startTime = timezone.now()
        earliestReading = startTime - timezone.timedelta(seconds=seconds)
        sampleInterval = 1 / frequencyInHz
        count = 0
        totalMeasurements = int(seconds * frequencyInHz)

        for count in range(totalMeasurements):
            timeAtReading = earliestReading + timezone.timedelta(
                seconds=count / frequencyInHz + gauss(0, sampleInterval)
            )
            self.logSingleMeasurement(timeAtReading)
            if printProgress is True and count % 1000 == 0:
                print(
                    "("
                    + "{:3.3f}%".format(count / totalMeasurements * 100)
                    + ") Created "
                    + str(count)
                    + " measurements"
                )

        if printProgress is True:
            print(
                "({}% done!) Created ".format(100)
                + str(totalMeasurements)
                + " measurements"
            )

        endTime = timezone.now()
        if printProgress is True:
            print("Time elapsed: " + str(endTime - startTime))

    def logLiveMeasurements(self, frequencyInHz, sleepTimer=0):
        """log measurements as they generate in real time.

        Here, the definition of "live" is defined as achieving at least 70% of insertion
        in the unit test at frequency 1Hz - 100Hz for up to 15 seconds. In the case which
        tests of this method cannot pass on a specific machine, some common causes to look
        into include:

        - Some sensor types require heavier resources to generate data, as each execution
        of the unit test may choose random sensor type in the simulator.
        - Database connection is limited, which impacts insertion performance, causing
        following measurements to halt.
        - Frequency for measurement generation is too high. The device running this program
        does not have enough resources to generate required sensor measurements. Please
        notice that for some sensors, data generation use various random number generations
        extensively.

        Arguments:

            frequencyInHz {float} -- frequency for measurement generation. This method will
            do its best to achieve the frequency at its best.

        Keyword Arguments:

            sleepTimer {float} -- time in seconds before automatically stop generate new
            measurements. (default: {0} which will result in generating measurements
            infinitely)
        """

        startTime = timezone.now()
        stopTime = startTime + timezone.timedelta(seconds=sleepTimer)
        sampleInterval = 1 / frequencyInHz
        cycleEnd = startTime

        while True:
            self.logSingleMeasurement(timezone.now())
            if sleepTimer != 0 and stopTime < timezone.now():
                break
            cycleEnd = cycleEnd + timezone.timedelta(
                microseconds=sampleInterval * 1000000
            )
            intervalOffset = (cycleEnd - timezone.now()).microseconds / 1000000
            sleepInterval = sampleInterval - intervalOffset
            if sleepInterval < 0:
                sleepInterval = sleepInterval * sampleInterval
            sleep(sampleInterval)

    def assertVenue(self):
        assert isinstance(
            self.venue, models.AGVenue
        ), "No venue registered in the simulator. Create one first before calling this."

    def assertEvent(self):
        assert isinstance(
            self.event, models.AGEvent
        ), "No event registered in the simulator. Create one first before calling this."

    def assertSensorType(self):
        assert isinstance(self.sensorType, models.AGSensorType), (
            "No sensor type registered in the simulator. "
            + "Create one first before calling this."
        )

    def assertSensor(self):
        assert isinstance(
            self.sensor, models.AGSensor
        ), "No sensor registered in the simulator. Create one first before calling this."
