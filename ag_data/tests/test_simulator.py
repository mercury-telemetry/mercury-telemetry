from random import randint

from django.test import TestCase
from django.utils.dateparse import parse_datetime
from django.utils import timezone

from ag_data.simulator import Simulator
from ag_data.models import AGEvent, AGSensor, AGMeasurement
from ag_data.tests.common import test_event_data, test_sensor_data


class SimulatorTest(TestCase):
    def test_simulator_creation(self):
        sim = Simulator()
        self.assertEqual(sim.event, None)
        self.assertEqual(sim.sensor, None)

    def test_simulator_create_event(self):
        sim = Simulator()
        totalTestEvents = len(test_event_data)
        # test event creation for indices in range
        for index in range(totalTestEvents):
            sim.createAnEventFromPresets(index)
            current_event = test_event_data[index]

            event = AGEvent.objects.get(pk=sim.event.event_uuid)
            self.assertEqual(event.event_name, current_event["agEventName"])
            self.assertEqual(
                (event.event_date), parse_datetime(current_event["agEventDate"])
            )
            self.assertEqual(
                event.event_description, current_event["agEventDescription"]
            )

        # test event creation for index out of range
        with self.assertRaises(Exception) as e:
            sim.createAnEventFromPresets(totalTestEvents)
        correct_exception_message = (
            "Cannot find requested event (index "
            + str(totalTestEvents)
            + ") from presets"
        )
        self.assertEqual(str(e.exception), correct_exception_message)

    def test_simulator_create_sensor(self):
        sim = Simulator()
        totalTestSensors = len(test_sensor_data)
        # test sensor creation for indices in range
        for index in range(totalTestSensors):
            sim.createASensorFromPresets(index)
            current_sensor = test_sensor_data[index]

            sensor = AGSensor.objects.get(pk=sim.sensor.sensor_id)
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
            sim.createASensorFromPresets(totalTestSensors)
        correct_exception_message = (
            "Cannot find requested sensor (index "
            + str(totalTestSensors)
            + ") from presets"
        )
        self.assertEqual(str(e.exception), correct_exception_message)

    def test_simulator_log_single_measurement_no_event(self):
        randSensorIndex = randint(0, len(test_sensor_data) - 1)

        sim = Simulator()
        sim.createASensorFromPresets(randSensorIndex)

        with self.assertRaises(AssertionError) as ae:
            timestamp = timezone.now()
            sim.logSingleMeasurement(timestamp=timestamp)
        correct_assertion_message = "No event registered in the simulator"
        self.assertEqual(str(ae.exception), correct_assertion_message)

    def test_simulator_log_single_measurement_no_sensor(self):
        randEventIndex = randint(0, len(test_event_data) - 1)

        sim = Simulator()
        sim.createAnEventFromPresets(randEventIndex)

        with self.assertRaises(AssertionError) as ae:
            timestamp = timezone.now()
            sim.logSingleMeasurement(timestamp=timestamp)
        correct_assertion_message = "No sensor registered in the simulator"
        self.assertEqual(str(ae.exception), correct_assertion_message)

    def test_simulator_log_single_measurement(self):
        randEventIndex = randint(0, len(test_event_data) - 1)
        randSensorIndex = randint(0, len(test_sensor_data) - 1)

        sim = Simulator()
        sim.createAnEventFromPresets(randEventIndex)
        sim.createASensorFromPresets(randSensorIndex)

        timestamp = timezone.now()
        measurement = sim.logSingleMeasurement(timestamp=timestamp)

        # test data in database
        measurement_in_database = AGMeasurement.objects.get(
            pk=measurement.measurement_uuid
        )
        self.assertEqual(measurement_in_database.measurement_timestamp, timestamp)
        self.assertEqual(measurement_in_database.measurement_event, sim.event)
        self.assertEqual(measurement_in_database.measurement_sensor, sim.sensor)

        # test measurement payload format
        measurement_payload = measurement_in_database.measurement_value
        correct_payload_format = test_sensor_data[randSensorIndex]["agSensorFormat"]
        for field in measurement_payload.keys():
            self.assertIn(field, measurement_payload.keys())

        # FIXME: test string/number restriant
