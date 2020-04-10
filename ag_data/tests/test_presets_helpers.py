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
            self.assertEqual(
                venue.longitude, Decimal(str(reference["agVenueLongitude"]))
            )

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

    def test_createVenueFromPresetAtIndex_multiple(self):
        totalTestVenues = len(presets.sample_venues)

        for index in range(totalTestVenues):
            reference = presets.sample_venues[index]

            venue = helpers.createVenueFromPresetAtIndex(index)

        self.assertEqual(totalTestVenues, AGVenue.objects.count())

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
