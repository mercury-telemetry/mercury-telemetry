from decimal import Decimal

from django.test import TestCase
from django.utils.dateparse import parse_datetime

from ag_data.models import AGVenue, AGEvent, AGSensorType, AGSensor, AGMeasurement
from ag_data.presets import sample_user_data as presets
from ag_data import utilities

from ag_data.presets import helpers


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

    def inactive_test_multiple_sensors(self):  # FIXME: reactivate this test

        self.assertEqual(AGVenue.objects.all().count(), 2)
        self.assertEqual(AGEvent.objects.all().count(), 2)
        self.assertEqual(AGSensorType.objects.all().count(), 1)
        self.assertEqual(AGSensor.objects.all().count(), 2)
        self.assertEqual(AGMeasurement.objects.all().count(), 25)
