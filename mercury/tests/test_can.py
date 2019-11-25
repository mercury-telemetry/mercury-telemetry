from django.test import TestCase
from mercury.can import CANDecoder, InvalidBitException, MessageLengthException
from mercury.can_map import CANMapper
from mercury.models import (
    TemperatureSensor,
    AccelerationSensor,
    WheelSpeedSensor,
    SuspensionSensor,
    FuelLevelSensor,
)

# EXAMPLE_CAN_MSG_INT = 0b1000000000110100001000000010000000000000001110000000000
EXAMPLE_CAN_MSG_EXTENDED = (
    0b10000000001101000000000000000000000001000000010000000000000001110000000000
)


class TestCANDRecessiveBits(TestCase):
    def setUp(self) -> None:
        decoder = CANDecoder(EXAMPLE_CAN_MSG_EXTENDED)
        self.data = decoder.decode_can_message()

    def test_can_1s(self):
        self.assertEqual(1, self.data["ack_delimiter"])
        self.assertEqual(1, self.data["crc_delimiter"])


class TestCANSensorIdentification(TestCase):
    def setUp(self) -> None:
        """The CAN messages here are of no magic significant other than they were
        verified by a human to meet the implementation requirements of the CAN decoder
        and mapping to Sensors."""
        self.temp_data = CANDecoder(
            0b100000000001000100000000001000000010000000100000001000000010000000100000001000000010000000000000001110000000000  # noqa E501
        ).decode_can_message()
        self.accel_data = CANDecoder(
            0b1000000000100000001000000010000000000000001110000000000
        ).decode_can_message()
        self.wheel_speed_data = CANDecoder(
            0b1000000000110000001000000010000000000000001110000000000
        ).decode_can_message()
        self.suspension_data = CANDecoder(
            0b1000000001000000001000000010000000000000001110000000000
        ).decode_can_message()
        self.fuel_data = CANDecoder(
            0b1000000001010000001000000010000000000000001110000000000
        ).decode_can_message()

    def test_can_sensor_identification(self):
        temp_model = CANMapper(self.temp_data).get_sensor_from_id()
        self.assertEqual(TemperatureSensor, temp_model)

        accel_model = CANMapper(self.accel_data).get_sensor_from_id()
        self.assertEqual(AccelerationSensor, accel_model)

        wheel_speed_model = CANMapper(self.wheel_speed_data).get_sensor_from_id()
        self.assertEqual(WheelSpeedSensor, wheel_speed_model)

        suspension_model = CANMapper(self.suspension_data).get_sensor_from_id()
        self.assertEqual(SuspensionSensor, suspension_model)

        fuel_model = CANMapper(self.fuel_data).get_sensor_from_id()
        self.assertEqual(FuelLevelSensor, fuel_model)

        none_model_int = CANMapper({"can_id": 9999}).get_sensor_from_id()
        self.assertEqual(None, none_model_int)
        none_model_str = CANMapper({"can_id": "doesnotexit"}).get_sensor_from_id()
        self.assertEqual(None, none_model_str)


class TestCANInputTypes(TestCase):
    def setUp(self) -> None:
        binary_number_decoder = CANDecoder(
            0b10000000001101000000000000000000000001000000010000000000000001110000000000
        )
        self.bin_data = binary_number_decoder.decode_can_message()
        binary_string_decoder = CANDecoder(
            "0b10000000001101000000000000000000000001000000010000000000000001110000000000"
        )
        self.bin_str_data = binary_string_decoder.decode_can_message()
        integer_decoder = CANDecoder(9459720945368167357440)
        self.int_data = integer_decoder.decode_can_message()
        bytes_decoder = CANDecoder(
            b"0b10000000001101000000000000000000000001000000010000000000000001110000000000"
        )
        self.bytes_data = bytes_decoder.decode_can_message()

    def test_input_equivalency(self):
        self.assertEqual(self.bin_data, self.bin_str_data)
        self.assertEqual(self.bin_str_data, self.int_data)
        self.assertEqual(self.int_data, self.bytes_data)


class TestCANExceptions(TestCase):
    def test_msg_length_exception(self):
        with self.assertRaises(MessageLengthException) as cm:
            temp_data = CANDecoder(
                0b100000000001000100000000001000000010000000100000001000000010000000100000001000000010000000000000001110000000000000000000000000000000000  # noqa E501
            )

    def test_invalid_bit_crc(self):
        temp_data = CANDecoder(
            0b10000000001101000000000000000000000001000000010000000000000000110000000000
        )
        with self.assertRaises(InvalidBitException) as cm:
            temp_data.decode_can_message()

    def test_invalid_bit_ack(self):
        temp_data = CANDecoder(
            0b10000000001101000000000000000000000001000000010000000000000001100000000000
        )
        with self.assertRaises(InvalidBitException) as cm:
            temp_data.decode_can_message()

    def test_value_error_for_int_as_str_caught(self):
        temp_data = CANDecoder(
            "9459720945368167357440"
        )
        self.assertTrue(isinstance(temp_data, CANDecoder))
