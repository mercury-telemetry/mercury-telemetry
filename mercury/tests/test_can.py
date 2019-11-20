from django.test import TestCase
from mercury.can import CANDecoder
from mercury.models import (
    TemperatureSensor,
    AccelerationSensor,
    WheelSpeedSensor,
    SuspensionSensor,
    FuelLevelSensor,
)

EXAMPLE_CAN_MSG = 0b1000000000110100001000000010000000000000001110000000000
EXAMPLE_CAN_MSG_EXTENDED = (
    0b10000000001101000000000000000000000001000000010000000000000001110000000000
)


class TestCANDecoderExtended(TestCase):
    def setUp(self) -> None:
        decoder = CANDecoder(EXAMPLE_CAN_MSG_EXTENDED)
        sensor, self.data = decoder.decode_can_message_full_dict()

    def test_can_1s(self):
        self.assertEqual(1, self.data["ack_delimiter"])
        self.assertEqual(1, self.data["crc_delimiter"])


class TestCANSensors(TestCase):
    def setUp(self) -> None:
        """The CAN messages here are of no magic significant other than they were
        verified by a human to meet the implementation requirements of the CAN decoder
        and mapping to Sensors."""
        self.temp_model, self.temp_data = CANDecoder(
            0b1000000000010000001000000010000000000000001110000000000
        ).decode_can_message()
        self.accel_model, self.accel_data = CANDecoder(
            0b1000000000100000001000000010000000000000001110000000000
        ).decode_can_message()
        self.wheel_speed_model, self.wheel_speed_data = CANDecoder(
            0b1000000000110000001000000010000000000000001110000000000
        ).decode_can_message()
        self.suspension_model, self.suspension_data = CANDecoder(
            0b1000000001000000001000000010000000000000001110000000000
        ).decode_can_message()
        self.fuel_model, self.fuel_data = CANDecoder(
            0b1000000001010000001000000010000000000000001110000000000
        ).decode_can_message()

    def test_can_sensor_identification(self):
        self.assertEqual(TemperatureSensor, self.temp_model)
        self.assertEqual(AccelerationSensor, self.accel_model)
        self.assertEqual(WheelSpeedSensor, self.wheel_speed_model)
        self.assertEqual(SuspensionSensor, self.suspension_model)
        self.assertEqual(FuelLevelSensor, self.fuel_model)
