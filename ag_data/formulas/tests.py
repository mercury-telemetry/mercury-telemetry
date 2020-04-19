from django.test import TestCase

from ag_data.formulas.pipeline import FormulaPipeline
from ag_data.models import AGEvent, AGVenue, AGSensorType, AGSensor
from ag_data.formulas import formulas

import datetime


def get_formula_id(f):
    for fid, formula in formulas.formula_map.items():
        if formula == f:
            return fid


class FormulaPipelineTests(TestCase):
    fixtures = ["sample.json"]

    def setUp(self):
        self.venue = AGVenue.objects.first()
        self.event = AGEvent.objects.first()
        self.pipeline = FormulaPipeline(event=self.event)
        self.timestamp = datetime.datetime.now()

    def test_save_measurement_flow(self):
        formula_id = get_formula_id(formulas.flow_sensor)
        sensor_type = AGSensorType.objects.filter(processing_formula=formula_id).first()
        sensor = AGSensor.objects.create(name="Test Sensor", type_id=sensor_type)

        result = self.pipeline.save_measurement(
            sensor, self.timestamp, {"volumetricFlow": 2.0}
        )
        self.assertEqual(result.timestamp, self.timestamp)
        self.assertEqual(result.event_uuid, self.event)
        self.assertEqual(result.sensor_id, sensor)

        self.timestamp += datetime.timedelta(seconds=5)
        result = self.pipeline.save_measurement(
            sensor, self.timestamp, {"volumetricFlow": 1.0}
        )
        self.assertEqual(result.timestamp, self.timestamp)
        self.assertEqual(result.event_uuid, self.event)
        self.assertEqual(result.sensor_id, sensor)

    def test_save_measurement_dual_temperature(self):
        formula_id = get_formula_id(formulas.dual_temperature_sensor)
        sensor_type = AGSensorType.objects.filter(processing_formula=formula_id).first()
        sensor = AGSensor.objects.create(name="Test Sensor", type_id=sensor_type)

        result = self.pipeline.save_measurement(
            sensor, self.timestamp, {"internal": 2.0, "external": 1.0}
        )
        self.assertEqual(result.timestamp, self.timestamp)
        self.assertEqual(result.event_uuid, self.event)
        self.assertEqual(result.sensor_id, sensor)

    def test_save_measurement_identity(self):
        formula_id = get_formula_id(formulas.identity)
        sensor_type = AGSensorType.objects.filter(processing_formula=formula_id).first()
        sensor = AGSensor.objects.create(name="Test Sensor", type_id=sensor_type)

        result = self.pipeline.save_measurement(
            sensor, self.timestamp, {"internal": 2.0, "external": 1.0}
        )
        self.assertEqual(result.timestamp, self.timestamp)
        self.assertEqual(result.event_uuid, self.event)
        self.assertEqual(result.sensor_id, sensor)


class FormulaTests(TestCase):
    fixtures = ["sample.json"]

    def test_identity(self):
        self.assertEqual(formulas.identity(), {})
        self.assertEqual(formulas.identity(randomkey=10), {"randomkey": 10})

    def test_simple_temperature_sensor(self):
        self.assertEqual(
            formulas.simple_temperature_sensor(temperature=10), {"temperature": 10}
        )

    def test_dual_temperature_sensor(self):
        res = formulas.dual_temperature_sensor(internal=1, external=2)
        self.assertEqual(res, {"mean": 1.5, "diff": -1})

    def test_flow_sensor(self):
        now = datetime.datetime.now()
        res = formulas.flow_sensor(
            prevGasLevel=None, prevTimestamp=None, volumetricFlow=1, timestamp=now
        )
        self.assertEqual(res, {"gasLevel": 100})

        now, then = now + datetime.timedelta(seconds=10), now
        res = formulas.flow_sensor(
            prevGasLevel=100, prevTimestamp=then, volumetricFlow=2, timestamp=now
        )
        self.assertEqual(res, {"gasLevel": 80})
