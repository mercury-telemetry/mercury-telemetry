# Test code written by Xiaofeng Xu to read serial messages from port

import asyncio
import glob
import sys
import json

import serial
import serial_asyncio
from django.utils import dateparse


class AsyncSerialProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print("port opened", transport)
        transport.serial.rts = False
        transport.write(b"hello world\n")

    def data_received(self, data):
        m = data.decode("utf-8")
        print(m)
        # print("data received", repr(data))
        try:
            message = json.loads(data.decode("utf-8"))
            print(message)
        except json.JSONDecodeError:
            print()
        
        # print(repr(data))
        # json_to_models(repr(data))
        # if len(repr(data).split(";")) > 2:
        self.transport.close()

        
    def connection_lost(self, exc):
        print("port closed")
        asyncio.get_event_loop().stop()


def json_to_models(json_str, event_id):
        """
        Json example:
        {
        sensors:{
            ss_id : “Sensor id”,
            ss_value : {
                /*as many values as you wish*/
                value_a_name : “value_a”,
                value_b_name : “value_b”,
                value_c_name : “value_c”
            }
            date : “2014-03-12T13:37:27+00:00” /*ISO 8601 dates*/
        };
        """
        res = []
        sensors = json_str["sensors"]
        ss_id = int(sensors["ss_id"])
        ss_value = sensors["ss_value"]
        date = dateparse.parse_datetime(sensors["date"])


ser = serial.Serial()
ports = glob.glob("/dev/tty.u*")
print(ports[0])
ser.port = ports[0]
ser.timeout = 1
ser.open()
# print(ser.port)
# print(ser.baudrate)
# print(ser.parity)
# print(ser.stopbits)
# print(ser.bytesize)
# print(ser.timeout)
# while 1:
#     x = ser.readline()
#     if x is not "":
#         print(x)

loop = asyncio.new_event_loop()
coro = serial_asyncio.create_serial_connection(
    loop, AsyncSerialProtocol, ports[0]
)
try:
    loop.run_until_complete(coro)
    loop.run_forever()
except KeyboardInterrupt:
    sys.stdout.write('\n')
finally:
    loop.close()