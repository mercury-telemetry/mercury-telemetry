#!/bin/bash

function showStatus() {
	printf "\n${1}\n"
}

showStatus 'Running Raspberry Pi Common Setup'

cd ~/Downloads

showStatus 'Updating system...'
sudo apt-get update -y && sudo apt-get upgrade -y && sudo apt-get autoremove -y

showStatus 'Enabling VNC'
sudo raspi-config nonint do_vnc 0

showStatus 'Enabling SSH'
sudo raspi-config nonint do_ssh 0

showStatus 'Setting screen resolution for remote access'
sudo raspi-config nonint do_resolution 2 16

showStatus 'Installing essentials'

showStatus 'Installing vim'
sudo apt-get install vim -y

showStatus 'Installing curl and wget'
sudo apt-get install curl wget -y

showStatus 'Installing htop'
sudo apt-get install git htop -y

showStatus 'Installing screen'
sudo apt-get install screen -y

showStatus 'Installing nmap'
sudo apt-get install nmap -y

showStatus 'Installing AnyDesk'
wget https://download.anydesk.com/rpi/anydesk_5.5.4-1_armhf.deb
sudo dpkg -i anydesk*.deb
sudo apt-get install -f
sudo systemctl daemon-reload

showStatus 'Completed Raspberry Pi Common Setup'
cd ~/
