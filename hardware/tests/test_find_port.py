from django.test import TestCase

from ..CommunicationsPi.find_port import is_usb_serial

class IsUsbSerialTests(TestCase):
    """
    Tests for the is_usb_serial function
    """

    def test_port_vid_empty(self):
        """
        insures that the is_serial_usb function retunrs false
        if the port.vid param is empty
        """
        port = dict.fromkeys(["vid",])
        args = {}

        print(port)

        response = is_usb_serial(port, args)
        self.assertFalse(response)