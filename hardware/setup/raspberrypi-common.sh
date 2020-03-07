function showStatus() {
	printf "\n${1}\n"
}

showStatus 'Running Raspberry Pi Common Setup'

showStatus 'Updating system...'
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get autoremove -y

showStatus 'Enabling VNC'
sudo raspi-config nonint do_vnc 0

showStatus 'Enabling SSH'
sudo raspi-config nonint do_ssh 0

showStatus 'Installing AnyDesk'
wget https://download.anydesk.com/rpi/anydesk_5.5.4-1_armhf.deb
sudo dpkg -i anydesk*.deb
sudo apt-get install -f
sudo systemctl daemon-reload

showStatus 'Completed Raspberry Pi Common Setup'
