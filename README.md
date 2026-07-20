# 💾 Snap-Tool v3.4

Modular toolkit for managing Elasticsearch snapshots, repositories, and indexes via Python.

# ⚙️ Features
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

# 📝 Requirements
- ElasticSearch 7.x or 8.x
- Python 3.12 +
- Python Libraries
  - libPyDialog (https://github.com/erickrr-bd/libPyDialog)
  - libPyElk (https://github.com/erickrr-bd/libPyElk)
  - libPyTelegram (https://github.com/erickrr-bd/libPyTelegram)
  - libPyLog (https://github.com/erickrr-bd/libPyLog)
  - libPyUtils (https://github.com/erickrr-bd/libPyUtils)

# Installation
To install or update Snap-Tool, the installer must be executed, for this it must be executed as follows:

`snap_tool_installer.sh`

Note: You just have to follow the instructions that appear on the screen and choose the desired options.

# Execution
To run Snap-Tool, run the following command (creation of the alias is required):

`Snap-Tool`
