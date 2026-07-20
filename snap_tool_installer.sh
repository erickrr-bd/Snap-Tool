#! /bin/bash

# Date: 07/07/2026
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
BASE_DIR=/opt/Snap-Tool
SNAP_TOOL_CONFIGURATION=/opt/Snap-Tool/configuration
SNAP_TOOL_LOGS=/var/log/Snap-Tool
SNAP_TOOL_KEY=/opt/Snap-Tool/configuration/key

# Print banner
echo -e "\e[1;33m--------------------------------------------------------------------------------\e[0m\n"
echo "
   _____                      _______          _ 
  / ____|                    |__   __|        | |
 | (___  _ __   __ _ _ __ ______| | ___   ___ | |
  \___ \| '_ \ / _\ | '_ \______| |/ _ \ / _ \| |
  ____) | | | | (_| | |_) |     | | (_) | (_) | |
 |_____/|_| |_|\__,_| .__/      |_|\___/ \___/|_|v3.4.1
                    | |                          
                    |_|                                                                   
"
echo -e "\e[1;33m--------------------------------------------------------------------------------\e[0m\n"
echo -e "[*] Author: Erick Roberto Rodriguez Rodriguez"
echo -e "[*] Email: erodriguez@tekium.mx, erickrr.tbd93@gmail.com"
echo -e "[*] GitHub: https://github.com/erickrr-bd/Snap-Tool"
echo -e "[*] Installer for Snap-Tool v3.4.1 - July 2026\n"

echo "Do you want to install or update Snap-Tool? (I/U)"
read opc

if [ $opc = "I" ] || [ $opc = "i" ]; then
	# "inv_alert" user and group creation.
	banner "Creating user and group"
	echo ''
	if grep -w ^snap_tool /etc/group > /dev/null; then
		echo -e "[*] \e[0;31m\"snamp_tool\" already exists\e[0m"
	else
		groupadd snap_tool
		echo -e "[*] \e[0;32m\"snap_tool\" group created\e[0m"
	fi
	if id snap_tool &> /dev/null; then
		echo -e "[*] \e[0;31m\"snap_tool\" already exists\e[0m\n"
	else
		useradd -M -s /bin/nologin -g snap_tool -d /opt/Snap-Tool snap_tool
		echo -e "[*] \e[0;32m\"snap_tool\" user created\e[0m\n"
	fi
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
	chown snap_tool:snap_tool -R $BASE_DIR
	find $BASE_DIR -type f -exec chmod 600 {} \;
	find $BASE_DIR -type d -exec chmod 700 {} \;
	chmod u+x /opt/Snap-Tool/Snap_Tool.py
	chown snap_tool:snap_tool -R $SNAP_TOOL_LOGS
	chmod 700 $SNAP_TOOL_LOGS
	echo -e "[*] \e[0;32mChanges made\e[0m\n"
	# Creating aliases.
	banner "Creating aliases for Snap-Tool"
	echo ''
	echo "alias Snap-Tool='/opt/Snap-Tool/Snap_Tool.py'" >> ~/.bashrc
	echo -e "[*] \e[0;32mCreated alias\e[0m\n"
elif [ $opc = "U" ] || [ $opc = "u" ]; then
	# "inv_alert" user and group creation.
	banner "Creating user and group"
	echo ''
	if grep -w ^snap_tool /etc/group > /dev/null; then
		echo -e "[*] \e[0;31m\"snamp_tool\" already exists\e[0m"
	else
		groupadd snap_tool
		echo -e "[*] \e[0;32m\"snap_tool\" group created\e[0m"
	fi
	if id snap_tool &> /dev/null; then
		echo -e "[*] \e[0;31m\"snap_tool\" already exists\e[0m\n"
	else
		useradd -M -s /bin/nologin -g snap_tool -d /opt/Snap-Tool snap_tool
		echo -e "[*] \e[0;32m\"snap_tool\" user created\e[0m\n"
	fi
	# Copy directories and files.
	banner "Updating Snap-Tool"
	echo ''
	cp -r Snap-Tool /opt
	echo -e "[*] \e[0;32mUpdate completed\e[0m\n"
	# Delete previous configuration.
	banner "Deletion of folders and files"
	echo ''
	rm -rf /etc/Snap-Tool
	echo -e "[*] \e[0;32mFolders and files deleted\e[0m\n"
	# Creation of folders and files.
	banner "Creation of folders and files"
	echo ''
	mkdir -p $SNAP_TOOL_CONFIGURATION
	encryption_key=$(cat /dev/urandom | head -n 30 | md5sum | head -c 30)
	cat << EOF > $SNAP_TOOL_KEY
$encryption_key
EOF
	echo -e "[*] \e[0;32mFolders and files created\e[0m\n"
	# Assignment of permits and owner.
	banner "Change of permissions and owner"
	echo ''
	chown snap_tool:snap_tool -R $BASE_DIR
	find $BASE_DIR -type f -exec chmod 600 {} \;
	find $BASE_DIR -type d -exec chmod 700 {} \;
	chmod u+x /opt/Snap-Tool/Snap_Tool.py
	echo -e "[*] \e[0;32mChanges made\e[0m\n"
else
	clear
	exit
fi 
