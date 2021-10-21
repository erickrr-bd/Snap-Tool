# Snap-Tool v3.1

Author: Erick Rodríguez erickrr.tbd93@gmail.com

License: GPLv3

Snap-Tool is a tool developed in Python, which allows the management of tasks related to ElasticSearch snapshots, through a graphical interface.

# Applications
## Snap-Tool
Graphic application from where all the management in relation to the ElasticSearch snapshots is carried out. It has the ability to alert via Telegram.

Characteristics:
- The connection with ElasticSearch can be done through HTTPS and HTTP authentication (It must be configured in ElasticSearch).
- Allows you to create and modify the Snap-Tool connection settings.
- Encrypts sensitive data such as passwords so that they are not stored in plain text.
- Allows you to create a snapshot of a particular index. Snap-Tool will send an alert when the process begins and when it ends, in order not to have to be aware of the process. Once the snapshot has been created, it allows you to decide whether or not to delete the stored index. In case of deleting it, an alert will be sent with the notification that the index was deleted.
- Allows you to delete one or more snapshots created. An alert will be sent for each snapshot deleted.
- Allows you to mount a snapshot as a searchable snapshot (enterprise license required). An alert is sent when this action is performed on a snapshot.

# Requirements
- CentOS 8 (So far it has only been tested in this version)
- ElasticSearch 7.x 
- Enterprise license for Elastic Stack (searchable snapshots)
- Python 3.6
- Python Libraries
  - elasticsearch-dsl
  - requests
  - pycurl
  - pythondialog
  - pycryptodome
  - pyyaml

# Installation
To install or update Snap-Tool, you must run the installer_snap_tool.sh executable with administrator rights. The installer will perform the following actions:
- Copy and creation of directories and files necessary for the operation of Snap-Tool.
- Creation of passphrase for the encryption and decryption of sensitive information, which is generated randomly, so it is unique for each installed Snap-Tool installation.

# Commercial Support
![Tekium](https://github.com/unmanarc/uAuditAnalyzer2/blob/master/art/tekium_slogo.jpeg)

Tekium is a cybersecurity company specialized in red team and blue team activities based in Mexico, it has clients in the financial, telecom and retail sectors.

Tekium is an active sponsor of the project, and provides commercial support in the case you need it.

For integration with other platforms such as the Elastic stack, SIEMs, managed security providers in-house solutions, or for any other requests for extending current functionality that you wish to see included in future versions, please contact us: info at tekium.mx

For more information, go to: https://www.tekium.mx/
