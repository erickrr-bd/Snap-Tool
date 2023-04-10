"""
Class that manages all the constant variables of the application.
"""
class Constants:
	"""
	Title that is shown in the background of the application.
	"""
	BACKTITLE = "SNAP-TOOL v3.3 by Erick Rodriguez"

	"""
	Absolute path of the Snap-Tool configuration file.
	"""
	PATH_SNAP_TOOL_CONFIGURATION_FILE = "/etc/Snap-Tool/configuration/snap_tool_conf.yaml"

	"""
	Absolute path of the file where the key for the encryption/decryption process is stored.
	"""
	PATH_KEY_FILE = "/etc/Snap-Tool/configuration/key"

	"""
	Absolute path of the application logs.
	"""
	NAME_FILE_LOG = "/var/log/Snap-Tool/snap-tool-log-"

	"""
	Name of the user created for the operation of the application.
	"""
	USER = "snap_tool"

	"""
	Name of the group created for the operation of the application.
	"""
	GROUP = "snap_tool"

	"""
	Options displayed in the main menu.
	"""
	OPTIONS_MAIN_MENU = [("1", "Configuration"),
					     ("2", "Repositories"),
					     ("3", "Snapshots"),
					     ("4", "Indices"),
					     ("5", "Nodes information"),
					     ("6", "About"),
					     ("7", "Exit")]

	"""
	Options that are shown when the configuration file does not exist.
	"""
	OPTIONS_CONFIGURATION_FALSE = [("Create", "Create the configuration file", 0)]

	"""
	Options that are shown when the configuration file exists.
	"""
	OPTIONS_CONFIGURATION_TRUE = [("Update", "Update the configuration file", 0),
								  ("Display", "Display the configuration data", 0)]

	"""
	Options that are shown when the configuration file exists.
	"""
	OPTIONS_AUTHENTICATION_METHOD = [("HTTP Authentication", "Use HTTP Authentication", 0),
								     ("API Key", "Use API Key", 0)]

	"""
	Options displayed to update a value established in the Snap-Tool configuration.
	"""
	OPTIONS_CONFIGURATION_SNAP_TOOL_UPDATE = [("Host", "ElasticSearch Host", 0),
							 	 			  ("Port", "ElasticSearch Port", 0),
							 	 			  ("SSL/TLS", "Enable or disable SSL/TLS connection", 0),
							 	 			  ("Authentication", "Enable or disable authentication method", 0),
							 	 			  ("Delete Index", "Enable or disable delete index", 0),
							 	 			  ("Password", "Password for privileged actions", 0),
							 	 			  ("Bot Token", "Telegram Bot Token", 0),
							 	 			  ("Chat ID", "Telegram channel identifier", 0)]

	"""
	Options displayed when "ElasticSearch hosts" option will be modified.
	"""
	OPTIONS_ES_HOSTS_UPDATE = [("1", "Add New Hosts"),
							   ("2", "Modify Hosts"),
							   ("3", "Remove Hosts")]

	"""
	Options displayed when the use of SSL/TLS is enabled.
	"""
	OPTIONS_SSL_TLS_TRUE = [("Disable", "Disable SSL/TLS communication", 0),
							("Certificate Verification", "Modify certificate verification", 0)]

	"""
	Options displayed when the use of SSL/TLS is disabled.
	"""
	OPTIONS_SSL_TLS_FALSE = [("Enable", "Enable SSL/TLS communication", 0)]

	"""
	Options displayed when "SSL certificate verification" option is enabled.
	"""
	OPTIONS_VERIFICATE_CERTIFICATE_TRUE = [("Disable", "Disable certificate verification", 0),
								   		   ("Certificate File", "Change certificate file", 0)]

	"""
	Options displayed when "SSL certificate verification" option is disabled.
	"""
	OPTIONS_VERIFICATE_CERTIFICATE_FALSE = [("Enable", "Enable certificate verification", 0)]

	"""
	Options displayed when "Use authentication method" option is enabled.
	"""
	OPTIONS_AUTHENTICATION_TRUE = [("Data", "Modify authentication method", 0),
								   ("Disable", "Disable authentication method", 0)]

	"""
	Options displayed when an authentication method will be modified.
	"""
	OPTIONS_AUTHENTICATION_METHOD_TRUE = [("Data", "Modify authentication method data", 0),
								   	      ("Disable", "Disable authentication method", 0)]

	"""
	Options displayed when "Use authentication method" option is disabled.
	"""
	OPTIONS_AUTHENTICATION_FALSE = [("Enable", "Enable authentication", 0)]

	"""
	Options displayed when the HTTP authentication credentials will be modified.
	"""
	OPTIONS_HTTP_AUTHENTICATION_DATA = [("Username", "Username for HTTP Authentication", 0),
								 		("Password", "User password", 0)]

	"""
	Options displayed when the API Key credentials will be modified.
	"""
	OPTIONS_API_KEY_DATA = [("API Key ID", "API Key Identifier", 0),
							("Api Key", "API Key", 0)]

	"""
	Options displayed when automatic index removal is enabled.
	"""
	OPTIONS_DELETE_INDEX_TRUE = [("Disable", "Disable automatic index removal", 0)]

	"""
	Options displayed when automatic index removal is disabled
	"""
	OPTIONS_DELETE_INDEX_FALSE = [("Enable", "Enable automatic index removal", 0)]

	"""
	Options displayed in the "Repositories" menu.
	"""
	OPTIONS_REPOSITORIES_MENU = [("1", "Create Repository"),
							     ("2", "Delete Repositories")]

	"""
	Options displayed in the "Indexes" menu.
	"""
	OPTIONS_INDEXES_MENU = [("1", "Delete Indexes")]

	"""
	Options displayed in the "Snapshots" menu.
	"""
	OPTIONS_SNAPSHOTS_MENU = [("1", "Create Snapshot"),
							  ("2", "Delete Snapshots"),
							  ("3", "Restore Snapshot"),
							  ("4", "Mount Searchable Snapshot")]