#!/bin/bash
##################################################################################3
# Erata
# 	$(AM_V_CCLD)$(LINK) $(client_bluetoothctl_OBJECTS) $(client_bluetoothctl_LDADD) $(LIBS) -lpthread  
#	in make file 
# 	if you r getting compilation issue then add the -lpthread in this line 
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#nmap -sn 192.168.1.0/24
# 

clear

echo "Enter 1 to install NPM"
echo "Enter 2 to make Custom folder"
echo "Enter 3 to Stop Custom BLE service"
echo "Enter 4 to start BLE on PI board"
echo "Enter 5 to "

read user_opt
echo "$user_opt"

if  [ "$user_opt" -eq 1 ]; then
	clear
	echo "You have selected option $user_opt"
	echo "sudo apt-get remove nodered -y"
	sudo apt-get remove nodered -y
	echo "------------------------------------"
	echo "------------------------------------"
	echo "Press Enter"
	read Enter

	sudo apt-get remove nodejs nodejs-legacy -y
	echo "------------------------------------"
	echo "------------------------------------"
	echo "Press Enter"
	read Enter


	sudo apt-get remove npm  -y # if you installed npm
	echo "------------------------------------"
	echo "------------------------------------"
	echo "Press Enter"
	read Enter

	sudo curl -sL https://deb.nodesource.com/setup_5.x | sudo bash -
	echo "------------------------------------"
	echo "------------------------------------"
	echo "Press Enter"
	read Enter

	sudo apt-get install nodejs -y
	echo "------------------------------------"
	echo "------------------------------------"
	echo "Press Enter"
	read Enter

	node -v
	npm -v	
elif [ "$user_opt" -eq 2 ]; then
	clear
	echo "You have selected option $user_opt"
	cd ~
	mkdir ble
	cd ble
	mkdir tsp
	cd ~	
elif [ "$user_opt" -eq 3 ]; then
	clear
	echo "You have selected option $user_opt"
	sudo systemctl stop bluetooth.service
	sudo systemctl disable bluetooth.service
	
elif [ "$user_opt" -eq 4 ]; then
	clear
	echo "You have selected option $user_opt"
	
	sudo chmod -R 777 ~/ble/tsp/TSP-bluez-5.44

	#pi@raspberrypi:~/ble/tsp/TSP-bluez-5.44 $ sudo apt-get install python-pip
	sudo apt-get install python-pip
	
	#pi@raspberrypi:~/ble/tsp/TSP-bluez-5.44 $ sudo pip install pexpect
	sudo pip install pexpect
	
	#pi@raspberrypi:~/ble/tsp/TSP-bluez-5.44 $ sudo apt-get install rfkill
	sudo apt-get install rfkill
	
	#pi@raspberrypi:~/ble/tsp/TSP-bluez-5.44 $ sudo pip install ibmiotf
	sudo pip install ibmiotf
	
	#pi@raspberrypi:~/ble/tsp/TSP-bluez-5.44 $ sudo apt-get install glib2.0
	sudo apt-get install glib2.0
	
	#pi@raspberrypi:~/ble/tsp/TSP-bluez-5.44 $ sudo apt-get install -y libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
	sudo apt-get install -y libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev
	
	#pi@raspberrypi:~/ble/tsp/TSP-bluez-5.44 $ sudo apt-get install libbluetooth-dev
	sudo apt-get install libbluetooth-dev
elif [ "$user_opt" -eq 5 ]; then
	clear
	echo "You have selected option $user_opt"
	
	cd ~/ble/tsp/TSP-bluez-5.44/
	
	#pi@raspberrypi:~/ble/tsp/TSP-bluez-5.44 $ sudo sudo python start.py 
	sudo sudo python start.py
	
	#pi@raspberrypi:~/ble/tsp/TSP-bluez-5.44 $ sudo python trigger_ble.py /home/pi/ble/tsp/TSP-bluez-5.44/div/Python/1/
	sudo python trigger_ble.py /home/pi/ble/tsp/TSP-bluez-5.44/div/Python/1/


elif [ "$user_opt" -eq 6 ]; then
	clear
	echo "You have selected option $user_opt"	
	cd ~/ble/tsp/TSP-bluez-5.44/NODE_JS
	rm -rf node_modules/
	sudo npm install noble sleep util child_process mqtt
	sudo npm install moment
	sudo npm install line-reader
	sudo npm install n-readlines
	sudo npm install string-search
	
else
	echo "No correct option selected "
fi
