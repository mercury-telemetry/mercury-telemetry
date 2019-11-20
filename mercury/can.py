from .models import (
    TemperatureSensor,
    AccelerationSensor,
    WheelSpeedSensor,
    SuspensionSensor,
    FuelLevelSensor,
)
import logging

ID_TO_SENSOR_MAP = {
    1: TemperatureSensor,
    2: AccelerationSensor,
    3: WheelSpeedSensor,
    4: SuspensionSensor,
    5: FuelLevelSensor,
}


logging.basicConfig(level=logging.WARN)
log = logging.getLogger(__name__)


class InvalidBitException(Exception):
    def __init__(self, value, field_name):
        self.error = (
            f"An invalid bit value of {value} was decoded for field {field_name}"
        )
        log.error(self.error)


class CANDecoder:
    def __init__(self, message):
        self.message = message
        self.data = {}

    def read_bits(self, num_bits):
        """This function reads <num_bits> number of bits from the message
        and returns the most significant bits and modifies the message with those
        most significant bits removed."""
        this_value = self.message[0:num_bits]
        self.message = self.message[num_bits:]
        return this_value

    def read_bits_as_int(self, num_bits) -> int:
        """Return the bitstrem read as a base-10 integer."""
        bits = self.read_bits(num_bits)
        return int(bits, 2)

    def decode_can_message(self):
        data = self._decode_can_message()
        return data["sensor_type"], data["data"]

    def decode_can_message_full_dict(self) -> dict:
        return self._decode_can_message()

    def _decode_can_message(self) -> dict:
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
        self.data["sof"] = self.read_bits_as_int(1)
        if self.data["sof"] == "0":
            raise InvalidBitException(self.data["sof"], "Start of Frame")

        """Arbitration Field is 12-bits or 32-bits long
        Assume we only have an 11-bit identifiers in this project for now,
        so a 12-bit arbitration field. The 32-bit long field also means the following
        IDE fiels moves out of the control field into arbitration field.
        The ID defines the ECU that sent this message."""
        self.data["can_id"] = self.read_bits_as_int(11)
        self.data["sensor_type"] = ID_TO_SENSOR_MAP[self.data["can_id"]]
        # RTR of 0 means this is a normal data frame
        # RTR of 1 means this is a remote frame, unlikely in our use case
        self.data["rtr"] = self.read_bits_as_int(1)

        """The control field is a 6-bit field that contains the length of the
        data in bytes, so read n bits where n is 8 * data_length_field.
        IDE of 0 uses 11-bit ID format, IDE of 1 uses 29-bit ID format.
        R0 is a reservered spacer field of 1-bit. The SRR field has the value of the
        RTR bit in the extended ID mode, and is not present in the standard
        ID mode."""
        self.data["ide"] = self.read_bits_as_int(1)
        if int(self.data["ide"]) == 1:  # 29-bit ID format, 32-bit arbitration field
            self.data["srr"] = self.data["rtr"]
            self.data["extended_can_id"] = self.read_bits_as_int(18)
            self.data["rtr"] = self.read_bits_as_int(1)
        else:
            self.data["srr"] = None
            self.data["extended_can_id"] = None
        self.data["r0"] = self.read_bits_as_int(1)
        self.data["data_length_code"] = self.read_bits_as_int(4)
        self.data["data"] = self.read_bits_as_int(self.data["data_length_code"] * 8)

        """CRC Field is 16-bits.
        The CRC segment is 15-bits in the field and contains the frame check sequence
        spanning from SOF through Arbitration Field, Control Field, and Data Field.
        The CRC Delimeter bit is always recessive (i.e. 1) following the CRC field."""
        self.data["crc_segment"] = self.read_bits_as_int(15)

        self.data["crc_delimiter"] = self.read_bits_as_int(1)
        if self.data["crc_delimiter"] == "0":
            raise InvalidBitException(self.data["crc_delimiter"], "CRC Delimiter")

        # ACK Field is 2-bits
        # Delimiter is always recessive (1)
        self.data["ack_bit"] = self.read_bits_as_int(1)
        self.data["ack_delimiter"] = self.read_bits_as_int(1)
        if self.data["ack_delimiter"] == "0":
            raise InvalidBitException(self.data["ack_delimiter"], "ACK Delimiter")

        # EOF
        self.data["end_of_frame"] = self.read_bits_as_int(7)

        # IFS
        self.data["interframe_space"] = self.read_bits_as_int(3)
        return self.data
