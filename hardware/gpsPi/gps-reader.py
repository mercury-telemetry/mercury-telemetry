import serial

# want GPRMC and GPGGA
# GPRMC universal coordinated time 


gps = serial.Serial('/dev/serial0', 9600)

while True:
    while gps.inWaiting() == 0:
        pass

    nmeaSentence = gps.readline().split(",")
    print(nmeaSentence)
