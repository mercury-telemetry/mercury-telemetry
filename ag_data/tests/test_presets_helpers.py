from decimal import Decimal
from random import randint

from django.test import TestCase
from django.utils.dateparse import parse_datetime

from ag_data.models import AGVenue, AGEvent, AGSensorType, AGSensor, AGMeasurement
from ag_data.presets import sample_user_data as presets
from ag_data import utilities

from ag_data.presets import helpers


class CreateVenueFromPresetsAtIndexTest(TestCase):
    def test_in_range(self):
        totalTestVenues = len(presets.sample_venues)

        for index in range(totalTestVenues):
            reference = presets.sample_venues[index]

            venue = helpers.createVenueFromPresetAtIndex(index)
            venue = AGVenue.objects.get(pk=venue.uuid)

            self.assertEqual(venue.name, reference["agVenueName"])
            self.assertEqual(venue.description, reference["agVenueDescription"])
            self.assertEqual(venue.latitude, Decimal(str(reference["agVenueLatitude"])))
            self.assertEqual(
                venue.longitude, Decimal(str(reference["agVenueLongitude"]))
            )

    def test_out_of_range(self):
        totalTestVenues = len(presets.sample_venues)

        with self.assertRaises(Exception) as e:
            helpers.createVenueFromPresetAtIndex(totalTestVenues)
        correct_exception_message = (
            "Cannot find requested venue (index "
            + str(totalTestVenues)
            + ") from presets"
        )
        self.assertEqual(str(e.exception), correct_exception_message)

    def test_multiple(self):
        totalTestVenues = len(presets.sample_venues)

        for index in range(totalTestVenues):
            reference = presets.sample_venues[index]

            venue = helpers.createVenueFromPresetAtIndex(index)

        self.assertEqual(totalTestVenues, AGVenue.objects.count())


class CreateEventFromPresetsAtIndexTest(TestCase):
    def setUp(self):
        self.totalTestEvents = len(presets.sample_events)

        randomVenuePresetIndex = randint(0, len(presets.sample_venues) - 1)
        self.testVenue = helpers.createVenueFromPresetAtIndex(randomVenuePresetIndex)

    def test_in_range(self):
        for index in range(self.totalTestEvents):
            reference = presets.sample_events[index]

            eventReturned = helpers.createEventFromPresetAtIndex(self.testVenue, index)

            event = AGEvent.objects.get(pk=eventReturned.uuid)

            self.assertEqual(eventReturned, event)

            self.assertEqual(event.name, reference["agEventName"])
            self.assertEqual(event.date, parse_datetime(reference["agEventDate"]))
            self.assertEqual(event.description, reference["agEventDescription"])
            self.assertEqual(event.venue_uuid, self.testVenue)

    def test_out_of_range(self):
        with self.assertRaises(Exception) as e:
            helpers.createEventFromPresetAtIndex(self.testVenue, self.totalTestEvents)
        correct_exception_message = (
            "Cannot find requested event (index "
            + str(self.totalTestEvents)
            + ") from presets"
        )
        self.assertEqual(str(e.exception), correct_exception_message)

    def test_multiple(self):
        for index in range(self.totalTestEvents):
            reference = presets.sample_events[index]

            event = helpers.createEventFromPresetAtIndex(self.testVenue, index)

        self.assertEqual(self.totalTestEvents, AGEvent.objects.count())


class CreateSensorFromPresetsAtIndexTest(TestCase):
    def test_in_range(self):
        totalTestSensors = len(presets.sample_sensors)
        utilities.createOrResetAllBuiltInSensorTypes()

        for index in range(totalTestSensors):
            reference = presets.sample_sensors[index]

            sensor = helpers.createSensorFromPresetAtIndex(index)
            sensor = AGSensor.objects.get(pk=sensor.id)

            self.assertEqual(sensor.name, reference["agSensorName"])
            self.assertEqual(sensor.type_id.id, reference["agSensorType"])

    def test_out_of_range(self):
        totalTestSensors = len(presets.sample_sensors)

        with self.assertRaises(Exception) as e:
            helpers.createSensorFromPresetAtIndex(totalTestSensors)
        correct_exception_message = (
            "Cannot find requested sensor (index "
            + str(totalTestSensors)
            + ") from presets"
        )
        self.assertEqual(str(e.exception), correct_exception_message)

    def test_multiple(self):
        totalTestSensors = len(presets.sample_sensors)
        utilities.createOrResetAllBuiltInSensorTypes()

        for index in range(totalTestSensors):
            reference = presets.sample_sensors[index]

            sensor = helpers.createSensorFromPresetAtIndex(index)

        self.assertEqual(totalTestSensors, AGSensor.objects.count())
