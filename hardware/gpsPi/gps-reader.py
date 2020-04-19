import serial

GPS = serial.Serial('/dev/serial0', 9600)

while True:
    while GPS.inWaiting() == 0:
        pass

    NMEA = GPS.readline()
    print(NMEA)
