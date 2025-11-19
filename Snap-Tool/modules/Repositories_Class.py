"""
Class that manages everything related to Repositories.
"""
from os import path
from libPyElk import libPyElk
from libPyLog import libPyLog
from dataclasses import dataclass
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram
from libPyConfiguration import libPyConfiguration
from .Telegram_Messages_Class import TelegramMessages

@dataclass
class Repositories:

	def __init__(self) -> None:
		"""
		Class constructor.
		"""
		self.logger = libPyLog()
		self.utils = libPyUtils()
		self.constants = Constants()
		self.elasticsearch = libPyElk()
		self.telegram = libPyTelegram()
		self.telegram_messages = TelegramMessages()
		self.dialog = libPyDialog(self.constants.BACKTITLE)


	def create_repository(self) -> None:
		"""
		Method that creates a repository.
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
				if path.exists(self.constants.SNAP_TOOL_CONFIGURATION):
					snap_tool_data = self.utils.read_yaml_file(self.constants.SNAP_TOOL_CONFIGURATION)
					passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
					telegram_bot_token = self.utils.decrypt_data(snap_tool_data["telegram_bot_token"], passphrase).decode("utf-8")
					telegram_chat_id = self.utils.decrypt_data(snap_tool_data["telegram_chat_id"], passphrase).decode("utf-8")
					repository_name = self.dialog.create_inputbox("Enter the repository's name:", 8, 50, "prueba")
					repository_path = self.dialog.select_directory("/etc", 8, 50, "Repository's Path")
					compress_repository = self.dialog.create_yes_or_no("\nAre metadata files required to be stored compressed?", 8, 50, "Compress Repository")
					compress_repository = True if compress_repository == "ok" else False
					self.elasticsearch.create_repository(conn_es, repository_name, repository_path, compress_repository)
					self.logger.create_log(f"Repository created: {repository_name}", 2, "_createRepository", use_file_handler = True, file_name = self.constants.LOG_FILE)
					telegram_message = self.telegram_messages.generate_create_repository_message(repository_name, repository_path, compress_repository)
					response_http_code = self.telegram.send_telegram_message(telegram_bot_token, telegram_chat_id, telegram_message)
					self.telegram_messages.create_log_by_telegram_code(response_http_code)
					self.dialog.create_message(f"\nRepository created: {repository_name}", 7, 50, "Notification Message")
				else:
					self.dialog.create_message("\nSnap-Tool Configuration file not found.", 7, 50, "Error Message")
				conn_es.transport.close()
			else:
				self.dialog.create_message("\nES Configuration file not found.", 7, 50, "Error Message")
		except Exception as exception:
			self.dialog.create_message("\nError creating repository. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_createRepository", use_file_handler = True, file_name = self.constants.LOG_FILE)


	def delete_repositories(self) -> None:
		"""
		Method that deletes repositories.
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
				if path.exists(self.constants.SNAP_TOOL_CONFIGURATION):
					snap_tool_data = self.utils.read_yaml_file(self.constants.SNAP_TOOL_CONFIGURATION)
					passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
					telegram_bot_token = self.utils.decrypt_data(snap_tool_data["telegram_bot_token"], passphrase).decode("utf-8")
					telegram_chat_id = self.utils.decrypt_data(snap_tool_data["telegram_chat_id"], passphrase).decode("utf-8")
					repositories_list = self.elasticsearch.get_repositories(conn_es)
					if repositories_list:
						tuple_to_rc = self.utils.convert_list_to_tuple_rc(repositories_list, "Repository Name")
						repositories = self.dialog.create_checklist("Select one or more options:", 18, 70, tuple_to_rc, "Repositories")
						text = self.utils.get_str_from_list(repositories, "Selected Repositories:")
						self.dialog.create_scrollbox(text, 15, 60, "Delete Repositories")
						delete_repository_yn = self.dialog.create_yes_or_no("\nAre you sure to remove the selected repositories?\n\n**NOTE: This action cannot be undone.", 10, 50, "Delete Repositories")
						if delete_repository_yn == "ok":
							for repository_name in repositories:
								self.elasticsearch.delete_repository(conn_es, repository_name)
								self.logger.create_log(f"Repository deleted: {repository_name}", 3, "_deleteRepository", use_file_handler = True, file_name = self.constants.LOG_FILE)
								telegram_message = self.telegram_messages.generate_delete_repository_message(repository_name)
								response_http_code = self.telegram.send_telegram_message(telegram_bot_token, telegram_chat_id, telegram_message)
								self.telegram_messages.create_log_by_telegram_code(response_http_code)
							self.dialog.create_message("\nRepositories deleted.", 7, 50, "Notification Message")
					else:
						self.dialog.create_message("\nNo repositories found.", 7, 50, "Notification Message")
				else:
					self.dialog.create_message("\nSnap-Tool's Configuration not found.", 7, 50, "Error Message")
				conn_es.transport.close()
			else:
				self.dialog.create_message("\nES Configuration not found.", 7, 50, "Error Message")
		except Exception as exception:
			self.dialog.create_message("\nError deleting repositories. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_deleteRepository", use_file_handler = True, file_name = self.constants.LOG_FILE)
