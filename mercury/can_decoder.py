from .can_sensors import *

example_can_msg = "1000000000010000001000000010000000000000000100000000000"


def read_bits(msg, num_bits):
    this_value = msg[0:num_bits]
    msg = msg[num_bits:]
    return this_value, msg


def decode_can_message(msg):
    # we need the binary representation of the integer
    msg = bin(int(msg))

    msg = bin(int(example_can_msg, 2))
    # the first two chars are '0b', so strip them out
    msg = msg[2:]

    # Start of Frame
    sof, msg = read_bits(msg, 1)

    # Arbitration Field
    # ID, defines the ECU that sent this message
    msg_id, msg = read_bits(msg, 11)
    rtr, msg = read_bits(msg, 1)

    # the control field is a 6-bit field that contains the length of the
    # data in bytes, so read n bits where n is 8 * control_field
    control_field, msg = read_bits(msg, 6)
    data, msg = read_bits(msg, int(control_field, 2) * 8)

    # CRC Field
    crc, msg = read_bits(msg, 15)
    crc_delimiter, msg = read_bits(msg, 1)

    # ACK Field
    ack_bit, msg = read_bits(msg, 1)
    ack_delimiter, msg = read_bits(msg, 1)

    # EOF
    end_of_frame, msg = read_bits(msg, 7)

    # IFS
    interframe_space, msg = read_bits(msg, 3)
    return msg
