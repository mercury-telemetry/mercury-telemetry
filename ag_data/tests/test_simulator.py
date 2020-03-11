from random import randint, uniform
from decimal import Decimal

from django.test import TestCase
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from ag_data.simulator import Simulator
from ag_data.models import AGVenue, AGEvent, AGSensorType, AGSensor, AGMeasurement
from ag_data import presets


class SimulatorTest(TestCase):
    def setUp(self):
        self.sim = Simulator()

    def test_simulator_creation(self):
        self.assertEqual(self.sim.venue, None)
        self.assertEqual(self.sim.event, None)
        self.assertEqual(self.sim.sensor, None)

    def test_simulator_create_venue(self):
        totalTestVenues = len(presets.venue_presets)

        # test venue creation for indices in range
        for index in range(totalTestVenues):
            self.sim.createAVenueFromPresets(index)
            current_venue = presets.venue_presets[index]

            venue = AGVenue.objects.get(pk=self.sim.venue.venue_uuid)
            self.assertEqual(venue.venue_name, current_venue["agVenueName"])
            self.assertEqual(
                (venue.venue_description), current_venue["agVenueDescription"]
            )
            self.assertEqual(
                venue.venue_latitude, Decimal(str(current_venue["agVenueLatitude"]))
            )
            self.assertEqual(
                venue.venue_longitude, Decimal(str(current_venue["agVenueLongitude"]))
            )

        # test event creation for index out of range
        with self.assertRaises(Exception) as e:
            self.sim.createAVenueFromPresets(totalTestVenues)
        correct_exception_message = (
            "Cannot find requested venue (index "
            + str(totalTestVenues)
            + ") from presets"
        )
        self.assertEqual(str(e.exception), correct_exception_message)

    def test_simulator_create_event(self):
        totalTestEvents = len(presets.event_presets)

        # test event creation for indices in range
        for index in range(totalTestEvents):
            self.sim.createAVenueFromPresets(index)
            self.sim.createAnEventFromPresets(index)
            current_event = presets.event_presets[index]

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

    def test_simulator_create_sensor_type(self):
        totalTestSensorTypes = len(presets.sensor_type_presets)

        # test sensor type creation for indices in range
        for index in range(totalTestSensorTypes):
            self.sim.createOrResetASensorTypeFromPresets(index)

            expected_sensor_type = presets.sensor_type_presets[index]

            sensorType = AGSensorType.objects.get(pk=self.sim.sensorType.sensorType_id)
            self.assertEqual(
                sensorType.sensorType_name, expected_sensor_type["agSensorTypeName"]
            )
            self.assertEqual(
                sensorType.sensorType_processingFormula,
                expected_sensor_type["agSensorTypeFormula"],
            )
            self.assertEqual(
                sensorType.sensorType_format, expected_sensor_type["agSensorTypeFormat"]
            )

            # test when the method is called when the record already exists

            sensorType.sensorType_name = expected_sensor_type["agSensorTypeName"] + " "
            sensorType.sensorType_processingFormula = (
                expected_sensor_type["agSensorTypeFormula"] + 1
            )
            sensorType.sensorType_format = [expected_sensor_type["agSensorTypeFormat"]]
            sensorType.save()

            self.sim.createOrResetASensorTypeFromPresets(index)
            sensorType = AGSensorType.objects.get(pk=self.sim.sensorType.sensorType_id)

            self.assertEqual(
                sensorType.sensorType_name, expected_sensor_type["agSensorTypeName"]
            )
            self.assertEqual(
                sensorType.sensorType_processingFormula,
                expected_sensor_type["agSensorTypeFormula"],
            )
            self.assertEqual(
                sensorType.sensorType_format, expected_sensor_type["agSensorTypeFormat"]
            )

        # test sensor type creation for index out of range
        with self.assertRaises(Exception) as e:
            self.sim.createOrResetASensorTypeFromPresets(totalTestSensorTypes)
        correct_exception_message = (
            "Cannot find requested sensor type (index "
            + str(totalTestSensorTypes)
            + ") from presets"
        )
        self.assertEqual(str(e.exception), correct_exception_message)

    def test_simulator_create_sensor(self):
        totalTestSensors = len(presets.sensor_presets)

        # test sensor creation for indices in range
        for index in range(totalTestSensors):
            # create the corresponding sensor type, if it is not present
            sensorTypeID = presets.sensor_presets[index]["agSensorType"]
            self.sim.createOrResetASensorTypeFromPresets(sensorTypeID)

            self.sim.createASensorFromPresets(index)
            current_sensor = presets.sensor_presets[index]

            sensor = AGSensor.objects.get(pk=self.sim.sensor.sensor_id)
            self.assertEqual(sensor.sensor_name, current_sensor["agSensorName"])

        # test sensor creation for index out of range
        with self.assertRaises(Exception) as e:
            self.sim.createASensorFromPresets(totalTestSensors)
        correct_exception_message = (
            "Cannot find requested sensor (index "
            + str(totalTestSensors)
            + ") from presets"
        )
        self.assertEqual(str(e.exception), correct_exception_message)

    def test_simulator_log_single_measurement_no_venue(self):
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

    def test_simulator_log_single_measurement_no_event(self):
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

    def test_simulator_log_single_measurement_no_sensor(self):
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

    def test_simulator_log_single_measurement(self):
        randEventIndex = self.randEventIndex()

        self.sim.createAVenueFromPresets(self.randVenueIndex())
        self.sim.createAnEventFromPresets(randEventIndex)

        for index in range(len(presets.sensor_presets)):
            self.sim.createASensorFromPresets(
                index, cascadeCreation=True
            )  # FIXME: add another condition

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
            correct_payload_format = presets.sensor_type_presets[index][
                "agSensorTypeFormat"
            ]

            # NOTE: limitation: this only checks the keys at root level of the payload
            for field in correct_payload_format.keys():
                self.assertIn(field, measurement_payload.keys())
            for field in measurement_payload.keys():
                self.assertIn(field, correct_payload_format.keys())

            # FIXME: test string/number restriant

    def test_simulator_log_multiple_measurements(self):
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

    def randVenueIndex(self):
        return randint(0, len(presets.venue_presets) - 1)

    def randEventIndex(self):
        return randint(0, len(presets.event_presets) - 1)

    def randSensorIndex(self):
        return randint(0, len(presets.sensor_presets) - 1)
