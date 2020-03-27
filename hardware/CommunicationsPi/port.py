# Test code written by Xiaofeng Xu to read serial messages from port

import asyncio
import glob
import sys
import json
import serial
import serial_asyncio


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

        self.transport.close()

    def connection_lost(self, exc):
        print("port closed")
        asyncio.get_event_loop().stop()


ser = serial.Serial()
ports = glob.glob("/dev/tty.u*")
print(ports[0])
ser.port = ports[0]
ser.timeout = 1
ser.open()

loop = asyncio.new_event_loop()
coro = serial_asyncio.create_serial_connection(loop, AsyncSerialProtocol, ports[0])
try:
    loop.run_until_complete(coro)
    loop.run_forever()
except KeyboardInterrupt:
    sys.stdout.write("\n")
finally:
    loop.close()
