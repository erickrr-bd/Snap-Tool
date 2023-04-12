# Snap-Tool v3.3

Author: Erick Rodríguez 

Email: erickrr.tbd93@gmail.com, erodriguez@tekium.mx

License: GPLv3

Snap-Tool allows the management of ElasticSearch repositories, snapshots and indexes in an easy and graphical way.

# Applications
## Snap-Tool

Characteristics:
- Create, modify and display Snap-Tool settings.
- The connection to ElasticSearch can be via HTTPS or HTTP.
- When using HTTPS, you have the option to verify or not verify the SSL certificate.
- For the connection with ElasticSearch an authentication method can be used (HTTP Authentication or API key).
- Passphrase generation during the installation process, so it is different in each implementation.
- Encrypts sensitive data, such as passwords.
- Requests a password (defined during the configuration process) for privileged actions. For example, when an index is deleted.
- Create and delete repositories (FS type).
- Create and delete snapshots.
- Restore snapshots.
- Mount snapshots as searchable snapshots (enterprise license required).
- Delete indexes.
- Shows the percentage of disk used by each of the cluster nodes.
- Sending alerts via Telegram for each action taken.
- Generation of application logs.

# Requirements
- CentOS 8 or Rocky Linux 8
- ElasticSearch 7.x 
- Python 3.6
- Python Libraries
  - libPyDialog (https://github.com/erickrr-bd/libPyDialog)
  - libPyElk (https://github.com/erickrr-bd/libPyElk)
  - libPyTelegram (https://github.com/erickrr-bd/libPyTelegram)
  - libPyLog (https://github.com/erickrr-bd/libPyLog)
  - libPyUtils (https://github.com/erickrr-bd/libPyUtils)

# Installation
To install or update Snap-Tool, the installer must be executed, for this it must be executed as follows:

`./installer_snap_tool.sh`

Note: You just have to follow the instructions that appear on the screen and choose the desired options.

# Execution
To run Snap-Tool, run the following command (creation of the alias is required):

`Snap-Tool`

# Commercial Support
![Tekium](https://github.com/unmanarc/uAuditAnalyzer2/blob/master/art/tekium_slogo.jpeg)

Tekium is a cybersecurity company specialized in red team and blue team activities based in Mexico, it has clients in the financial, telecom and retail sectors.

Tekium is an active sponsor of the project, and provides commercial support in the case you need it.

For integration with other platforms such as the Elastic stack, SIEMs, managed security providers in-house solutions, or for any other requests for extending current functionality that you wish to see included in future versions, please contact us: info at tekium.mx

For more information, go to: https://www.tekium.mx/
