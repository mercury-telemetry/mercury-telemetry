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

EXAMPLE_CAN_MSG = "0b1000000000110100001000000010000000000000001110000000000"
EXAMPLE_CAN_MSG_EXTENDED = 0b10000000001101000000000000000000000001000000010000000000000001110000000000


class TestCANDecoder(TestCase):
    def test_can_decode_extended(self):
        decoder = CANDecoder(EXAMPLE_CAN_MSG_EXTENDED)
        sensor, can_id, data = decoder.decode_can_message()
        self.assertEqual(sensor, WheelSpeedSensor)
        self.assertNotEqual(sensor, SuspensionSensor)
