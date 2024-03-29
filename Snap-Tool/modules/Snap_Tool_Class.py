from os import path
from sys import exit
from .Indexes_Class import Indexes
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from .Snapshots_Class import Snapshots
from .Repositories_Class import Repositories
from .Nodes_Information_Class import NodesInformation
from .Snap_Tool_Configuration_Class import SnapToolConfiguration

"""
Class that manages the operation of Snap-Tool.
"""
class SnapTool:

	def __init__(self):
		"""
		Class constructor.
		"""
		self.__constants = Constants()
		self.__dialog = libPyDialog(self.__constants.BACKTITLE, self.mainMenu)


	def mainMenu(self):
		"""
		Method that displays the "Main" menu.
		"""
		option_main_menu = self.__dialog.createMenuDialog("Select a option:", 14, 50, self.__constants.OPTIONS_MAIN_MENU, "Main Menu")
		self.__switchMainMenu(int(option_main_menu))


	def __repositoriesMenu(self):
		"""
		Method that displays the "Repositories" menu.
		"""
		option_repositories_menu = self.__dialog.createMenuDialog("Select a option:", 9, 50, self.__constants.OPTIONS_REPOSITORIES_MENU, "Repositories Menu")
		self.__switchRepositoriesMenu(int(option_repositories_menu))


	def __snapshotsMenu(self):
		"""
		Method that displays the "Snapshots" menu.
		"""
		option_snapshots_menu = self.__dialog.createMenuDialog("Select a option:", 11, 50, self.__constants.OPTIONS_SNAPSHOTS_MENU, "Snapshots Menu")
		self.__switchSnapshotsMenu(int(option_snapshots_menu))


	def __indexesMenu(self):
		"""
		Method that displays the "Indexes" menu.
		"""
		option_indexes_menu = self.__dialog.createMenuDialog("Select a option:", 8, 50, self.__constants.OPTIONS_INDEXES_MENU, "Indexes Menu")
		self.__switchIndexesMenu(int(option_indexes_menu))


	def __switchMainMenu(self, option_main_menu):
		"""
		Method that executes an action based on the option selected in the "Main" menu.

		:arg option_main_menu (integer): Chosen option.
		"""
		if option_main_menu == 1:
			self.__defineConfiguration()
		elif option_main_menu == 2:
			self.__repositoriesMenu()
		elif option_main_menu == 3:
			self.__snapshotsMenu()
		elif option_main_menu == 4:
			self.__indexesMenu()
		elif option_main_menu == 5:
			nodes_information = NodesInformation(self.mainMenu)
			nodes_information.displayNodesInformation()
		elif option_main_menu == 6:
			self.__showAboutApplication()
		elif option_main_menu == 7:
			exit(1)


	def __switchRepositoriesMenu(self, option_repositories_menu):
		"""
		Method that executes an action based on the option selected in the "Repositories" menu.

		:arg option_repositories_menu (integer): Chosen option.
		"""
		repositories = Repositories(self.mainMenu)
		if option_repositories_menu == 1:
			repositories.createRepository()
		elif option_repositories_menu == 2:
			repositories.deleteRepositories()


	def __switchSnapshotsMenu(self, option_snapshots_menu):
		"""
		Method that executes an action based on the option selected in the "Snapshots" menu.

		:arg option_snapshots_menu (integer): Chosen option.
		"""
		snapshots = Snapshots(self.mainMenu)
		if option_snapshots_menu == 1:
			snapshots.createSnapshot()
		elif option_snapshots_menu == 2:
			snapshots.deleteSnapshots()
		elif option_snapshots_menu == 3:
			snapshots.restoreSnapshot()
		elif option_snapshots_menu == 4:
			snapshots.mountSearchableSnapshot()


	def __switchIndexesMenu(self, option_indexes_menu):
		"""
		Method that executes an action based on the option selected in the "Indexes" menu.

		:arg option_indexes_menu (integer): Chosen option.
		"""
		indexes = Indexes(self.mainMenu)
		if option_indexes_menu == 1:
			indexes.deleteIndexes()


	def __defineConfiguration(self):
		"""
		Method that defines the actions to perform on the Snap-Tool configuration.
		"""
		snap_tool_configuration = SnapToolConfiguration(self.mainMenu)
		if not path.exists(self.__constants.PATH_SNAP_TOOL_CONFIGURATION_FILE):
			option_configuration_false = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_CONFIGURATION_FALSE, "Snap-Tool Configuration Options")
			if option_configuration_false == "Create":
				snap_tool_configuration.createConfiguration()
		else:
			option_configuration_true = self.__dialog.createRadioListDialog("Select a option:", 9, 50, self.__constants.OPTIONS_CONFIGURATION_TRUE, "Snap-Tool Configuration Options")
			if option_configuration_true == "Update":
				snap_tool_configuration.updateConfiguration()
			elif option_configuration_true == "Display":
				snap_tool_configuration.displayConfigurationData()


	def __showAboutApplication(self):
		"""
		Method that displays information about the application
		"""
		message_to_display = "\nCopyright@2023 Tekium. All rights reserved.\nSnap-Tool v3.3\nAuthor: Erick Rodríguez\nEmail: erickrr.tbd93@gmail.com, erodriguez@tekium.mx\n" + "License: GPLv3\n\nEasy management of snapshots, repositories and indexes\nwith ElasticSearch and Python."
		self.__dialog.createScrollBoxDialog(message_to_display, 14, 60, "About")
		self.mainMenu()