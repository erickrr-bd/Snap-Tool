# Snap-Tool v3.3

Author: Erick Rodríguez 

Email: erickrr.tbd93@gmail.com, erodriguez@tekium.mx

License: GPLv3

Snap-Tool allows the management of ElasticSearch repositories, snapshots and indexes in an easy and graphical way.

# Applications
## Snap-Tool
Graphic application that allows the management of ElasticSearch repositories, snapshots and indexes.

Characteristics:
- Allows you to create and modify the Snap-Tool connection settings.
- The connection with ElasticSearch can be done through HTTPS and HTTP authentication (It must be configured in ElasticSearch).
- Encrypts sensitive data such as passwords so that they are not stored in plain text.
- Allows you to create a repository to store snapshots (type FS).
- Allows you to delete one or more repositories (type FS).
- Allows you to create a snapshot of a specific index.
- Allows you to delete one or more snapshots.
- Allows you to restore a snapshot.
- Allows you to mount a snapshot as a searchable snapshot (enterprise license required).
- Allows you to delete one or more indexes.
- It shows the percentage of disk space occupied by each of the nodes that make up the ElasticSearch cluster.
- It does not allow operations on the indexes of the system, for security reasons.
- Sending alerts to a Telegram channel of the operations carried out in the application.

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

# Execution
The /etc/Snap-Tool path is accessed and the Snap_Tool.py binary is executed as follows:

- python3 Snap_Tool.py or ./Snap_Tool.py

# Commercial Support
![Tekium](https://github.com/unmanarc/uAuditAnalyzer2/blob/master/art/tekium_slogo.jpeg)

Tekium is a cybersecurity company specialized in red team and blue team activities based in Mexico, it has clients in the financial, telecom and retail sectors.

Tekium is an active sponsor of the project, and provides commercial support in the case you need it.

For integration with other platforms such as the Elastic stack, SIEMs, managed security providers in-house solutions, or for any other requests for extending current functionality that you wish to see included in future versions, please contact us: info at tekium.mx

For more information, go to: https://www.tekium.mx/
