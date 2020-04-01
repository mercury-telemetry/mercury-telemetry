from random import gauss, random
from time import sleep

from django.utils import timezone

from ag_data import utilities


class Simulator:

    venue = None
    event = None
    sensor = None

    def setUp(self, venue, event, sensor):
        self.venue = venue
        self.event = event
        self.sensor = sensor

    def logProcessedSingleMeasurement(self, timestamp, value):
        utilities.assertVenue(self.venue)
        utilities.assertEvent(self.event)
        utilities.assertSensor(self.sensor)

        measurementDict = {
            "measurement_timestamp": timestamp,
            "measurement_sensor": self.sensor.id,
            "measurement_values": value,
        }

        from ag_data.formulas.ingestion_engine import MeasurementIngestionEngine

        engine = MeasurementIngestionEngine()
        engine.event = self.event

        engine.saveMeasurement(measurementDict)

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

        utilities.assertVenue(self.venue)
        utilities.assertEvent(self.event)
        utilities.assertSensor(self.sensor)

        value = self.generateMeasurementPayload()

        self.logProcessedSingleMeasurement(timestamp, value)

    def checkSensorType(self, typeID):
        return self.sensor.type_id.id == typeID

    def generateMeasurementPayload(self):
        utilities.assertSensor(self.sensor)

        payload = None

        if self.checkSensorType(0):
            payload = {"side": (random() < 0.5)}

        elif self.checkSensorType(2):
            payload = {"reading": gauss(23, 1)}

        elif self.checkSensorType(4):
            payload = {"internal": gauss(15, 3), "external": gauss(20, 2)}

        elif self.checkSensorType(6):
            payload = {"volumetricFlow": gauss(0.2, 0.15)}

        elif self.checkSensorType(6):
            payload = {"sample": gauss(0.5, 0.5)}

        return payload

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
