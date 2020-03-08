function showStatus() {
	printf "\n${1}\n"
}

showStatus 'Running Raspberry Pi Common Setup'

showStatus 'Enabling VNC'
sudo raspi-config nonint do_vnc 0

showStatus 'Enabling SSH'
sudo raspi-config nonint do_ssh 0

showStatus 'Completed Raspberry Pi Common Setup'
