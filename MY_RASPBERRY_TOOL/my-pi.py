#!/usr/bin/python -tt
# ReachView code is placed under the GPL license.
# Written by Egor Fedorov (egor.fedorov@emlid.com)
# Copyright (c) 2015, Emlid Limited
# All rights reserved.

# If you are interested in using ReachView code as a part of a
# closed source project, please contact Emlid Limited (info@emlid.com).

# This file is part of ReachView.

# ReachView is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# ReachView is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with ReachView.  If not, see <http://www.gnu.org/licenses/>.

import time
import pexpect
import subprocess
import sys
import os
import syslog
import shutil
import re
import os.path
import commands
import getpass
import ast
import datetime


"""
Document to use this script
There are four options to use this script
################################################################################################################################################################
Option 1 :-
	This option just erase the SD card
	create boot & root partiton
	
################################################################################################################################################################
Option 2 :- 
	This option will earse SD card for copy the pi image to SD card
	will preapre the basic SD card for booting
	will update the networking SSID & password
################################################################################################################################################################
Option 3 :- 
	This option will ask user to 
	Let us upgrade the latest kernel
	if u press Yes
	For Kernel Update :- https://www.raspberrypi.org/documentation/linux/kernel/building.md
	It will clone the source of latest kernel & compile the source code
	Finally it will give you updated Zimage & well as latest kernel modules
	Once it is done user has to copy the zImage to boot folder of SD card &
	As well edit the config.txt file in boot folder add kernel=zImage
	module from ISNTALL_MOD_PATH in linux folder has to copy to SD card in root /lib/modules

################################################################################################################################################################
Option 4 :-  
	This option used to take the back up of SD card
	it will ask user where is the boot path as well as root path
	user has to provide the path
	then it will take the data backup from this path
	Create Release folder.
	Relase.csv will contain backup of release in CSV file
	as well as
	in  text file it will contain version
"""


#Make sure your SD card is formatted 

script_version = "version_0"
sd_card_path	= "sd_path.conf"
RPI_image_path = "rpi_image.conf"
New_Kimage_path = "kernel_image.conf"

SD_card_location = 0
Zimage_card_location = 0
Modules_location = 0

"""#############################################################################################"""
def Open_File(path):
	if os.path.isfile(path) and os.access(path, os.R_OK):
		print "\n ******* File exists and is readable  %s " % path
		f = open(path, 'r')
		#print f.read()
		f.close()
		return '1'
	else:
		print "Either file is missing or is not readable %s " % path
		sys.exit(0);
		return '0'

"""#############################################################################################"""
def Do_changes_SD_Card():
	print "Update changes in boot folder & RFS "	
	USER_ID = getpass.getuser()
	os.system("ls /media/%s" %USER_ID);

	if(Open_File(sd_card_path)):
		with open(sd_card_path) as f:
			SD_card_location= f.read().splitlines() 
			print ("SD_card_location is %s " % SD_card_location[0])
	else:
		sys.exit(0);
	
	boot_sd_path = raw_input("Enter Boot Path of SD card: ");
	ssh_location = boot_sd_path+"/ssh"
	print ssh_location;	
	print(("touch %s " % ssh_location));
	print(commands.getoutput("touch %s " % ssh_location));
	config_location = boot_sd_path + "/config.txt"
	f = open(config_location, 'a+')
	f.write('# Enable UART\n')  # python will convert \n to os.linesep
	f.write('enable_uart=1\n')						
	f.close()  
	root_sd_path = raw_input("Enter Root Path of SD card: ");
	network_location = root_sd_path + "/etc/wpa_supplicant/wpa_supplicant.conf"
	f = open(network_location, 'a+')
	f.write('network={ \n');
	f.write('     ssid="tspwifi" \n');
	f.write('    psk="tspjanuary" \n');
	f.write('}');
	print ("\nSD is ready ")
	
