from django.test import TestCase
from mercury.can import CANDecoder
from mercury.models import (
    SimulatedData,
    TemperatureSensor,
    AccelerationSensor,
    WheelSpeedSensor,
    SuspensionSensor,
    FuelLevelSensor,
)

EXAMPLE_CAN_MSG = "1000000000110000001000000010000000000000000100000000000"


class TestCANDecoder(TestCase):
    def test_can_decode(self):
        decoder = CANDecoder(EXAMPLE_CAN_MSG)
        sensor, can_id, data = decoder.decode_can_message()
        self.assertEqual(sensor, WheelSpeedSensor)
        self.assertNotEqual(sensor, SuspensionSensor)
