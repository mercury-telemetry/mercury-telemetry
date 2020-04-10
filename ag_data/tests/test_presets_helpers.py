from decimal import Decimal

from django.test import TestCase
from django.utils.dateparse import parse_datetime

from ag_data.models import AGVenue, AGEvent, AGSensorType, AGSensor, AGMeasurement
from ag_data.presets import sample_user_data as presets
from ag_data import utilities

from ag_data.presets import helpers


class PresetsHelpersTest(TestCase):
    def test_createVenueFromPresetAtIndex_in_range(self):
        totalTestVenues = len(presets.sample_venues)

        for index in range(totalTestVenues):
            reference = presets.sample_venues[index]

            venue = helpers.createVenueFromPresetAtIndex(index)
            venue = AGVenue.objects.get(pk=venue.uuid)

            self.assertEqual(venue.name, reference["agVenueName"])
            self.assertEqual(venue.description, reference["agVenueDescription"])
            self.assertEqual(venue.latitude, Decimal(str(reference["agVenueLatitude"])))
            self.assertEqual(venue.longitude, Decimal(str(reference["agVenueLongitude"])))

    def test_createVenueFromPresetAtIndex_out_of_range(self):
        totalTestVenues = len(presets.sample_venues)

        with self.assertRaises(Exception) as e:
            helpers.createVenueFromPresetAtIndex(totalTestVenues)
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

    def test_createSensorFromPresetAtIndex_in_range(self):
        totalTestSensors = len(presets.sample_sensors)
        utilities.createOrResetAllBuiltInSensorTypes()

        for index in range(totalTestSensors):
            reference = presets.sample_sensors[index]

            sensor = helpers.createSensorFromPresetAtIndex(index)
            sensor = AGSensor.objects.get(pk=sensor.id)

            self.assertEqual(sensor.name, reference["agSensorName"])
            self.assertEqual(sensor.type_id.id, reference["agSensorType"])

    def test_createSensorFromPresetAtIndex_out_of_range(self):
        totalTestSensors = len(presets.sample_sensors)

        with self.assertRaises(Exception) as e:
            helpers.createSensorFromPresetAtIndex(totalTestSensors)
        correct_exception_message = (
            "Cannot find requested sensor (index "
            + str(totalTestSensors)
            + ") from presets"
        )
        self.assertEqual(str(e.exception), correct_exception_message)

    def test_createSensorFromPresetAtIndex_stress(self):
        totalTestSensors = len(presets.sample_sensors)
        utilities.createOrResetAllBuiltInSensorTypes()

        for index in range(totalTestSensors):
            reference = presets.sample_sensors[index]

            sensor = helpers.createSensorFromPresetAtIndex(index)

        self.assertEqual(totalTestSensors, AGSensor.objects.count())
