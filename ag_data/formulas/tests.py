from django.test import TestCase

from ag_data.formulas.ingestion_engine import MeasurementIngestionEngine
from ag_data.utilities import MeasurementExchange
from django.utils import timezone
from ag_data.models import AGEvent, AGVenue, AGSensorType, AGSensor, AGMeasurement
from ag_data.formulas.library.system.mercury_formulas import (
    fEmptyResult,
    fMercurySimpleTemperatureSensor,
    fMercuryDualTemperatureSensor,
    fMercuryFlowSensor,
)
import datetime


class MeasurementIngestionEngineTests(TestCase):
    fixtures = ["sample.json"]

    def setUp(self):
        self.venue = AGVenue.objects.first()
        self.event = AGEvent.objects.first()

    def test_save_measurement(self):
        sensor_type = AGSensorType.objects.create(
            name="Coin Side Sensor",
            processing_formula=0,
            format={"reading": {"side": {"unit": "", "format": "bool"}}, "result": {}},
        )
        sensor = AGSensor.objects.create(name="Test Sensor", type_id=sensor_type,)

        engine = MeasurementIngestionEngine()

        measurement = MeasurementExchange(
            event=self.event,
            timestamp=timezone.now(),
            sensor=sensor,
            reading={"side": True},
        )
        result = engine.saveMeasurement(measurement)
        self.assertEqual(result.timestamp, measurement.timestamp)
        self.assertEqual(result.event_uuid, measurement.event)
        self.assertEqual(result.sensor_id, measurement.sensor)


class FormulaTests(TestCase):
    fixtures = ["sample.json"]

    def setUp(self):
        event = AGEvent.objects.first()
        sensor_type = AGSensorType.objects.first()
        sensor = AGSensor.objects.create(name="Test Sensor", type_id=sensor_type,)
        self.measurement = MeasurementExchange(
            event=event,
            timestamp=timezone.now(),
            sensor=sensor,
            reading={"side": True},
        )

    def test_empty_result(self):
        self.measurement.reading = {
            "side": True,
        }
        self.assertEqual(fEmptyResult(self.measurement), {})

        self.measurement.reading = {}
        self.assertEqual(fEmptyResult(self.measurement), {})

        self.measurement.reading = {"random-key": 123, "random-key2": "abc"}
        self.assertEqual(fEmptyResult(self.measurement), {})

    def test_simple_temperature_sensor(self):
        self.measurement.reading = {
            "side": True,
        }
        self.assertEqual(fMercurySimpleTemperatureSensor(self.measurement), {})

        self.measurement.reading = {}
        self.assertEqual(fMercurySimpleTemperatureSensor(self.measurement), {})

        self.measurement.reading = {"random-key": 123, "random-key2": "abc"}
        self.assertEqual(fMercurySimpleTemperatureSensor(self.measurement), {})

    def test_dual_temperature_sensor(self):
        self.measurement.reading = {"internal": 1, "external": 2}
        res = fMercuryDualTemperatureSensor(self.measurement)
        self.assertEqual(res, {"mean": 1.5, "diff": -1})

    def test_flow_sensor(self):
        now = datetime.datetime.now()

        AGMeasurement.objects.filter(sensor_id=self.measurement.sensor.id).delete()

        self.measurement.reading = {"volumetricFlow": 1}
        self.measurement.timestamp = now
        res = fMercuryFlowSensor(self.measurement)

        self.assertEqual(res, {"gasLevel": 100})

        AGMeasurement.objects.create(
            timestamp=now,
            event_uuid=self.measurement.event,
            sensor_id=self.measurement.sensor,
            value={"reading": self.measurement.reading, "result": res},
        )

        self.measurement.reading = {"volumetricFlow": 2}
        now = now + datetime.timedelta(seconds=10)
        self.measurement.timestamp = now
        res = fMercuryFlowSensor(self.measurement)
        self.assertEqual(res, {"gasLevel": 80})
