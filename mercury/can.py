import logging

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)


class InvalidBitException(Exception):
    def __init__(self, value, field_name):
        self.error = (
            f"An invalid bit value of {value} was decoded for field {field_name}"
        )
        log.error(self.error)


class MessageLengthException(Exception):
    def __init__(self, value):
        self.error = (
            f"The CAN message bit string length is {value}, but 130 is the maximum."
        )
        log.error(self.error)


class CANDecoder:
    def __init__(self, message):
        self.message = message
        self.can_data = {}
        log.debug("Message type: {}".format(type(self.message)))
        log.debug("Message: {}".format(self.message))

        # Convert various inputs the binary representation of the integer
        if type(self.message) is bytes:
            self.message = self.message.decode("utf-8")
        if type(self.message) is str:
            try:
                self.message = bin(int(self.message, 2))
            except ValueError:
                self.message = bin(int(self.message))
        elif type(self.message) is int:
            self.message = bin(self.message)

        # 130 bits is the maximum message length
        if len(self.message) > 130:
            raise MessageLengthException(len(self.message))

    def read_bits_as_int(self, num_bits) -> int:
        """Return the bitstream read as a base-10 integer."""
        if num_bits > 0:
            bits = self.read_bits(num_bits)
            log.info(f"bits: {bits}")
            log.info(f"num_bits: {num_bits}")
            return int(bits, 2)

    def read_bits_as_bin(self, num_bits):
        if num_bits > 0:
            return self.read_bits(num_bits)

    def read_bits(self, num_bits):
        """This function reads <num_bits> number of bits from the message
        and returns the most significant bits and modifies the message with those
        most significant bits removed."""
        this_value = self.message[0:num_bits]
        self.message = self.message[num_bits:]
        return this_value

    @staticmethod
    def read_can_data_word(bitstring, word_number):
        return bitstring[(word_number * 16) : ((word_number + 1) * 16)]  # noqa E203

    def decode_can_message(self) -> dict:
        """Decode CAN messages based on reference
        http://www.copperhilltechnologies.com/can-bus-guide-message-frame-format/"""

        # the first two chars are '0b' from bin() conversion, so strip them out
        self.message = self.message[2:]

        # Start of Frame field, 1-bit
        self.can_data["sof"] = self.read_bits_as_int(1)

        """Arbitration Field is 12-bits or 32-bits long
        Assume we only have an 11-bit identifiers in this project for now,
        so a 12-bit arbitration field. The 32-bit long field also means the following
        IDE fiels moves out of the control field into arbitration field.
        The ID defines the ECU that sent this message."""
        self.can_data["can_id"] = self.read_bits_as_int(11)
        # RTR of 0 means this is a normal data frame
        # RTR of 1 means this is a remote frame, unlikely in our use case
        self.can_data["rtr"] = self.read_bits_as_int(1)

        """The control field is a 6-bit field that contains the length of the
        data in bytes, so read n bits where n is 8 * data_length_field.
        IDE of 0 uses 11-bit ID format, IDE of 1 uses 29-bit ID format.
        R0 is a reservered spacer field of 1-bit. The SRR field has the value of the
        RTR bit in the extended ID mode, and is not present in the standard
        ID mode."""
        self.can_data["ide"] = self.read_bits_as_int(1)
        if int(self.can_data["ide"]) == 1:  # 29-bit ID format, 32-bit arbitration field
            self.can_data["srr"] = self.can_data["rtr"]
            self.can_data["extended_can_id"] = self.read_bits_as_int(18)
            self.can_data["rtr"] = self.read_bits_as_int(1)
        else:
            self.can_data["srr"] = None
            self.can_data["extended_can_id"] = None
        self.can_data["r0"] = self.read_bits_as_int(1)
        self.can_data["data_length_code"] = self.read_bits_as_int(4)
        self.can_data["data_bin"] = self.read_bits_as_bin(
            self.can_data["data_length_code"] * 8
        )
        self.can_data["data"] = int(self.can_data["data_bin"], 2)

        """For sensors providing multiple simultaneous values in one field, we will
        delimit at word length (16-bits) and store each word in our data dictionary.
        For sensors with single valued data, we just use the data field. See the
        views/can.py file for ORM declarations."""
        for word in range(self.can_data["data_length_code"] // 2):
            self.can_data[f"data_word_{word}"] = self.read_can_data_word(
                self.can_data["data_bin"], word
            )

        """CRC Field is 16-bits.
        The CRC segment is 15-bits in the field and contains the frame check sequence
        spanning from SOF through Arbitration Field, Control Field, and Data Field.
        The CRC Delimeter bit is always recessive (i.e. 1) following the CRC field."""
        self.can_data["crc_segment"] = self.read_bits_as_int(15)

        self.can_data["crc_delimiter"] = self.read_bits_as_int(1)
        if self.can_data["crc_delimiter"] == 0:
            raise InvalidBitException(self.can_data["crc_delimiter"], "CRC Delimiter")

        # ACK Field is 2-bits
        # Delimiter is always recessive (1)
        self.can_data["ack_bit"] = self.read_bits_as_int(1)
        self.can_data["ack_delimiter"] = self.read_bits_as_int(1)
        if self.can_data["ack_delimiter"] == 0:
            raise InvalidBitException(self.can_data["ack_delimiter"], "ACK Delimiter")

        # EOF
        self.can_data["end_of_frame"] = self.read_bits_as_int(7)

        # IFS
        self.can_data["interframe_space"] = self.read_bits_as_int(3)
        return self.can_data
