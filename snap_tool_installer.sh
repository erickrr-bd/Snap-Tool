#! /bin/bash

# Date: 10/11/2025
# Author: Erick Roberto Rodriguez Rodriguez
# Installation script. 

# Usage: $ ./snap_tool_installer.sh

clear

# Function that prints a banner.
banner()
{
	echo "+------------------------------------------+"
  	printf "| %-40s |\n" "`date`"
  	echo "|                                          |"
  	printf "|`tput bold` %-40s `tput sgr0`|\n" "$@"
  	echo "+------------------------------------------+"
}

# Application folders and files.
BASE_DIR=/etc/Snap-Tool
SNAP_TOOL_CONFIGURATION=/etc/Snap-Tool/configuration
SNAP_TOOL_LOGS=/var/log/Snap-Tool
SNAP_TOOL_KEY=/etc/Snap-Tool/configuration/key

# Print banner
echo -e "\e[1;33m--------------------------------------------------------------------------------\e[0m\n"
echo "
   _____                      _______          _ 
  / ____|                    |__   __|        | |
 | (___  _ __   __ _ _ __ ______| | ___   ___ | |
  \___ \| '_ \ / _\ | '_ \______| |/ _ \ / _ \| |
  ____) | | | | (_| | |_) |     | | (_) | (_) | |
 |_____/|_| |_|\__,_| .__/      |_|\___/ \___/|_|v3.4 
                    | |                          
                    |_|                                                                   
"
echo -e "\e[1;33m--------------------------------------------------------------------------------\e[0m\n"
echo -e "[*] Author: Erick Roberto Rodriguez Rodriguez"
echo -e "[*] Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com"
echo -e "[*] GitHub: https://github.com/erickrr-bd/Snap-Tool"
echo -e "[*] Installer for Snap-Tool v3.4 - November 2025\n"

echo "Do you want to install or update Snap-Tool? (I/U)"
read opc

if [ $opc = "I" ] || [ $opc = "i" ]; then
	# Copy directories and files.
	banner "Installing Snap-Tool"
	echo ''
	cp -r Snap-Tool /opt
	echo -e "[*] \e[0;32mInstallation completed\e[0m\n"
	# Creation of folders and files.
	banner "Creation of folders and files"
	echo ''
	mkdir -p $SNAP_TOOL_CONFIGURATION
	mkdir -p $SNAP_TOOL_LOGS
	encryption_key=$(cat /dev/urandom | head -n 30 | md5sum | head -c 30)
	cat << EOF > $SNAP_TOOL_KEY
$encryption_key
EOF
	echo -e "[*] \e[0;32mFolders and files created\e[0m\n"
	# Assignment of permits and owner.
	banner "Change of permissions and owner"
	echo ''
	find $BASE_DIR -type f -exec chmod 640 {} \;
	find $BASE_DIR -type d -exec chmod 750 {} \;
	find /opt/Snap-Tool -type f -exec chmod 640 {} \;
	find /opt/Snap-Tool -type d -exec chmod 750 {} \;
	chmod +x /opt/Snap-Tool/Snap_Tool.py
	chmod 750 $SNAP_TOOL_LOGS
	echo -e "[*] \e[0;32mChanges made\e[0m\n"
	# Creating aliases.
	banner "Creating aliases for Snap-Tool"
	echo ''
	echo "alias Snap-Tool='/opt/Snap-Tool/Snap_Tool.py'" >> ~/.bashrc
	echo -e "[*] \e[0;32mCreated alias\e[0m\n"
elif [ $opc = "U" ] || [ $opc = "u" ]; then
	# Copy directories and files.
	banner "Updating Snap-Tool"
	echo ''
	cp -r Snap-Tool /opt
	echo -e "[*] \e[0;32mUpdate completed\e[0m\n"
	# Assignment of permits and owner.
	banner "Change of permissions and owner"
	echo ''
	find /opt/Snap-Tool -type f -exec chmod 640 {} \;
	find /opt/Snap-Tool -type d -exec chmod 750 {} \;
	chmod +x /opt/Snap-Tool/Snap_Tool.py
	echo -e "[*] \e[0;32mChanges made\e[0m\n"
else
	clear
	exit
fi 