# get gpsd
sudo apt-get update
sudo apt-get install gpsd gpsd-clients python-gps

# disable the gpsd systemd service
sudo systemctl stop gpsd.socket
sudo systemctl disable gpsd.socket

# enable the gpsd systemd service
# sudo systemctl enable gpsd.socket
# sudo systemctl start gpsd.socket