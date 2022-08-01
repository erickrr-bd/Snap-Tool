from os import path
from sys import exit
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from .Snap_Tool_Configuration_Class import SnapToolConfiguration

class SnapTool:

	__dialog = None

	__constants = None

	def __init__(self):
		self.__constants = Constants()
		self.__dialog = libPyDialog(self.__constants.BACKTITLE, self.mainMenu)


	def mainMenu(self):
		"""
		Method that shows the "Main" menu.
		"""
		option_main_menu = self.__dialog.createMenuDialog("Select a option:", 14, 50, self.__constants.OPTIONS_MAIN_MENU, "Main Menu")
		self.__switchMainMenu(int(option_main_menu))


	def __switchMainMenu(self, option):
		"""
		Method that executes a certain action based on the number of the option chosen in the "Main" menu.

		:arg option (integer): Option number.
		"""
		if option == 1:
			self.__defineSnapToolConfiguration()
		"""
		elif option == 2:
			self.__alertRulesMenu()
		elif option == 3:
			self.__serviceMenu()
		elif option == 4:
			self.__TelkAlertAgentMenu()
		elif option == 5:
			self.__TelkAlertReportMenu()
		elif option == 6:
			self.__showAboutApplication()
		elif option == 7:
			exit(1)
		"""

	def __defineSnapToolConfiguration(self):
		"""
		
		"""
		snap_tool_configuration = SnapToolConfiguration(self.mainMenu)
		if not path.exists(self.__constants.PATH_CONFIGURATION_FILE):
			option_configuration_false = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_CONFIGURATION_FALSE, "Configuration Options")
			if option_configuration_false == "Create":
				snap_tool_configuration.createSnapToolConfiguration()
		else:
			option_configuration_true = self.__dialog.createRadioListDialog("Select a option:", 10, 50, self.__constants.OPTIONS_CONFIGURATION_TRUE, "Configuration Options")
			if option_configuration_true == "Modify":
				snap_tool_configuration.modifySnapToolConfiguration()
			elif option_configuration_true == "Show":
				snap_tool_configuration.showSnapToolConfiguration()