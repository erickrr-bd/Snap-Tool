"""
Class that manages all the constant variables of the application.
"""
class Constants:
	"""
	Title that is shown in the background of the application.
	"""
	BACKTITLE = "SNAP-TOOL"

	"""
	Absolute path of the Snap-Tool configuration file.
	"""
	PATH_CONFIGURATION_FILE = "/etc/Snap-Tool/configuration/snap_tool_conf.yaml"

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
	OPTIONS_MAIN_MENU = [("1", "Snap-Tool Configuration"),
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
	OPTIONS_CONFIGURATION_TRUE = [("Modify", "Modify the configuration file", 0),
								  ("Show", "Show the configuration data", 0)]

	"""
	Options that are shown when the configuration file exists.
	"""
	OPTIONS_AUTHENTICATION_METHOD = [("HTTP authentication", "Use HTTP Authentication", 0),
								     ("API Key", "Use API Key", 0)]