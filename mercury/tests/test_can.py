from django.test import TestCase
from mercury.can import CANDecoderTester
from mercury.models import (
    SimulatedData,
    TemperatureSensor,
    AccelerationSensor,
    WheelSpeedSensor,
    SuspensionSensor,
    FuelLevelSensor,
)

EXAMPLE_CAN_MSG = "0b1000000000110100001000000010000000000000001110000000000"
EXAMPLE_CAN_MSG_EXTENDED = (
    0b10000000001101000000000000000000000001000000010000000000000001110000000000
)


class TestCANDecoderExtended(TestCase):
    def setUp(self) -> None:
        decoder = CANDecoderTester(EXAMPLE_CAN_MSG_EXTENDED)

        self.sensor, self.data, self.sof, self.can_id, self.rtr, self.ide, self.srr, self.extended_can_id, self.r0, self.data_length_code, self.crc_segment, self.crc_delimiter, self.ack_bit, self.ack_delimiter, self.end_of_frame, self.interspace_frame = (
            decoder.decode_can_message()
        )

    def test_can_decode_extended(self):
        self.assertEqual(self.sensor, WheelSpeedSensor)
        self.assertNotEqual(self.sensor, SuspensionSensor)

    def test_can_1s(self):
        self.assertEqual(1, self.ack_delimiter)
        self.assertEqual(1, self.crc_delimiter)
