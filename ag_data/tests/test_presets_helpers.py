from decimal import Decimal

from django.test import TestCase
from django.utils.dateparse import parse_datetime

from ag_data.models import AGVenue, AGEvent, AGSensorType, AGSensor, AGMeasurement
from ag_data import presets


class PresetsHelpersTest(TestCase):
    def inactive_test_simulator_create_venue(self):  # FIXME: reactivate this test
        totalTestVenues = len(presets.venue_presets)

        # test venue creation for indices in range
        for index in range(totalTestVenues):
            self.sim.createAVenueFromPresets(index)
            current_venue = presets.venue_presets[index]

            venue = AGVenue.objects.get(pk=self.sim.venue.uuid)
            self.assertEqual(venue.name, current_venue["agVenueName"])
            self.assertEqual((venue.description), current_venue["agVenueDescription"])
            self.assertEqual(
                venue.latitude, Decimal(str(current_venue["agVenueLatitude"]))
            )
            self.assertEqual(
                venue.longitude, Decimal(str(current_venue["agVenueLongitude"]))
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

    def inactive_test_simulator_create_event(self):  # FIXME: reactivate this test
        totalTestEvents = len(presets.event_presets)

        # test event creation for indices in range
        for index in range(totalTestEvents):
            self.sim.createAVenueFromPresets(index)
            self.sim.createAnEventFromPresets(index)
            current_event = presets.event_presets[index]

            event = AGEvent.objects.get(pk=self.sim.event.uuid)
            self.assertEqual(event.name, current_event["agEventName"])
            self.assertEqual((event.date), parse_datetime(current_event["agEventDate"]))
            self.assertEqual(event.description, current_event["agEventDescription"])

        # test event creation for index out of range
        with self.assertRaises(Exception) as e:
            self.sim.createAnEventFromPresets(totalTestEvents)
        correct_exception_message = (
            "Cannot find requested event (index "
            + str(totalTestEvents)
            + ") from presets"
        )
        self.assertEqual(str(e.exception), correct_exception_message)

    def inactive_test_simulator_create_sensor(self):  # FIXME: reactivate this test
        totalTestSensors = len(presets.sensor_presets)

        # test sensor creation for indices in range
        for index in range(totalTestSensors):
            # create the corresponding sensor type, if it is not present
            sensorTypeID = presets.sensor_presets[index]["agSensorType"]
            self.sim.createOrResetASensorTypeFromPresets(sensorTypeID)

            self.sim.createASensorFromPresets(index)
            current_sensor = presets.sensor_presets[index]

            sensor = AGSensor.objects.get(pk=self.sim.sensor.id)
            self.assertEqual(sensor.name, current_sensor["agSensorName"])

        # test sensor creation for index out of range
        with self.assertRaises(Exception) as e:
            self.sim.createASensorFromPresets(totalTestSensors)
        correct_exception_message = (
            "Cannot find requested sensor (index "
            + str(totalTestSensors)
            + ") from presets"
        )
        self.assertEqual(str(e.exception), correct_exception_message)

    def inactive_test_multiple_sensors(self):  # FIXME: reactivate this test

        self.assertEqual(AGVenue.objects.all().count(), 2)
        self.assertEqual(AGEvent.objects.all().count(), 2)
        self.assertEqual(AGSensorType.objects.all().count(), 1)
        self.assertEqual(AGSensor.objects.all().count(), 2)
        self.assertEqual(AGMeasurement.objects.all().count(), 25)

    def inactive_test_create_sensor_type(self):  # FIXME: reactivate this test
        totalTestSensorTypes = len(presets.sensor_type_presets)

        # test sensor type creation for indices in range
        for index in range(totalTestSensorTypes):
            self.sim.createOrResetASensorTypeFromPresets(index)

            expected_type_id = presets.sensor_type_presets[index]

            sensorType = AGSensorType.objects.get(pk=self.sim.sensorType.id)
            self.assertEqual(sensorType.name, expected_type_id["agSensorTypeName"])
            self.assertEqual(
                sensorType.processing_formula, expected_type_id["agSensorTypeFormula"]
            )
            self.assertEqual(sensorType.format, expected_type_id["agSensorTypeFormat"])

            # test when the method is called when the record already exists

            sensorType.name = expected_type_id["agSensorTypeName"] + " "
            sensorType.processing_formula = expected_type_id["agSensorTypeFormula"] + 1
            sensorType.format = [expected_type_id["agSensorTypeFormat"]]
            sensorType.save()

            self.sim.createOrResetASensorTypeFromPresets(index)
            sensorType = AGSensorType.objects.get(pk=self.sim.sensorType.id)

            self.assertEqual(sensorType.name, expected_type_id["agSensorTypeName"])
            self.assertEqual(
                sensorType.processing_formula, expected_type_id["agSensorTypeFormula"]
            )
            self.assertEqual(sensorType.format, expected_type_id["agSensorTypeFormat"])

        # test sensor type creation for index out of range
        with self.assertRaises(Exception) as e:
            self.sim.createOrResetASensorTypeFromPresets(totalTestSensorTypes)
        correct_exception_message = (
            "Cannot find requested sensor type (index "
            + str(totalTestSensorTypes)
            + ") from presets"
        )
        self.assertEqual(str(e.exception), correct_exception_message)
