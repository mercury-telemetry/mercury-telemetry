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
        """Decode CAN messages based on reference
        http://www.copperhilltechnologies.com/can-bus-guide-message-frame-format/"""

        # Use the binary representation of the integer
        try:
            self.message = bin(int(self.message))
        except ValueError:
            return False

        # the first two chars are '0b' from bin() conversion, so strip them out
        self.message = self.message[2:]

        # Start of Frame field, 1-bit
        sof = self.read_bits(1)

        """Arbitration Field is 12-bits or 32-bits long
        Assume we only have an 11-bit identifiers in this project for now,
        so a 12-bit arbitration field. The 32-bit long field also means the following
        IDE fiels moves out of the control field into arbitration field.
        The ID defines the ECU that sent this message."""
        can_id = self.read_bits(11)
        sensor_type = ID_TO_SENSOR_MAP[int(can_id, 2)]
        # RTR of 0 means this is a normal data frame
        # RTR of 1 means this is a remote frame, unlikely in our use case
        rtr = self.read_bits(1)

        """The control field is a 6-bit field that contains the length of the
        data in bytes, so read n bits where n is 8 * data_length_field.
        IDE of 0 uses 11-bit ID format, IDE of 1 uses 29-bit ID format."""
        ide = self.read_bits(1)
        if int(ide) == 1:  # 29-bit ID format, 32-bit arbitration field
            srr = rtr
            extended_can_id = self.read_bits(18)
            rtr = self.read_bits(1)
        r0 = self.read_bits(1)
        data_length_code = self.read_bits(4)
        data = self.read_bits(int(data_length_code, 2) * 8)

        """CRC Field is 16-bits.
        The CRC segment is 15-bits in the field and contains the frame check sequence spanning
        from SOF through Arbitration Field, Control Field, and Data Field.
        The CRC Delimeter bit is always recessive (i.e. 1) following the CRC field."""
        crc = self.read_bits(15)
        crc_delimiter = self.read_bits(1)

        # ACK Field is 2-bits
        # Delimiter is always recessive (1)
        ack_bit = self.read_bits(1)
        ack_delimiter = self.read_bits(1)

        # EOF
        end_of_frame = self.read_bits(7)

        # IFS
        interframe_space = self.read_bits(3)
        return sensor_type, can_id, data
