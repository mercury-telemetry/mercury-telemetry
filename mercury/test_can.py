from django.test import TestCase
from .can import CANDecoder


class TestCANDecoder(TestCase):
    def test_can_decoder(self):
        decoded_message = CANDecoder.to_json("foo")
        self.assertEqual(decoded_message, True)


