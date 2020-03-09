from random import randint, uniform

from django.test import TestCase
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from ag_data.simulator import Simulator
from ag_data.models import AGEvent, AGSensor, AGMeasurement
from ag_data.tests.common import test_event_data, test_sensor_data


class SimulatorTest(TestCase):
    def setUp(self):
        self.sim = Simulator()

    def test_simulator_creation(self):
        self.assertEqual(self.sim.event, None)
        self.assertEqual(self.sim.sensor, None)

    def test_simulator_create_event(self):
        totalTestEvents = len(test_event_data)
        # test event creation for indices in range
        for index in range(totalTestEvents):
            self.sim.createAnEventFromPresets(index)
            current_event = test_event_data[index]

            event = AGEvent.objects.get(pk=self.sim.event.event_uuid)
            self.assertEqual(event.event_name, current_event["agEventName"])
            self.assertEqual(
                (event.event_date), parse_datetime(current_event["agEventDate"])
            )
            self.assertEqual(
                event.event_description, current_event["agEventDescription"]
            )

        # test event creation for index out of range
        with self.assertRaises(Exception) as e:
            self.sim.createAnEventFromPresets(totalTestEvents)
        correct_exception_message = (
            "Cannot find requested event (index "
            + str(totalTestEvents)
            + ") from presets"
        )
        self.assertEqual(str(e.exception), correct_exception_message)

    def test_simulator_create_sensor(self):
        totalTestSensors = len(test_sensor_data)
        # test sensor creation for indices in range
        for index in range(totalTestSensors):
            self.sim.createASensorFromPresets(index)
            current_sensor = test_sensor_data[index]

            sensor = AGSensor.objects.get(pk=self.sim.sensor.sensor_id)
            self.assertEqual(sensor.sensor_name, current_sensor["agSensorName"])
            self.assertEqual(
                sensor.sensor_description, current_sensor["agSensorDescription"]
            )
            self.assertEqual(
                sensor.sensor_processing_formula, current_sensor["agSensorFormula"]
            )
            self.assertEqual(sensor.sensor_format, current_sensor["agSensorFormat"])

        # test sensor creation for index out of range
        with self.assertRaises(Exception) as e:
            self.sim.createASensorFromPresets(totalTestSensors)
        correct_exception_message = (
            "Cannot find requested sensor (index "
            + str(totalTestSensors)
            + ") from presets"
        )
        self.assertEqual(str(e.exception), correct_exception_message)

    def test_simulator_log_single_measurement_no_event(self):
        randSensorIndex = randint(0, len(test_sensor_data) - 1)

        self.sim.createASensorFromPresets(randSensorIndex)

        with self.assertRaises(AssertionError) as ae:
            timestamp = timezone.now()
            self.sim.logSingleMeasurement(timestamp=timestamp)
        correct_assertion_message = "No event registered in the simulator"
        self.assertEqual(str(ae.exception), correct_assertion_message)

    def test_simulator_log_single_measurement_no_sensor(self):
        randEventIndex = randint(0, len(test_event_data) - 1)

        self.sim.createAnEventFromPresets(randEventIndex)

        with self.assertRaises(AssertionError) as ae:
            timestamp = timezone.now()
            self.sim.logSingleMeasurement(timestamp=timestamp)
        correct_assertion_message = "No sensor registered in the simulator"
        self.assertEqual(str(ae.exception), correct_assertion_message)

    def test_simulator_log_single_measurement(self):
        randEventIndex = randint(0, len(test_event_data) - 1)

        self.sim.createAnEventFromPresets(randEventIndex)

        for index in range(len(test_sensor_data)):
            self.sim.createASensorFromPresets(index)

            timestamp = timezone.now()
            measurement = self.sim.logSingleMeasurement(timestamp=timestamp)

            # test data in database
            measurement_in_database = AGMeasurement.objects.get(
                pk=measurement.measurement_uuid
            )
            self.assertEqual(measurement_in_database.measurement_timestamp, timestamp)
            self.assertEqual(measurement_in_database.measurement_event, self.sim.event)
            self.assertEqual(
                measurement_in_database.measurement_sensor, self.sim.sensor
            )

            # test measurement payload format by cross comparison of all keys in payload
            # and the expected specification
            measurement_payload = measurement_in_database.measurement_value
            correct_payload_format = test_sensor_data[index]["agSensorFormat"]

            # NOTE: limitation: this only checks the keys at root level of the payload
            for field in correct_payload_format.keys():
                self.assertIn(field, measurement_payload.keys())
            for field in measurement_payload.keys():
                self.assertIn(field, correct_payload_format.keys())

            # FIXME: test string/number restriant

    def test_simulator_log_multiple_measurements(self):
        import sys
        from io import StringIO

        randEventIndex = randint(0, len(test_event_data) - 1)
        randSensorIndex = randint(0, len(test_sensor_data) - 1)

        self.sim.createAnEventFromPresets(randEventIndex)
        self.sim.createASensorFromPresets(randSensorIndex)

        randFrequencyInHz = uniform(1, 100)
        randSeconds = uniform(1, 60)

        self.sim.logMeasurementsInThePastSeconds(
            seconds=randSeconds, frequencyInHz=randFrequencyInHz, printProgress=False
        )

        # test number of measurements
        totalMeasurementsInDatabase = (
            AGMeasurement.objects.filter(measurement_event=self.sim.event)
            .filter(measurement_sensor=self.sim.sensor)
            .count()
        )
        self.assertEqual(
            totalMeasurementsInDatabase, int(randSeconds * randFrequencyInHz)
        )

        # test output prompts
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            self.sim.logMeasurementsInThePastSeconds(
                seconds=randSeconds, frequencyInHz=randFrequencyInHz
            )
            outputString = out.getvalue().strip()
            self.assertIn("({}% done!) Created ".format(100), outputString)
            self.assertIn(str(totalMeasurementsInDatabase), outputString)
        finally:
            sys.stdout = saved_stdout

    def test_simulator_log_continuous_measurements(self):
        """Tests the logLiveMeasurements(self, frequencyInHz, sleepTimer) method in the
        Simulator class. By default, it will run the test 10 times.

        To run this test case only, and to stop testing when any failure is encountered,
        use this single command:

        python manage.py test ag_data.tests.test_simulator.SimulatorTest.
        test_simulator_log_continuous_measurements --failfast
        """
        randEventIndex = randint(0, len(test_event_data) - 1)
        randSensorIndex = randint(0, len(test_sensor_data) - 1)

        # Change the number of loops for testing on demand
        for i in range(1):
            self.sim.createAnEventFromPresets(randEventIndex)
            self.sim.createASensorFromPresets(randSensorIndex)

            randFrequencyInHz = uniform(1, 100)
            randSleepTimer = uniform(1, 15)

            startTime = timezone.now()

            self.sim.logLiveMeasurements(
                frequencyInHz=randFrequencyInHz, sleepTimer=randSleepTimer
            )

            endTime = timezone.now()
            secondsElapsed = endTime - startTime

            # test sleep timer
            self.assertTrue(
                randSleepTimer - 1 <= secondsElapsed.seconds <= randSleepTimer + 1
            )

            # test total measurement count
            totalMeasurementsInDatabase = (
                AGMeasurement.objects.filter(measurement_event=self.sim.event)
                .filter(measurement_sensor=self.sim.sensor)
                .count()
            )

            expectedTotal = int(randSleepTimer * randFrequencyInHz)

            # If this test fails on a device, uncomment following lines for more info.

            # print("Actual: " + str(totalMeasurementsInDatabase))
            # print("Expected: " + str(expectedTotal))
            # print(
            #     "Completion: {:3.1f}%".format(
            #         totalMeasurementsInDatabase / expectedTotal * 100
            #     )
            # )

            self.assertTrue(
                expectedTotal * 0.7
                <= totalMeasurementsInDatabase
                <= expectedTotal * 1.1
            )
