from django.test import TestCase

from ag_data.models import AGSensorType, AGSensor


class AGSensorTest(TestCase):
    def setUp(self):
        self.sensorType = AGSensorType.objects.create(
            name="test sensor type",
            processing_formula="0",
            format={"key": "value"},
            graph_type=AGSensorType.GRAPH,
        )

        self.foo_serial = 100
        self.foo_name = "sensor foo"
        self.foo_type = self.sensorType

        return super().setUp()

    def test_sensor_creation(self):
        AGSensor.objects.create(
            serial=self.foo_serial, name=self.foo_name, type_id=self.foo_type
        )

        self.assertEqual(AGSensor.objects.all().count(), 1)

        sensor_in_db = AGSensor.objects.all().first()

        self.assertEqual(sensor_in_db.serial, self.foo_serial)
        self.assertEqual(sensor_in_db.name, self.foo_name)
        self.assertEqual(sensor_in_db.type_id, self.foo_type)

    def test_sensor_unique_serial(self):
        sensor_foo = AGSensor.objects.create(
            serial=self.foo_serial, name=self.foo_name, type_id=self.foo_type
        )

        sensor_foo2 = AGSensor.objects.create(
            serial=self.foo_serial, name=self.foo_name, type_id=self.foo_type
        )

        self.assertEqual(AGSensor.objects.all().count(), 2)

        self.assertEqual(sensor_foo.serial, self.foo_serial)

        self.assertEqual(sensor_foo2.serial, self.foo_serial + 1)
        self.assertEqual(sensor_foo2.name, self.foo_name)
        self.assertEqual(sensor_foo2.type_id, self.foo_type)
