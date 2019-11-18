from .models import (
    TemperatureSensor,
    AccelerationSensor,
    WheelSpeedSensor,
    SuspensionSensor,
    FuelLevelSensor,
)

ID_TO_SENSOR_MAP = {
    1: TemperatureSensor,
    2: AccelerationSensor,
    3: WheelSpeedSensor,
    4: SuspensionSensor,
    5: FuelLevelSensor,
}

# example_can_msg = "1000000000010000001000000010000000000000000100000000000"
example_can_msg = "1000000000110000001000000010000000000000000100000000000"


class CANDecoder:
    def __init__(self, message):
        self.message = message
        self.sensor_type = None
        self.data = None

    def read_bits(self, num_bits):
        """This function reads <num_bits> number of bits from the message 
        and returns the most significant bits and modifies the message with those
        most significant bits removed."""
        this_value = self.message[0:num_bits]
        self.message = self.message[num_bits:]
        return this_value

    def decode_can_message(self):
        # we need the binary representation of the integer
        try:
            self.message = bin(int(self.message))
        except ValueError:
            return False

        self.message = bin(int(example_can_msg, 2))
        # the first two chars are '0b', so strip them out
        self.message = self.message[2:]

        # Start of Frame
        sof, = self.read_bits(1)

        # Arbitration Field
        # ID, defines the ECU that sent this message
        can_id = self.read_bits(11)
        sensor_type = ID_TO_SENSOR_MAP[int(can_id, 2)]

        rtr = self.read_bits(1)

        # the control field is a 6-bit field that contains the length of the
        # data in bytes, so read n bits where n is 8 * control_field
        ide = self.read_bits(1)
        r0 = self.read_bits(1)

        control_field = self.read_bits(4)
        data = self.read_bits(int(control_field, 2) * 8)

        # CRC Field
        crc = self.read_bits(15)
        crc_delimiter = self.read_bits(1)

        # ACK Field
        ack_bit = self.read_bits(1)
        ack_delimiter = self.read_bits(1)

        # EOF
        end_of_frame = self.read_bits(7)

        # IFS
        interframe_space = self.read_bits(3)
        return sensor_type, can_id, data