"""#############################################################################################"""
def Prepare_New_SD_Card():
	print "Ready to prepare new SD card"
	if(Open_File(sd_card_path)):
		with open(sd_card_path) as f:
			SD_card_location= f.read().splitlines() 
			print ("SD_card_location is %s " % SD_card_location[0])
	else:
		sys.exit(0);

	if(Open_File(RPI_image_path)):
		with open(RPI_image_path) as f:
			rpi_image_location= f.read().splitlines() 
			print ("SD_card_location is %s " % rpi_image_location[0])
	else:
		sys.exit(0);

	print("sudo dd if=%s of=%s bs=4M conv=fsync" % (rpi_image_location[0],SD_card_location[0]));
	print(commands.getoutput("sudo dd if=%s of=%s bs=4M conv=fsync" % (rpi_image_location[0],SD_card_location[0])));	
	print "SD card is flashed but under sync "
	os.system("sync");

	print(commands.getoutput("sudo umount %s ") % SD_card_location);
	print "--------------------------------------------------------"
	print "------------------                   -------------------"
	print "	       Please remove the SD Card & insert back	"
	print "------------------	            -------------------"
	print "--------------------------------------------------------"
	junk = raw_input("Press Enter to Continue ");

"""#############################################################################################"""
def Get_Sd_card_bkup():
	print "Bkup will start"
	
	if not os.path.exists("Release"):
		os.mkdir("Release")

	os.chdir("Release");
	boot_sd_path = raw_input("Enter boot path of SD card: ");
	root_sd_path = raw_input("Enter Root path of SD card: ");

	if not (os.path.isfile("Release.csv")):
		os.system("touch Release.csv");

	if not (os.path.isfile("Release.txt")):
		os.system("touch Release.txt");
		os.system("echo 0 >> Release.txt ")

	with open("Release.txt") as f:
		cur_version= f.read().splitlines() 

	print ("Current version %s \n" % cur_version[0])	
	Version = ast.literal_eval(cur_version[0])
	print "Version No %s" %Version
	print boot_sd_path
	print root_sd_path
	if os.path.exists(boot_sd_path):
		print "\n Boot Path is there"	
		if not os.path.exists(root_sd_path):
			print "\n Root Path is wrong"	
		else:	
			os.mkdir(cur_version[0]);
			os.chdir(cur_version[0]);
			Boot_version = cur_version[0]+'.'+'boot.tar'
			Root_version = cur_version[0]+'.'+'root.tar'
			now = datetime.datetime.now()
			Todays_Date = now.strftime("%Y-%m-%d_%H:%M:%S")
			Customer_Name = raw_input("Enter a Customer name: ")
			csv_update = Todays_Date+','+cur_version[0]+','+Boot_version+','+Root_version+','+Customer_Name
			print "Boot Version %s" % Boot_version
			print "Root Version %s" % Root_version
			print "CSV Version %s" % csv_update
			print(('su -c "tar -cvf %s %s"' % (Boot_version,boot_sd_path)));		
			print(('su -c "tar -cvf %s %s"' % (Root_version,root_sd_path)));
			print(commands.getoutput('su -c "tar -cvf %s %s"' % (Boot_version,boot_sd_path)));		
			print(commands.getoutput('su -c "tar -cvf %s %s"' % (Root_version,root_sd_path)));
			print(commands.getoutput("pwd"))
			print("Wait for SYNC ")
			os.system("sync");
			if (os.path.isfile(Boot_version)):
				if (os.path.isfile(Root_version)):
					os.chdir('..')
					print(commands.getoutput("pwd"))
					file = open("Release.csv",'a+') 
					file.write(csv_update) 
					file.close()
					Version = Version + 1;
					file = open("Release.txt",'w') 
					file.write(str(Version)) 
					file.close()
					print ("***************************************")
					print ("           Back up Completed successfully \n")
					print ("***************************************")					
				else:
					print ("***************************************")
					print ("           Back up Error \n")
					print ("***************************************")
	else:
		print "Path does not exist \n"
	print "Byeeeeee"

