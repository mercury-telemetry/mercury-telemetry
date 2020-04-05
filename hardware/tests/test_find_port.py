from django.test import SimpleTestCase

from unittest import mock
from serial.tools.list_ports_common import ListPortInfo
from argparse import Namespace

from ..CommunicationsPi.find_port import is_usb_serial, extra_info, get_port


class IsUsbSerialTests(SimpleTestCase):
    """
    Tests for the is_usb_serial function
    """

    def test_port_vid_empty(self):
        """
        insures that the is_serial_usb function retunrs false
        if the port.vid param is empty
        """
        port = ListPortInfo()
        port.vid = None
        args = Namespace()
        args.vid = None

        response = is_usb_serial(port, args)
        self.assertFalse(response)

    def test_args_vid_not_empty(self):
        """
        checks to make sure that the is_serial_usb function
        exists correctly when the args["vid"] is not empty
        and port["vid"] doesn't equal args["vid"]
        """
        port = ListPortInfo()
        port.vid = "foo"
        args = Namespace()
        args.vid = "bar"
        response = is_usb_serial(port, args)
        self.assertFalse(response)

    def test_args_pid_not_empty(self):
        """
        checks to make sure that the is_serial_usb function
        exists correctly when the args["pid"] is not empty
        and port["[id"] doesn't equal args["vid"]
        """
        port = ListPortInfo()
        args = Namespace()
        port.vid = "bar"
        port.pid = "foo"

        args.vid = None
        args.pid = "bar"

        response = is_usb_serial(port, args)
        self.assertFalse(response)

    def test_args_vendor_not_empty(self):
        """
        checks to make sure that the is_serial_usb function
        exists correctly when the args["vendor"] is not empty
        and port["manufacturer"] doesn't start with args["vendor"]
        """
        port, args = ListPortInfo(), Namespace()
        port.vid = "bar"
        port.pid = "foo"
        port.manufacturer = "Apple"

        args.vid = None
        args.pid = None
        args.vendor = "Microsoft"

        response = is_usb_serial(port, args)
        self.assertFalse(response)

    def test_args_serial_not_empty(self):
        """
        checks to make sure that the is_serial_usb function
        exists correctly when the args["serial"] is not empty
        and port["serial_number"] doesn't start with args["serial"]
        """
        port, args = ListPortInfo(), Namespace()

        port.vid = "bar"
        port.pid = "foo"
        port.manufacturer = "Apple"
        port.serial_number = "456"

        args.vid = None
        args.pid = None
        args.vendor = None
        args.serial = "123"

        response = is_usb_serial(port, args)
        self.assertFalse(response)

    def test_args_intf_not_empty(self):
        """
        checks to make sure that the is_serial_usb function
        exists correctly when the args["serial"] is not empty
        and port["interface"] is none
        """
        port, args = ListPortInfo(), Namespace()

        port.vid = "bar"
        port.pid = "foo"
        port.manufacturer = "Apple"
        port.serial_number = "456"
        port.interface = None

        args.vid = None
        args.pid = None
        args.vendor = None
        args.serial = None
        args.intf = "foo"

        response = is_usb_serial(port, args)
        self.assertFalse(response)

    def test_args_intf_not_empty_interface_not_empty(self):
        """
        checks to make sure that the is_serial_usb function
        exists correctly when the args["serial"] is not empty
        and port["interface"] is different than args["serial"]
        """
        port, args = ListPortInfo(), Namespace()

        port.vid = "bar"
        port.pid = "foo"
        port.manufacturer = "Apple"
        port.serial_number = "456"
        port.interface = "bar"

        args.vid = None
        args.pid = None
        args.vendor = None
        args.serial = None
        args.intf = "foo"

        response = is_usb_serial(port, args)
        self.assertFalse(response)

    def test_pass(self):
        """
        insure that is_serial_usb returns true if all test cases haven't
        failed
        """
        port, args = ListPortInfo(), Namespace()

        port.vid = "bar"
        port.pid = "foo"
        port.manufacturer = "Apple"
        port.serial_number = "456"
        port.interface = "bar"

        args.vid = None
        args.pid = None
        args.vendor = None
        args.serial = None
        args.intf = None

        response = is_usb_serial(port, args)
        self.assertTrue(response)


class ExtraInfoTests(SimpleTestCase):
    def test_manufacturer(self):
        """
        insure that the manufacturer is added to the
        extra_items list if it is present in port
        """
        port = {"manufacturer": "Microsoft"}
        response = extra_info(port)
        self.assertTrue(port["manufacturer"] in response)

    def test_no_matches(self):
        """
        insure that extra_info returns the empty string if
        none of the keys match
        """
        port = {"foo": "bar"}
        self.assertTrue(extra_info(port) == "")

    def test_serial_number(self):
        """
        insure that the serial_number is added to the
        extra_items list if it is present in port
        """
        port = {"serial_number": "123"}
        response = extra_info(port)
        self.assertTrue(port["serial_number"] in response)

    def test_interface(self):
        """
        insure that the interface is added to the
        extra_items list if it is present in port
        """
        port = {"interface": "123interface"}
        response = extra_info(port)
        self.assertTrue(port["interface"] in response)


class GetPortTests(SimpleTestCase):
    @mock.patch("serial.tools.list_ports.comports")
    def test_get_port_match(self, port_mocks):

        port_mocks.return_value = [
            {
                "vid": "vid",
                "pid": None,
                "manufacturer": None,
                "serial_number": None,
                "interface": None,
                "device": "usb",
            }
        ]
        self.assertTrue("port found" in get_port())

    @mock.patch("serial.tools.list_ports.comports")
    def test_get_port_empty(self, port_mocks):

        port_mocks.return_value = [
            {
                "vid": None,
                "pid": None,
                "manufacturer": None,
                "serial_number": None,
                "interface": None,
                "device": "usb",
            }
        ]
        self.assertIsNone(get_port())
