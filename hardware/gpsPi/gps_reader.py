import os
import serial
from ..Utils.utils import get_logger


class GPSReader:
    def __init__(self, log_file_name=None):
        self.gps = serial.Serial(os.environ["GPS_PORT"], os.environ["GPS_BAUDRATE"])

        if log_file_name is None:
            self.logging = get_logger("GPS_LOG_FILE")
        else:
            self.logging = get_logger(log_file_name, log_file_name)

    def get_geolocation(self):
        while self.gps.inWaiting() == 0:
            pass

        nmeaSentence = self.gps.readline().split(",")
        nmeaType = nmeaSentence[0]

        # Added additional check to verify if nmeaSentence has valid data
        if nmeaType == "$GPRMC" and nmeaSentence[2] == "A":
            latitude_hours = float(nmeaSentence[3][0:2])
            latitude_minutes = float(nmeaSentence[3][2:])
            longitude_hours = float(nmeaSentence[5][0:3])
            longitude_minutes = float(nmeaSentence[5][3:])

            latitude_decimal = latitude_hours + latitude_minutes / 60
            longitude_decimal = longitude_hours + longitude_minutes / 60

            latitude_dir = nmeaSentence[4]
            longitude_dir = nmeaSentence[6]

            if latitude_dir == "S":
                latitude_decimal = latitude_decimal * -1
            if longitude_dir == "W":
                longitude_decimal = longitude_decimal * -1

            self.logging.info("latitude_decimal: " + latitude_decimal)
            self.logging.info("longitude_decimal: " + longitude_decimal)

            # print(latitude_decimal)
            # print(longitude_decimal)
            # print("")
