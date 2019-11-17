from django.test import TestCase
import datetime
from mercury.models import (
    SimulatedData,
    TemperatureSensor,
    AccelerationSensor,
    WheelSpeedSensor,
    SuspensionSensor,
    FuelLevelSensor,
)

# Test Values
TEST_TEMP = 999.0
TEST_ACCEL_Y = 9.81
TEST_WHEEL_SPEED_FR = 30
TEST_SUSPENSION_FR = 2
TEST_FUEL = 6


def create_simulated_data_objects():
    SimulatedData.objects.create(
        temperature=TEST_TEMP, created_at=datetime.datetime.now()
    )
    TemperatureSensor.objects.create(
        temperature=TEST_TEMP, created_at=datetime.datetime.now()
    )
    AccelerationSensor.objects.create(
        acceleration_x=TEST_ACCEL_Y, created_at=datetime.datetime.now()
    )
    WheelSpeedSensor.objects.create(
        wheel_speed_fr=TEST_WHEEL_SPEED_FR, created_at=datetime.datetime.now()
    )
    SuspensionSensor.objects.create(
        suspension_fr=TEST_SUSPENSION_FR, created_at=datetime.datetime.now()
    )
    FuelLevelSensor.objects.create(
        current_fuel_level=TEST_FUEL, created_at=datetime.datetime.now()
    )


class TestSensorModels(TestCase):
    def setUp(self):
        create_simulated_data_objects()

    def test_vehicle_temp(self):
        foo = SimulatedData.objects.get(temperature=TEST_TEMP)
        self.assertEqual(foo.temperature, TEST_TEMP)

    def test_vehicle_temp_method(self):
        foo = SimulatedData()
        foo.temperature = 987
        self.assertEqual(foo.temp(), 987)

    def test_temp(self):
        foo = TemperatureSensor.objects.get(temperature=TEST_TEMP)
        self.assertEqual(foo.temperature, TEST_TEMP)

    def test_acceleration(self):
        foo = AccelerationSensor.objects.get(acceleration_x=TEST_ACCEL_Y)
        self.assertEqual(foo.acceleration_x, TEST_ACCEL_Y)

    def test_wheel_speed(self):
        foo = WheelSpeedSensor.objects.get(wheel_speed_fr=TEST_WHEEL_SPEED_FR)
        self.assertEqual(foo.wheel_speed_fr, TEST_WHEEL_SPEED_FR)

    def test_suspension(self):
        foo = SuspensionSensor.objects.get(suspension_fr=TEST_SUSPENSION_FR)
        self.assertEqual(foo.suspension_fr, TEST_SUSPENSION_FR)

    def test_fuel_level(self):
        foo = FuelLevelSensor.objects.get(current_fuel_level=TEST_FUEL)
        self.assertEqual(foo.current_fuel_level, TEST_FUEL)
