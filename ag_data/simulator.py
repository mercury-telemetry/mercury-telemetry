from random import gauss
from time import sleep

from django.utils import timezone

from ag_data import models
from ag_data.tests import common


class Simulator:

    venue = None
    event = None
    sensor = None

    def createAVenueFromPresets(self, index):
        """Create a venue from available presets of venues

        Arguments:

            index {int} -- the index of the sensor preset to use.

        Raises:

            Exception: an exception raises when the index is not valid in presets.
        """
        if index > len(common.test_venue_data) - 1:
            raise Exception(
                "Cannot find requested venue (index " + str(index) + ") from presets"
            )
        else:
            pass

        test_venue_data = common.test_venue_data[index]

        self.venue = models.AGVenue.objects.create(
            venue_name=test_venue_data["agVenueName"],
            venue_description=test_venue_data["agVenueDescription"],
            venue_latitude=test_venue_data["agVenueLatitude"],
            venue_longitude=test_venue_data["agVenueLongitude"],
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
        if index > len(common.test_event_data) - 1:
            raise Exception(
                "Cannot find requested event (index " + str(index) + ") from presets"
            )
        else:
            pass

        test_event_data = common.test_event_data[index]

        self.assertVenue()

        self.event = models.AGEvent.objects.create(
            event_name=test_event_data["agEventName"],
            event_date=test_event_data["agEventDate"],
            event_description=test_event_data["agEventDescription"],
            event_venue=self.venue,
        )

    def createASensorFromPresets(self, index):
        """Create a sensor from available presets of sensors

        Arguments:

            index {int} -- the index of the sensor preset to use.

        Raises:

            Exception: an exception raises when the index is not valid in presets.
        """
        if index > len(common.test_event_data) - 1:
            raise Exception(
                "Cannot find requested sensor (index " + str(index) + ") from presets"
            )
        else:
            pass

        test_sensor_data = common.test_sensor_data[index]

        self.sensor = models.AGSensor.objects.create(
            sensor_name=test_sensor_data["agSensorName"],
            sensor_processing_formula=test_sensor_data["agSensorFormula"],
            sensor_format=test_sensor_data["agSensorFormat"],
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

        self.assertEvent()
        self.assertSensor()

        if self.checkSensorFormat(0):
            return models.AGMeasurement.objects.create(
                measurement_timestamp=timestamp,
                measurement_event=self.event,
                measurement_sensor=self.sensor,
                measurement_value={"reading": gauss(23, 3)},
            )
        elif self.checkSensorFormat(1):
            return models.AGMeasurement.objects.create(
                measurement_timestamp=timestamp,
                measurement_event=self.event,
                measurement_sensor=self.sensor,
                measurement_value={"internal": gauss(15, 3), "external": gauss(20, 2)},
            )

    def checkSensorFormat(self, index):
        return (
            self.sensor.sensor_format
            == common.test_sensor_data[index]["agSensorFormat"]
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

    def assertSensor(self):
        assert isinstance(
            self.sensor, models.AGSensor
        ), "No sensor registered in the simulator. Create one first before calling this."
