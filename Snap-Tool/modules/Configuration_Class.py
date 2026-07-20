"""
Class that manages everything related to the Snap-Tool's configuration.
"""
from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

class Configuration:

	def __init__(self) -> None:
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.telegram_chat_id = ()
		self.constants = Constants()
		self.telegram_bot_token = ()
		self.dialog = libPyDialog(self.constants.BACKTITLE)


	def define_telegram_bot_token(self) -> None:
		"""
		Method that defines the Telegram Bot Token.
		"""
		passphrase = None
		bot_token = None

		try:
			passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
			bot_token = self.dialog.create_inputbox("Enter the Telegram Bot Token:", 8, 50, "bot_token")
			self.telegram_bot_token = self.utils.encrypt_data(bot_token, passphrase)
		finally:
			passphrase = None
			bot_token = None
			del passphrase
			del bot_token


	def define_telegram_chat_id(self) -> None:
		"""
		Method that defines the Telegram Chat ID.
		"""
		passphrase = None
		chat_id = None

		try:
			passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
			chat_id = self.dialog.create_inputbox("Enter the Telegram Chat ID:", 8, 50, "chat_id")
			self.telegram_chat_id = self.utils.encrypt_data(chat_id, passphrase)
		finally:
			passphrase = None
			chat_id = None
			del passphrase
			del chat_id


	def modify_telegram_bot_token(self) -> None:
		"""
		Method that modifies the Telegram Bot Token.
		"""
		passphrase = None
		current_bot_token = None
		bot_token = None

		try:
			passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
			current_bot_token = self.utils.decrypt_data(self.telegram_bot_token, passphrase)
			bot_token = self.dialog.create_inputbox("Enter the Telegram Bot Token:", 8, 50, current_bot_token)
			self.telegram_bot_token = self.utils.encrypt_data(bot_token, passphrase)
			self.logger.create_log("Telegram Bot Token modified.", 3, "_modifySTConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		finally:
			passphrase = None
			current_bot_token = None
			bot_token = None
			del passphrase
			del current_bot_token
			del bot_token


	def modify_telegram_chat_id(self) -> None:
		"""
		Method that modifies the Telegram Chat ID.
		"""
		passphrase = None
		current_chat_id = None
		chat_id = None

		try:
			passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
			current_chat_id = self.utils.decrypt_data(self.telegram_chat_id, passphrase)
			chat_id = self.dialog.create_inputbox("Enter the Telegram Chat ID:", 8, 50, current_chat_id)
			self.telegram_chat_id = self.utils.encrypt_data(chat_id, passphrase)
			self.logger.create_log("Telegram Chat ID modified.", 3, "_modifySTConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		finally:
			passphrase = None
			current_chat_id = None
			chat_id = None
			del passphrase
			del current_chat_id
			del chat_id


	def convert_object_to_dict(self) -> dict:
		"""
		Method that converts a Configuration's object into a dictionary.

		Returns:
			configuration_data_json (dict): Dictionary with the object's data.
		"""
		configuration_data_json = {
			"telegram_bot_token" : self.telegram_bot_token,
			"telegram_chat_id" : self.telegram_chat_id
		}
		return configuration_data_json


	def convert_dict_to_object(self, configuration_data: dict) -> None:
		"""
		Method that converts a dictionary into an Configuration's object.

		Parameters:
			configuration_data (dict): Dictionary to convert.
		"""
		self.telegram_bot_token = configuration_data["telegram_bot_token"]
		self.telegram_chat_id = configuration_data["telegram_chat_id"]


	def create_file(self, configuration_data: dict) -> None:
		"""
		Method that creates the YAML file corresponding to the configuration.

		Parameters:
			configuration_data (dict): Data to save in the YAML file.
		"""
		try:
			self.utils.create_yaml_file(configuration_data, self.constants.SNAP_TOOL_CONFIGURATION)
			self.utils.change_owner( self.constants.SNAP_TOOL_CONFIGURATION, self.constants.USER, self.constants.GROUP, "600")
			if path.exists(self.constants.SNAP_TOOL_CONFIGURATION):
				self.dialog.create_message("\nConfiguration created.", 7, 50, "Notification Message")
				self.logger.create_log("Configuration created", 2, "__createSTConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE)
		except Exception as exception:
			self.dialog.create_message("\nError creating configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_createSTConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass


	def modify_configuration(self) -> None:
		"""
		Method that modifies the configuration.
		"""
		try:
			options = self.dialog.create_checklist("Select one or more options:", 9, 75, self.constants.CONFIGURATION_FIELDS, "Configuration Fields")	
			configuration_data = self.utils.read_yaml_file(self.constants.SNAP_TOOL_CONFIGURATION)
			self.convert_dict_to_object(configuration_data)
			original_hash = self.utils.get_hash_from_file(self.constants.SNAP_TOOL_CONFIGURATION)
			if "Bot Token" in options:
				self.modify_telegram_bot_token()
			if "Chat ID" in options:
				self.modify_telegram_chat_id()
			configuration_data = self.convert_object_to_dict()
			self.utils.create_yaml_file(configuration_data, self.constants.SNAP_TOOL_CONFIGURATION)
			new_hash = self.utils.get_hash_from_file(self.constants.SNAP_TOOL_CONFIGURATION)
			if new_hash == original_hash:
				self.dialog.create_message("\nConfiguration not modified.", 7, 50, "Notification Message")
			else:
				self.dialog.create_message("\nConfiguration modified.", 7, 50, "Notification Message")
		except Exception as exception:
			self.dialog.create_message("\nError modifying configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_modifySTConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass


	def display_configuration(self) -> None:
		"""
		Method that displays the configuration file's data.
		"""
		try:
			configuration_data = self.utils.convert_yaml_to_str(self.constants.SNAP_TOOL_CONFIGURATION)
			text = "\nData:\n\n" + configuration_data
			self.dialog.create_scrollbox(text, 18, 70, "Configuration")
		except Exception as exception:
			self.dialog.create_message("\nError displaying configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_displaySTConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		except KeyboardInterrupt:
			pass
			