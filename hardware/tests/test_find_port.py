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
        port = dict.fromkeys(["vid"])
        args = {}

        response = is_usb_serial(port, args)
        self.assertFalse(response)

    def test_args_vid_not_empty(self):
        """
        checks to make sure that the is_serial_usb function
        exists correctly when the args["vid"] is not empty
        and port["vid"] doesn't equal args["vid"]
        """
        port = {"vid": "foo"}
        args = {"vid": "bar"}
        response = is_usb_serial(port, args)
        self.assertFalse(response)

    def test_args_pid_not_empty(self):
        """
        checks to make sure that the is_serial_usb function
        exists correctly when the args["pid"] is not empty
        and port["[id"] doesn't equal args["vid"]
        """
        port = {"vid": "bar", "pid": "foo"}
        args = {"vid": None, "pid": "bar"}
        response = is_usb_serial(port, args)
        self.assertFalse(response)

    def test_args_vendor_not_empty(self):
        """
        checks to make sure that the is_serial_usb function
        exists correctly when the args["vendor"] is not empty
        and port["manufacturer"] doesn't start with args["vendor"]
        """
        port = {"vid": "bar", "pid": "foo", "manufacturer": "Apple"}
        args = {"vid": None, "pid": None, "vendor": "Microsoft"}
        response = is_usb_serial(port, args)
        self.assertFalse(response)

    def test_args_serial_not_empty(self):
        """
        checks to make sure that the is_serial_usb function
        exists correctly when the args["serial"] is not empty
        and port["serial_number"] doesn't start with args["serial"]
        """
        port = {
            "vid": "bar",
            "pid": "foo",
            "manufacturer": "Apple",
            "serial_number": "456",
        }
        args = {"vid": None, "pid": None, "vendor": None, "serial": "123"}
        response = is_usb_serial(port, args)
        self.assertFalse(response)

    def test_args_intf_not_empty(self):
        """
        checks to make sure that the is_serial_usb function
        exists correctly when the args["serial"] is not empty
        and port["interface"] is none
        """
        port = {
            "vid": "bar",
            "pid": "foo",
            "manufacturer": "Apple",
            "serial_number": "456",
            "interface": None,
        }
        args = {"vid": None, "pid": None, "vendor": None, "serial": None, "intf": "foo"}
        response = is_usb_serial(port, args)
        self.assertFalse(response)

    def test_args_intf_not_empty_interface_not_empty(self):
        """
        checks to make sure that the is_serial_usb function
        exists correctly when the args["serial"] is not empty
        and port["interface"] is different than args["serial"]
        """
        port = {
            "vid": "bar",
            "pid": "foo",
            "manufacturer": "Apple",
            "serial_number": "456",
            "interface": "bar",
        }
        args = {"vid": None, "pid": None, "vendor": None, "serial": None, "intf": "foo"}
        response = is_usb_serial(port, args)
        self.assertFalse(response)

    def test_pass(self):
        """
        insure that is_serial_usb returns true if all test cases haven't
        failed
        """
        port = {
            "vid": "bar",
            "pid": "foo",
            "manufacturer": "Apple",
            "serial_number": "456",
            "interface": "bar",
        }
        args = {"vid": None, "pid": None, "vendor": None, "serial": None, "intf": None}
        response = is_usb_serial(port, args)
        self.assertTrue(response)
