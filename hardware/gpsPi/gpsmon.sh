# run gpsmon
sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock
gpsmon /dev/serial0