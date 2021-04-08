#! /bin/bash

clear
echo -e "\e[96m@2021 Tekium. All rights reserved.\e[0m"
echo ''
echo -e '\e[96mInstaller for Snap-Tool v3.0\e[0m'
echo ''
echo -e '\e[96mAuthor: Erick Rodríguez erickrr.tbd93@gmail.com\e[0m'
echo ''
echo -e '\e[96mLicense: GPLv3\e[0m'
echo ''
echo -e '\e[1;33m--------------------------------------------------------------------------------\e[0m'
echo ''
echo 'Do you want to install or update Snap-Tool on the computer (I/U)?'
read opc
if [ $opc = "I" ] || [ $opc = "i" ]; then
	echo -e '\e[96mStarting the Snap-Tool installation...\e[0m'
	echo ''
	echo 'Do you want to install the packages and libraries necessary for the operation of Snap-Tool (Y/N)?'
	read opc_lib
	if [ $opc_lib = "Y" ] || [ $opc_lib = "y" ]; then
		echo ''
		echo -e '\e[96mStarting the installation of the required packages and libraries...\e[0m'
		yum install python3-pip -y
		dnf install dialog -y
		dnf install gcc -y
		dnf install python3-devel -y
		dnf install libcurl-devel -y
		dnf install openssl-devel -y
		pip3 install pythondialog 
		pip3 install pycryptodome
		pip3 install pyyaml 
		pip3 install pycurl 
		pip3 install elasticsearch-dsl 
		pip3 install requests 
		echo ''
		echo -e '\e[96mRequired installed libraries...\e[0m'
		sleep 3
		echo ''
	fi
	echo ''
	echo -e '\e[96mCopying and creating the required directories for Snap-Tool...\e[0m'
	echo ''
	dir=$(sudo pwd)
	cp -r Snap-Tool /etc/
	mkdir /etc/Snap-Tool/conf
	mkdir /var/log/Snap-Tool
	echo -e '\e[96mDirectories copied and created...\e[0m'
	sleep 3
	echo ''
	echo -e '\e[96mCreating passphrase...\e[0m'
	passphrase=$(cat /dev/random | tr -dc '[:alpha:]' | head -c 30; echo)
	cat << EOF > /etc/Snap-Tool/conf/key 
$passphrase
EOF
	echo ''
	echo -e '\e[96mPassphrase created...\e[0m'
	sleep 3
	echo ''
	chown root:root -R /etc/Snap-Tool
	chown root:root -R /var/log/Snap-Tool
	echo -e '\e[96mSnap-Tool installed on the computer...\e[0m'
	sleep 3	
	echo ''
	echo -e '\e[96mStarting Snap-Tool..\e[0m'
	sleep 5
	cd /etc/Snap-Tool
	python3 Snap_Tool.py
elif [ $opc = "U" ] || [ $opc = "u" ]; then
	echo ''
	echo -e '\e[96mStarting the Snap-Tool update...\e[0m'
	echo ''
	dir=$(sudo pwd)
	cp -r Snap-Tool /etc/
	chown root:root -R /etc/Snap-Tool
	sleep 3
	echo -e '\e[96mSnap-Tool updated...\e[0m'
	echo ''
	echo -e '\e[96mStarting Snap-Tool...\e[0m'
	sleep 5
	cd /etc/Snap-Tool
	python3 Snap_Tool.py
else
	clear
	exit
fi 