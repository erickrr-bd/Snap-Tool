"""
Class that manages the application's constants.
"""
from typing import List
from dataclasses import dataclass, field

@dataclass(frozen = True)
class Constants:
	"""
	Message displayed in the background.
	"""
	BACKTITLE: str = "SNAP-TOOL v3.4 by Erick Rodriguez"

	"""
	Snap-Tool's configuration file.
	"""
	ES_CONFIGURATION: str = "/etc/Snap-Tool/configuration/es_conf.yaml"

	"""
	Snap-Tool's configuration file.
	"""
	SNAP_TOOL_CONFIGURATION: str = "/etc/Snap-Tool/configuration/snap_tool.yaml"

	"""
	Encryption key's file.
	"""
	KEY_FILE: str = "/etc/Snap-Tool/configuration/key"

	"""
	Snap-Tool's log file.
	"""
	LOG_FILE: str = "/var/log/Snap-Tool/snap-tool-log"

	"""
	Options displayed in the "Main" menu.
	"""
	MAIN_MENU_OPTIONS: List = field(default_factory = lambda : [("1", "ES Configuration"), ("2", "Configuration"), ("3", "Snapshots"), ("4", "Indices"), ("5", "Repositories"), ("6", "Nodes Information"), ("7", "About"), ("8", "Exit")])

	"""
	Options that are displayed when the configuration file doesn't exist.
	"""
	CONFIGURATION_OPTIONS_FALSE: List = field(default_factory = lambda : [("Create", "Create the configuration file", 0)])

	"""
	Options that are displayed when the configuration file exists.
	"""
	CONFIGURATION_OPTIONS_TRUE: List = field(default_factory = lambda : [("Modify", "Modify the configuration file", 0), ("Display", "Display the configuration file", 0)])
	
	"""
	Configuration's fields.
	"""
	CONFIGURATION_FIELDS: List = field(default_factory = lambda : [("Bot Token", "Telegram Bot Token", 0), ("Chat ID", "Telegram channel identifier", 0)]) 

	"""
	Options displayed in the "Snapshots" menu.
	"""
	SNAPSHOTS_MENU_OPTIONS: List = field(default_factory = lambda : [("1", "Create Snapshot"), ("2", "Delete Snapshot(s)"), ("3", "Restore Snapshot"), ("4", "Mount Searchable Snapshot")])

	"""
	Options displayed in the "Indexes" menu.
	"""
	INDEXES_MENU_OPTIONS: List = field(default_factory = lambda : [("1", "Delete Index(es)")])

	"""
	Options displayed in the "Repositories" menu.
	"""
	REPOSITORIES_MENU_OPTIONS: List = field(default_factory = lambda : [("1", "Create Repository"), ("2", "Delete Repositories")])


	"""
	Options displayed when automatic index removal is enabled.
	"""
	OPTIONS_DELETE_INDEX_TRUE = [("Disable", "Disable automatic index removal", 0)]

	"""
	Options displayed when automatic index removal is disabled
	"""
	OPTIONS_DELETE_INDEX_FALSE = [("Enable", "Enable automatic index removal", 0)]
