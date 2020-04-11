from django.test import TestCase
from django.utils import timezone

from ag_data.presets import presets_generators
from ag_data import utilities

from ag_data.formulas.ingestion_engine import MeasurementExchange


class MeasurementExchangeTest(TestCase):
    def setUp(self):
        self.venue = presets_generators.createVenueFromPresetAtIndex(0)
        self.event = presets_generators.createEventFromPresetAtIndex(self.venue, 0)

        utilities.createOrResetAllBuiltInSensorTypes()

        self.sensor = presets_generators.createSensorFromPresetAtIndex(0)

    def test_measurement_exchange_creation(self):
        timestamp = timezone.now()
        reading = {}

        measurement_data = MeasurementExchange(
            event=self.event, timestamp=timestamp, sensor=self.sensor, reading=reading
        )

        self.assertIs(measurement_data.event, self.event)
        self.assertIs(measurement_data.timestamp, timestamp)
        self.assertIs(measurement_data.sensor, self.sensor)
        self.assertIs(measurement_data.reading, reading)

        self.assertIs(measurement_data.sensor_type, self.sensor.type_id)
        self.assertIs(
            measurement_data.processing_formula, self.sensor.type_id.processing_formula
        )
