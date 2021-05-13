# Snap-Tool v3.0

Author: Erick Rodríguez erickrr.tbd93@gmail.com

License: GPLv3

Snap-Tool is an application developed in Python, which uses a graphical interface, which allows the user to make a connection with ElasticSearch and to create and delete Snapshots, as well as to mount a snapshot as a searchable snapshot.

# Applications
## Snap-Tool
Application that allows you to create a snapshot of an index in ElasticSearch, delete the index when the creation process has finished, delete one or more snapshots and mount a snapshot as a searchable snapshot.

Characteristics:
- The connection with ElasticSearch can be done through HTTPS and HTTP authentication (It must be configured in ElasticSearch).
- Sending messages to a Telegram channel, where it is notified when the process starts and the creation of the snapshot ends, when an index is deleted, when one or more snapshots are deleted, when a searchable snapshot is mounted.

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
Run the executable installer_snap_tool.sh, which is in charge of installing the packages and libraries necessary for the operation of Snap-Tool (these can also be installed manually). It is also responsible for copying and creating the necessary files and directories. Run with a user with administrator permissions.

# Commercial Support
![Tekium](https://github.com/unmanarc/uAuditAnalyzer2/blob/master/art/tekium_slogo.jpeg)

Tekium is a cybersecurity company specialized in red team and blue team activities based in Mexico, it has clients in the financial, telecom and retail sectors.

Tekium is an active sponsor of the project, and provides commercial support in the case you need it.

For integration with other platforms such as the Elastic stack, SIEMs, managed security providers in-house solutions, or for any other requests for extending current functionality that you wish to see included in future versions, please contact us: info at tekium.mx

For more information, go to: https://www.tekium.mx/
