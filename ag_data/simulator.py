from time import sleep
from random import gauss, random

from django.utils import timezone

from ag_data.formulas.ingestion_engine import MeasurementIngestionEngine
from ag_data import utilities


class Simulator:

    event = None
    sensor = None
    engine = MeasurementIngestionEngine()

    def setUp(self, event, sensor):
        self.event = event
        self.sensor = sensor

    def logProcessedSingleMeasurement(self, timestamp, value):
        utilities.assertEvent(self.event)
        utilities.assertSensor(self.sensor)

        measurementDict = {
            "measurement_timestamp": timestamp,
            "measurement_sensor": self.sensor.id,
            "measurement_values": value,
        }

        return self.engine.saveMeasurement(measurementDict, self.event)

    def logSingleMeasurement(self, timestamp):

        utilities.assertEvent(self.event)
        utilities.assertSensor(self.sensor)

        value = self.generateMeasurementPayload()

        return self.logProcessedSingleMeasurement(timestamp, value)

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

        elif self.checkSensorType(8):
            payload = {"sample": gauss(0.5, 0.5)}

        else:
            raise ValueError(f"Unsupported sensor type ({self.sensor.type_id})")

        return payload

    def logMeasurementsInThePastSeconds(
        self, seconds, frequencyInHz, printProgress=True
    ):
        """Create as many measurements from the past till current time as needed
        with the specified time range and frequency.
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
                    f"({(count / totalMeasurements * 100):3.3f}%"
                    f") Created {str(count)} measurements"
                )

        if printProgress is True:
            print(f"(100% done!) Created {totalMeasurements} measurements")

        endTime = timezone.now()
        if printProgress is True:
            print("Time elapsed: " + str(endTime - startTime))

    def logLiveMeasurements(self, frequencyInHz, sleepTimerInSeconds=0):
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
        """

        startTime = timezone.now()
        stopTime = startTime + timezone.timedelta(seconds=sleepTimerInSeconds)
        sampleInterval = 1 / frequencyInHz
        cycleEnd = startTime

        while True:
            self.logSingleMeasurement(timezone.now())
            if sleepTimerInSeconds != 0 and stopTime < timezone.now():
                break
            cycleEnd = cycleEnd + timezone.timedelta(
                microseconds=sampleInterval * 1000000
            )
            intervalOffset = (cycleEnd - timezone.now()).microseconds / 1000000
            sleepInterval = sampleInterval - intervalOffset
            if sleepInterval < 0:
                sleepInterval = sleepInterval * sampleInterval
            sleep(sampleInterval)
