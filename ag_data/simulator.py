from random import gauss
from time import sleep

from django.utils import timezone

from ag_data import models
from ag_data.tests import common


class Simulator:

    event = None
    sensor = None

    def createAnEventFromPresets(self, index):
        """Create an event from available presets of events

        Arguments:

            index {int} -- the index of the sensor preset to use.

        Raises:

            Exception: an exception raises when the index is not valid in presets.
        """
        if index > len(common.test_event_data) - 1:
            raise Exception(
                "Cannot find requested event (index " + str(index) + ") from presets"
            )
        else:
            pass

        test_event_data = common.test_event_data[index]

        self.event = models.AGEvent.objects.create(
            event_name=test_event_data["agEventName"],
            event_date=test_event_data["agEventDate"],
            event_description=test_event_data["agEventDescription"],
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
            sensor_description=test_sensor_data["agSensorDescription"],
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

        # FIXME: handle situations when self.event or self.sensor is invalid
        assert isinstance(self.event, models.AGEvent), "No event registered in the simulator"
        assert isinstance(self.sensor, models.AGSensor), "No sensor registered in the simulator"

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

    def logContinuousRealTimeMeasurements(self, frequencyInHz, sleepTimer=0):
        startTime = timezone.now()
        stopTime = startTime + timezone.timedelta(seconds=sleepTimer)
        while True:
            self.logMeasurementsInThePastSeconds(
                1, frequencyInHz, printProgress=False
            )
            sampleInterval = 1 / frequencyInHz
            sleep(sampleInterval)
            if sleepTimer != 0 and stopTime < timezone.now():
                break
