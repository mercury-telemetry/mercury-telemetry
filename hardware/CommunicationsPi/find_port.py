#!/usr/bin/env python3
import sys
import argparse
import serial
import serial.tools.list_ports


def is_usb_serial(port, args):
    if port.vid is None:
        return False
    if not args.vid is None:
        if port.vid != args.vid:
            return False
    if not args.pid is None:
        if port.pid != args.pid:
            return False
    if not args.vendor is None:
        if not port.manufacturer.startswith(args.vendor):
            return False
    if not args.serial is None:
        if not port.serial_number.startswith(args.serial):
            return False
    if not args.intf is None:
        if port.interface is None or not args.intf in port.interface:
            return False
    return True


def extra_info(port):
    extra_items = []
    if port.manufacturer:
        extra_items.append("vendor '{}'".format(port.manufacturer))
    if port.serial_number:
        extra_items.append("serial '{}'".format(port.serial_number))
    if port.interface:
        extra_items.append("intf '{}'".format(port.interface))
    if extra_items:
        return " with " + " ".join(extra_items)
    return ""


def getPort():
    for port in serial.tools.list_ports.comports():
        if is_usb_serial(port, None):
            print(port)
            print(port.device)
            return
    return


def main():
    """The main program."""
    parser = argparse.ArgumentParser(
        prog="find-port.py",
        usage="%(prog)s [options] [command]",
        description="Find the /dev/tty port for a USB Serial devices",
    )
    parser.add_argument(
        "-l",
        "--list",
        dest="list",
        action="store_true",
        help="List USB Serial devices currently connected",
    )
    parser.add_argument(
        "-s",
        "--serial",
        dest="serial",
        help="Only show devices with the indicated serial number",
        default=None,
    )
    parser.add_argument(
        "-n",
        "--vendor",
        dest="vendor",
        help="Only show devices with the indicated vendor name",
        default=None,
    )
    parser.add_argument(
        "--pid",
        dest="pid",
        action="store",
        help="Only show device with indicated PID",
        default=None,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="Turn on verbose messages",
        default=False,
    )
    parser.add_argument(
        "--vid",
        dest="vid",
        action="store",
        help="Only show device with indicated VID",
        default=None,
    )
    parser.add_argument(
        "-i",
        "--intf",
        dest="intf",
        action="store",
        help="Shows devices which conatin the indicated interface string",
        default=None,
    )
    args = parser.parse_args(sys.argv[1:])

    if args.verbose:
        print("pyserial version = {}".format(serial.__version__))
        print("   vid =", args.vid)
        print("   pid =", args.pid)
        print("serial =", args.serial)
        print("vendor =", args.vendor)

    if args.list:
        detected = False
        for port in serial.tools.list_ports.comports():
            if is_usb_serial(port, args):
                print(
                    "USB Serial Device {:04x}:{:04x}{} found @{}\r".format(
                        port.vid, port.pid, extra_info(port), port.device
                    )
                )
                detected = True
        if not detected:
            print("No USB Serial devices detected.\r")
        return

    for port in serial.tools.list_ports.comports():
        if is_usb_serial(port, args):
            print(port)
            print(port.device)
            return
    sys.exit(1)


if __name__ == "__main__":
    main()
