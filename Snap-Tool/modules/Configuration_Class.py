"""
Class that manages everything related to the Snap-Tool's configuration.
"""
from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from dataclasses import dataclass, field

@dataclass
class Configuration:

	telegram_bot_token: tuple = field(default_factory = tuple)
	telegram_chat_id: tuple = field(default_factory = tuple)

	def __init__(self) -> None:
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.dialog = libPyDialog(self.constants.BACKTITLE)


	def define_telegram_bot_token(self) -> None:
		"""
		Method that defines the Telegram Bot Token.
		"""
		passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
		self.telegram_bot_token = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the Telegram Bot Token:", 8, 50, "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), passphrase)


	def define_telegram_chat_id(self) -> None:
		"""
		Method that defines the Telegram Chat ID.
		"""
		passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
		self.telegram_chat_id = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the Telegram Chat ID:", 8, 50, "-1002365478941"), passphrase)


	def modify_telegram_bot_token(self) -> None:
		"""
		Method that modifies the Telegram Bot Token.
		"""
		passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
		self.telegram_bot_token = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the Telegram Bot Token:", 8, 50, self.utils.decrypt_data(self.telegram_bot_token, passphrase).decode("utf-8")), passphrase)
		self.logger.create_log("Telegram Bot Token modified.", 3, "_modifySTConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE)


	def modify_telegram_chat_id(self) -> None:
		"""
		Method that modifies the Telegram Chat ID.
		"""
		passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
		self.telegram_chat_id = self.utils.encrypt_data(self.dialog.create_inputbox("Enter the Telegram Chat ID:", 8, 50, self.utils.decrypt_data(self.telegram_chat_id, passphrase).decode("utf-8")), passphrase)
		self.logger.create_log("Telegram Chat ID modified.", 3, "_modifySTConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE)


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
			if path.exists(self.constants.SNAP_TOOL_CONFIGURATION):
				self.dialog.create_message("\nConfiguration created.", 7, 50, "Notification Message")
				self.logger.create_log("Configuration created", 2, "__createSTConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE)
		except Exception as exception:
			self.dialog.create_message("\nError creating configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_createSTConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


	def modify_configuration(self) -> None:
		"""
		Method that modifies the configuration.
		"""
		try:
			options = self.dialog.create_checklist("Select one or more options:", 13, 75, self.constants.CONFIGURATION_FIELDS, "Configuration Fields")
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
			self.logger.create_log(exception, 4, "_modifySTConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")


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
			self.logger.create_log(exception, 4, "_displaySTConfiguration", use_file_handler = True, file_name = self.constants.LOG_FILE)
		except KeyboardInterrupt:
			pass
		finally:
			raise KeyboardInterrupt("Exit")
			