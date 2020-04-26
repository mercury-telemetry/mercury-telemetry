from hardware.gpsPi.gps_reader import GPSReader

gpsreader = GPSReader()
while True:
    gpsreader.get_geolocation()
