from random import randint, uniform

from django.test import TestCase
from django.utils import timezone

from ag_data.simulator import Simulator
from ag_data.models import AGMeasurement
from ag_data.presets import helpers as preset_helpers
from ag_data.presets import built_in_content as bic
from ag_data.presets import sample_user_data


class SimulatorTest(TestCase):
    def setUp(self):
        self.sim = Simulator()
        self.venue = preset_helpers.createVenueFromPresetAtIndex(0)
        self.event = preset_helpers.createEventFromPresetAtIndex(self.venue, 0)

        # self.sim.venue = self.venue
        # self.sim.event = self.event

    def test_simulator_creation(self):
        self.assertEqual(self.sim.venue, None)
        self.assertEqual(self.sim.event, None)
        self.assertEqual(self.sim.sensor, None)

    def inactive_test_simulator_log_single_measurement_no_venue(self):
        # FIXME: reactivate this test

        self.sim.createASensorFromPresets(
            self.randSensorIndex(), cascadeCreation=True
        )  # FIXME: another condition

        with self.assertRaises(AssertionError) as ae:
            timestamp = timezone.now()
            self.sim.logSingleMeasurement(timestamp=timestamp)
        correct_assertion_message = (
            "No venue registered in the simulator. "
            + "Create one first before calling this."
        )
        self.assertEqual(str(ae.exception), correct_assertion_message)

    def inactive_test_simulator_log_single_measurement_no_event(self):
        # FIXME: reactivate this test

        self.sim.createAVenueFromPresets(self.randVenueIndex())
        self.sim.createASensorFromPresets(
            self.randSensorIndex(), cascadeCreation=True
        )  # FIXME: another condition

        with self.assertRaises(AssertionError) as ae:
            timestamp = timezone.now()
            self.sim.logSingleMeasurement(timestamp=timestamp)
        correct_assertion_message = (
            "No event registered in the simulator. "
            + "Create one first before calling this."
        )
        self.assertEqual(str(ae.exception), correct_assertion_message)

    def inactive_test_simulator_log_single_measurement_no_sensor(self):
        # FIXME: reactivate this test

        self.sim.createAVenueFromPresets(self.randVenueIndex())
        self.sim.createAnEventFromPresets(self.randEventIndex())

        with self.assertRaises(AssertionError) as ae:
            timestamp = timezone.now()
            self.sim.logSingleMeasurement(timestamp=timestamp)
        correct_assertion_message = (
            "No sensor registered in the simulator. "
            + "Create one first before calling this."
        )
        self.assertEqual(str(ae.exception), correct_assertion_message)

    def inactive_test_simulator_log_single_measurement(self):
        # FIXME: reactivate this test

        randEventIndex = self.randEventIndex()

        self.sim.createAVenueFromPresets(self.randVenueIndex())
        self.sim.createAnEventFromPresets(randEventIndex)

        for index in range(len(bic.built_in_sensor_types)):
            self.sim.createASensorFromPresets(
                index, cascadeCreation=True
            )  # FIXME: add another condition

            timestamp = timezone.now()
            measurement = self.sim.logSingleMeasurement(timestamp=timestamp)

            # test data in database
            measurement_in_database = AGMeasurement.objects.get(pk=measurement.uuid)
            self.assertEqual(measurement_in_database.timestamp, timestamp)
            self.assertEqual(measurement_in_database.event_uuid, self.sim.event)
            self.assertEqual(measurement_in_database.sensor_id, self.sim.sensor)

            # test measurement payload format by cross comparison of all keys in payload
            # and the expected specification
            measurement_payload = measurement_in_database.value
            correct_payload_format = bic.built_in_sensor_types[index][
                "agSensorTypeFormat"
            ]

            # NOTE: limitation: this only checks the keys at root level of the payload
            for field in correct_payload_format.keys():
                self.assertIn(field, measurement_payload.keys())
            for field in measurement_payload.keys():
                self.assertIn(field, correct_payload_format.keys())

            # FIXME: test string/number restriant

    def inactive_test_simulator_log_multiple_measurements(self):
        # FIXME: reactivate this test

        import sys
        from io import StringIO

        self.sim.createAVenueFromPresets(self.randVenueIndex())
        self.sim.createAnEventFromPresets(self.randEventIndex())
        self.sim.createASensorFromPresets(
            self.randSensorIndex(), cascadeCreation=True
        )  # FIXME: add another condition

        randFrequencyInHz = uniform(1, 100)
        randSeconds = uniform(1, 60)

        self.sim.logMeasurementsInThePastSeconds(
            seconds=randSeconds, frequencyInHz=randFrequencyInHz, printProgress=False
        )

        # test number of measurements
        totalMeasurementsInDatabase = (
            AGMeasurement.objects.filter(event_uuid=self.sim.event)
            .filter(sensor_id=self.sim.sensor)
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

    def inactive_test_simulator_log_continuous_measurements(self):
        # FIXME: reactivate this test

        """Tests the logLiveMeasurements(self, frequencyInHz, sleepTimer) method in the
        Simulator class. By default, it will run the test 10 times.

        To run this test case only, and to stop testing when any failure is encountered,
        use this single command:

        python manage.py test ag_data.tests.test_simulator.SimulatorTest.
        test_simulator_log_continuous_measurements --failfast
        """
        randVenueIndex = self.randVenueIndex()
        randEventIndex = self.randEventIndex()
        randSensorIndex = self.randSensorIndex()

        # Change the number of loops for testing on demand
        for i in range(1):
            self.sim.createAVenueFromPresets(randVenueIndex)
            self.sim.createAnEventFromPresets(randEventIndex)
            self.sim.createASensorFromPresets(
                randSensorIndex, cascadeCreation=True
            )  # FIXME: add another condition

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
                AGMeasurement.objects.filter(event_uuid=self.sim.event)
                .filter(sensor_id=self.sim.sensor)
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

    def randVenueIndex(self):
        return randint(0, len(sample_user_data.sample_venues) - 1)

    def randEventIndex(self):
        return randint(0, len(sample_user_data.sample_events) - 1)

    def randSensorIndex(self):
        return randint(0, len(sample_user_data.sample_sensors) - 1)
