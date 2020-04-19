import serial

# want GPRMC and GPGGA
# GPRMC universal coordinated time 


gps = serial.Serial('/dev/serial0', 9600)

while True:
    while gps.inWaiting() == 0:
        pass

    nmeaSentence = gps.readline().split(",")
    nmeaType = nmeaSentence[0]

    if nmeaType == "$GPRMC":
        latitude_hours = float(nmeaSentence[3].split(".")[0])
        latitude_minutes = float(nmeaSentence[3].split(".")[1])
        longitude_hours = float(nmeaSentence[5].split(".")[0])
        longitude_minutes = float(nmeaSentence[5].split(".")[1])

        latitude_decimal = latitude_hours + latitude_minutes / 60
        longitude_decimal = longitude_hours + longitude_minutes / 60

        latitude_dir = nmeaSentence[4]
        longitude_dir = nmeaSentence[6]

        if latitude_dir == "S":
            latitude_decimal = latitude_decimal * -1
        if longitude_dir == "W":
            longitude_decimal = longitude_decimal * -1
        
        print(latitude_decimal)
        print(longitude_decimal)
        print("")


    # print(nmeaSentence)
