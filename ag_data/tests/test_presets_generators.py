from decimal import Decimal
from random import randint

from django.test import TestCase
from django.utils.dateparse import parse_datetime

from ag_data.models import AGVenue, AGEvent, AGSensor
from ag_data.presets import sample_user_data as presets
from ag_data import utilities

from ag_data.presets import presets_generators


class CreateVenueFromPresetsAtIndexTest(TestCase):
    def setUp(self):
        self.totalTestVenues = len(presets.sample_venues)

    def test_in_range(self):
        for index in range(self.totalTestVenues):
            reference = presets.sample_venues[index]

            venue = presets_generators.createVenueFromPresetAtIndex(index)
            venue = AGVenue.objects.get(pk=venue.uuid)

            self.assertEqual(venue.name, reference["agVenueName"])
            self.assertEqual(venue.description, reference["agVenueDescription"])
            self.assertEqual(venue.latitude, Decimal(str(reference["agVenueLatitude"])))
            self.assertEqual(
                venue.longitude, Decimal(str(reference["agVenueLongitude"]))
            )

    def test_out_of_range(self):
        with self.assertRaises(Exception) as e:
            presets_generators.createVenueFromPresetAtIndex(self.totalTestVenues)
        correct_exception_message = (
            "Cannot find requested venue (index "
            + str(self.totalTestVenues)
            + ") from presets"
        )
        self.assertEqual(str(e.exception), correct_exception_message)

    def test_multiple(self):
        for index in range(self.totalTestVenues):
            presets_generators.createVenueFromPresetAtIndex(index)

        self.assertEqual(self.totalTestVenues, AGVenue.objects.count())


class CreateEventFromPresetsAtIndexTest(TestCase):
    def setUp(self):
        self.totalTestEvents = len(presets.sample_events)

        randomVenuePresetIndex = randint(0, len(presets.sample_venues) - 1)
        self.testVenue = presets_generators.createVenueFromPresetAtIndex(
            randomVenuePresetIndex
        )

    def test_in_range(self):
        for index in range(self.totalTestEvents):
            reference = presets.sample_events[index]

            eventReturned = presets_generators.createEventFromPresetAtIndex(
                self.testVenue, index
            )

            event = AGEvent.objects.get(pk=eventReturned.uuid)

            self.assertEqual(eventReturned, event)

            self.assertEqual(event.name, reference["agEventName"])
            self.assertEqual(event.date, parse_datetime(reference["agEventDate"]))
            self.assertEqual(event.description, reference["agEventDescription"])
            self.assertEqual(event.venue_uuid, self.testVenue)

    def test_out_of_range(self):
        with self.assertRaises(Exception) as e:
            presets_generators.createEventFromPresetAtIndex(
                self.testVenue, self.totalTestEvents
            )
        correct_exception_message = (
            "Cannot find requested event (index "
            + str(self.totalTestEvents)
            + ") from presets"
        )
        self.assertEqual(str(e.exception), correct_exception_message)

    def test_multiple(self):
        for index in range(self.totalTestEvents):
            presets_generators.createEventFromPresetAtIndex(self.testVenue, index)

        self.assertEqual(self.totalTestEvents, AGEvent.objects.count())


class CreateSensorFromPresetsAtIndexTest(TestCase):
    def setUp(self):
        self.totalTestSensors = len(presets.sample_sensors)

        utilities.createOrResetAllBuiltInSensorTypes()

    def test_in_range(self):
        for index in range(self.totalTestSensors):
            reference = presets.sample_sensors[index]

            sensor = presets_generators.createSensorFromPresetAtIndex(index)
            sensor = AGSensor.objects.get(pk=sensor.id)

            self.assertEqual(sensor.name, reference["agSensorName"])
            self.assertEqual(sensor.type_id.id, reference["agSensorType"])

    def test_out_of_range(self):
        with self.assertRaises(Exception) as e:
            presets_generators.createSensorFromPresetAtIndex(self.totalTestSensors)
        correct_exception_message = (
            "Cannot find requested sensor (index "
            + str(self.totalTestSensors)
            + ") from presets"
        )
        self.assertEqual(str(e.exception), correct_exception_message)

    def test_multiple(self):
        for index in range(self.totalTestSensors):
            presets_generators.createSensorFromPresetAtIndex(index)

        self.assertEqual(self.totalTestSensors, AGSensor.objects.count())
