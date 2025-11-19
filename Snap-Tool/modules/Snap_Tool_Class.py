"""
Class that manages everything related to Snap-Tool.
"""
from os import path
from sys import exit
from libPyElk import libPyElk
from libPyLog import libPyLog
from dataclasses import dataclass
from libPyUtils import libPyUtils
from .Indexes_Class import Indexes
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from .Snapshots_Class import Snapshots
from .Repositories_Class import Repositories
from .Configuration_Class import Configuration
from libPyConfiguration import libPyConfiguration

@dataclass
class SnapTool:

	def __init__(self) -> None:
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.elasticsearch = libPyElk()
		self.dialog = libPyDialog(self.constants.BACKTITLE)


	def main_menu(self) -> None:
		"""
		Main menu.
    	"""
		try:
			option = self.dialog.create_menu("Select a option:", 15, 50, self.constants.MAIN_MENU_OPTIONS, "Main Menu")
			self.switch_main_menu(int(option))
		except KeyboardInterrupt:
			pass


	def snapshots_menu(self) -> None:
		"""
		Snapshots' menu.
		"""
		option = self.dialog.create_menu("Select a option:", 11, 50, self.constants.SNAPSHOTS_MENU_OPTIONS, "Snapshots Menu")
		self.switch_snapshots_menu(int(option))


	def indexes_menu(self) -> None:
		"""
		Indexes' menu.
		"""
		option = self.dialog.create_menu("Select a option:", 8, 50, self.constants.INDEXES_MENU_OPTIONS, "Indexes Menu")
		self.switch_indexes_menu(int(option))


	def repositories_menu(self) -> None:
		"""
		Repositories' menu.
		"""
		option = self.dialog.create_menu("Select a option:", 9, 50, self.constants.REPOSITORIES_MENU_OPTIONS, "Repositories Menu")
		self.switch_repositories_menu(int(option))


	def switch_main_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "Main" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		match option:
			case 1:
				self.define_es_configuration()
			case 2:
				self.define_configuration()
			case 3:
				self.snapshots_menu()
			case 4:
				self.indexes_menu()
			case 5:
				self.repositories_menu()
			case 6:
				self.display_nodes_information()
			case 7:
				self.display_about()
			case 8:
				exit(1)


	def switch_snapshots_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "Snapshots" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		snapshots = Snapshots()
		match option:
			case 1:
				snapshots.create_snapshot()
			case 2:
				snapshots.delete_snapshot()
			case 3:
				snapshots.restore_snapshot()
			case 4:
				snapshots.delete_inventories()


	def switch_indexes_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "Indexes" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		indexes = Indexes()
		match option:
			case 1:
				indexes.delete_indexes()


	def switch_repositories_menu(self, option: int) -> None:
		"""
		Method that executes an action based on the option chosen in the "Repositories" menu.

		Parameters:
    		option (int): Chosen option.
		"""
		repositories = Repositories()
		match option:
			case 1:
				repositories.create_repository()
			case 2:
				repositories.delete_repositories()


	def define_es_configuration(self) -> None:
		"""
		Method that defines the action to be performed on the ElasticSearch connection's configuration with Snap-Tool.
		"""
		if not path.exists(self.constants.ES_CONFIGURATION):
			option = self.dialog.create_radiolist("Select a option:", 8, 50, self.constants.CONFIGURATION_OPTIONS_FALSE, "ES Configuration")
			if option == "Create":
				self.create_es_configuration()
		else:
			option = self.dialog.create_radiolist("Select a option:", 9, 50, self.constants.CONFIGURATION_OPTIONS_TRUE, "ES Configuration")
			self.modify_es_configuration() if option == "Modify" else self.display_es_configuration()


	def create_es_configuration(self) -> None:
		"""
		Method that creates the configuration for the connection between ElasticSearch and Snap-Tool.
		"""
		es_data = libPyConfiguration(self.constants.BACKTITLE)
		es_data.define_es_host()
		es_data.define_verificate_certificate()
		es_data.define_use_authentication(self.constants.KEY_FILE)
		es_data.create_file(es_data.convert_object_to_dict(), self.constants.ES_CONFIGURATION, self.constants.LOG_FILE)


	def modify_es_configuration(self) -> None:
		"""
		Method that updates the configuration for the connection between ElasticSearch and Snap-Tool.
		"""
		es_data = libPyConfiguration(self.constants.BACKTITLE)
		es_data.modify_configuration(self.constants.ES_CONFIGURATION, self.constants.KEY_FILE, self.constants.LOG_FILE)


	def display_es_configuration(self) -> None:
		"""
		Method that displays the configuration for the connection between ElasticSearch and Snap-Tool.
		"""
		es_data = libPyConfiguration(self.constants.BACKTITLE)
		es_data.display_configuration(self.constants.ES_CONFIGURATION, self.constants.LOG_FILE)


	def define_configuration(self) -> None:
		"""
		Method that defines the action to be performed on the Snap-Tool's configuration.
		"""
		if not path.exists(self.constants.SNAP_TOOL_CONFIGURATION):
			option = self.dialog.create_radiolist("Select a option:", 8, 50, self.constants.CONFIGURATION_OPTIONS_FALSE, "Snap-Tool Configuration")
			if option == "Create":
				self.create_configuration()
		else:
			option = self.dialog.create_radiolist("Select a option:", 9, 50, self.constants.CONFIGURATION_OPTIONS_TRUE, "Snap-Tool Configuration")
			self.modify_configuration() if option == "Modify" else self.display_configuration()


	def create_configuration(self) -> None:
		"""
		Method that creates the Snap-Tool's configuration.
		"""
		snap_tool_data = Configuration()
		snap_tool_data.define_telegram_bot_token()
		snap_tool_data.define_telegram_chat_id()
		snap_tool_data.create_file(snap_tool_data.convert_object_to_dict())


	def modify_configuration(self) -> None:
		"""
		Method that updates the Snap-Tool's configuration.
		"""
		snap_tool_data = Configuration()
		snap_tool_data.modify_configuration()


	def display_configuration(self) -> None:
		"""
		Method that displays the Snap-Tool's configuration.
		"""
		snap_tool_data = Configuration()
		snap_tool_data.display_configuration()


	def display_nodes_information(self):
		"""
		Method that displays the space available on each of the nodes in the ElasticSearch cluster.
		"""
		try:
			if path.exists(self.constants.ES_CONFIGURATION):
				configuration = libPyConfiguration()
				data = self.utils.read_yaml_file(self.constants.ES_CONFIGURATION)
				configuration.convert_dict_to_object(data)
				if configuration.use_authentication:
					if configuration.authentication_method == "HTTP Authentication":
						conn_es = self.elasticsearch.create_connection_http_auth(configuration, self.constants.KEY_FILE)
					elif configuration.authentication_method == "API Key":
						conn_es = self.elasticsearch.create_connection_api_key(configuration, self.constants.KEY_FILE)
				else:
					conn_es = self.elasticsearch.create_connection_without_auth(configuration)
				nodes_info = self.elasticsearch.get_nodes_information(conn_es)
				text = "\nDisk space occupied:\n\n"
				for node in nodes_info:
					text += f"- {nodes_info[node]["name"]}\n"
					total_size_disk = nodes_info[node]["fs"]["total"]["total_in_bytes"]
					total_size_available_disk = nodes_info[node]["fs"]["total"]["available_in_bytes"]
					total_size_occupied_in_percentage = 100 - (total_size_available_disk * 100 / total_size_disk)
					text += f"Occupied percentage: {round(total_size_occupied_in_percentage, 2)}%\n\n"
				conn_es.transport.close()
				self.dialog.create_scrollbox(text, 16, 70, "Nodes information")
			else:
				self.dialog.create_message("\nES Configuration file not found.", 7, 50, "Error Message")
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Error")


	def display_about(self) -> None:
		"""
		Method that displays the about of the application.
		"""
		try:
			text = "\nAuthor: Erick Roberto Rodríguez Rodríguez\nEmail: erickrr.tbd93@gmail.com, erodriguez@tekium.mx\nGithub: https://github.com/erickrr-bd/Snap-Tool\nSnap-Tool v3.4 - November 2025" + "\n\nModular toolkit for managing Elasticsearch snapshots,\nrepositories, and indexes via Python."
			self.dialog.create_scrollbox(text, 13, 60, "About")
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Error")