"""#############################################################################################"""
def Upgrade_New_Kernel():
	print "Kernel upgrade started "
	print "\nDo you want to clone the new kernel source code"
	current_path = commands.getoutput("pwd");
	print "*******************************\n"
	print current_path
	print "*******************************\n"
	Linux_code_location = current_path +'/'+ 'linux'
	Zimage_location = current_path +'/'+ 'linux/arch/arm/boot/zImage'
  	Modules_location = current_path +'/'+ 'linux/INSTALL_MOD_PATH/lib/modules'
	xString = raw_input("Enter a yes or no ")

	if(xString == "yes"):
		print "Ready to push the image to SD card"
		print(commands.getoutput("git clone --depth=1 https://github.com/raspberrypi/linux"));
		print(commands.getoutput("ls linux/"));
		os.chdir("linux");
		os.mkdir("INSTALL_MOD_PATH")
		os.system("KERNEL=kernel7");
		os.system("make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcm2709_defconfig");
		os.system("make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- zImage modules dtbs");
		os.system('su -c "make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- INSTALL_MOD_PATH=mnt/ext4 modules_install"');
		print ("Linux_code_location is %s " % Linux_code_location)
		print ("Zimage_card_location is %s " % Zimage_location)
		print ("Modules_location is %s " % Modules_location)
		print ("User has to copy the Linux Image to SD card in boot folder \n");
		print ("User has to copy the Linux module to SD card in root folder \n");
	else:
		if not os.path.exists("linux"):
			print ("Please clone the linux source code \n")
		else:
			print "Get the location of Kernel Image & Modules \n"
			print ("\nLinux_code_location is %s " % Linux_code_location)
			print ("Zimage_card_location is %s " % Zimage_location)
			print ("Modules_location is %s " % Modules_location)


	currentuser = os.getenv("SUDO_USER")
	print currentuser
	print("Please copy the Zimage & Modules to SD card \n")
	print("ls /media/%s" %(currentuser))
	print(commands.getoutput("ls /media/%s" %(currentuser)))
	print "Byeeeee \n"

if __name__ == "__main__":
	os.system('clear')
	Group_ID = os.getegid()
	USER_ID = getpass.getuser()

	print os.getenv("USER")
	print os.getenv("SUDO_USER")

	print "\nUser ID %s " % (Group_ID)
	print "User Name %s " % (USER_ID)

	user = os.getenv("SUDO_USER")
	if user is None:
		print "\n ********* This program need 'sudo' **********\n"
		exit()

	#print(commands.getoutput("ls"));
	print "Press 1 to Erase SD card"
	print "Press 2 to prepare the basic SD card"
	print "Press 3 to upgrade the SD card with latest Kernel Image"
	print "Press 4 to Bkup the SD card"

	xString = input("Enter a number: ")
	xnumber = int(xString)
	localtime = time.asctime( time.localtime(time.time()))
	print "Local current time :", localtime

	if (xnumber==1):
		print ("\nEnter the path of SD card \n")
		os.system("ls -la /dev/mmcblk*")
		boot_sd_path = raw_input("Enter path of SD card: ");	
		os.system("sudo sh sd_prepare.sh %s" %(boot_sd_path))

	elif (xnumber==2):
		os.system("ls -la /dev/mmcblk*")
		boot_sd_path = raw_input("Enter path of SD card: ");	
		os.system("sudo sh sd_raw.sh %s" %(boot_sd_path))
		print "\n\nUser has selected to prepare new SD card\n"
		Prepare_New_SD_Card();
		Do_changes_SD_Card();

	elif (xnumber == 3): 
		print "User has selected to upgrade the Linux Kernel SD card"
		Upgrade_New_Kernel();

	elif (xnumber == 4): 
		print "User has selected to take back up from SD card"
		Get_Sd_card_bkup();

	else:
		print "This script did not get any argument"
		sys.exit(0);



