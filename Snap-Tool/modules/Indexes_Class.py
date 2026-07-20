"""
Class that manages everything related to Indexes.
"""
from os import path
from libPyElk import libPyElk
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram
from libPyConfiguration import libPyConfiguration
from .Telegram_Messages_Class import TelegramMessages

class Indexes:

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


	def delete_indexes(self) -> None:
		"""
		Method that deletes index(es).
		"""
		conn_es = None
		passphrase = None
		telegram_bot_token = None
		telegram_chat_id = None

		try:
			if not path.exists(self.constants.ES_CONFIGURATION):
				self.dialog.create_message("\nES Configuration file not found.", 7, 50, "Error Message")
				return
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
			if not path.exists(self.constants.SNAP_TOOL_CONFIGURATION):
				self.dialog.create_message("\nSnap-Tool Configuration file not found.", 7, 50, "Error Message")
				return
			snap_tool_data = self.utils.read_yaml_file(self.constants.SNAP_TOOL_CONFIGURATION)
			passphrase = self.utils.get_passphrase(self.constants.KEY_FILE)
			telegram_bot_token = self.utils.decrypt_data(snap_tool_data["telegram_bot_token"], passphrase)
			telegram_chat_id = self.utils.decrypt_data(snap_tool_data["telegram_chat_id"], passphrase)
			indexes_list = self.elasticsearch.get_indexes(conn_es)
			if not indexes_list:
				self.dialog.create_message("\nNo indexes found.", 7, 50, "Notification Message")
				return
			tuple_to_rc = self.utils.convert_list_to_tuple_rc(indexes_list, "Index Name")
			indexes = self.dialog.create_checklist("Select one or more options:", 18, 70, tuple_to_rc, "Indexes")
			if not indexes:
				return
			text = self.utils.get_str_from_list(indexes, "Selected Index(es):")
			self.dialog.create_scrollbox(text, 15, 60, "Delete Index(es)")
			delete_index_yn = self.dialog.create_yes_or_no("\nAre you sure to remove the selected indexes?\n\n**NOTE: This action cannot be undone.", 9, 50, "Delete Index(es)")
			if delete_index_yn:
				for index_name in indexes:
					try:
						self.elasticsearch.delete_index(conn_es, index_name)
						self.logger.create_log(f"Index deleted: {index_name}", 3, "_deleteIndex", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
						telegram_message = self.telegram_messages.generate_delete_index_message(index_name)
						response_http_code = self.telegram.send_telegram_message(telegram_bot_token, telegram_chat_id, telegram_message)
						self.telegram_messages.create_log_by_telegram_code(response_http_code)
					except Exception as inner_error:
						self.logger.create_log(f"Failed to delete index {index_name}: {str(inner_error)}", 4, "_deleteIndex", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
				self.dialog.create_message("\nIndex(es) deleted.", 7, 50, "Notification Message")
		except Exception as exception:
			self.dialog.create_message("\nError deleting index(es). For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_deleteIndex", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		finally:
			passphrase = None
			telegram_bot_token = None
			telegram_chat_id = None
			del passphrase
			del telegram_bot_token
			del telegram_chat_id 
			if conn_es and hasattr(conn_es, 'transport') and conn_es.transport:
				conn_es.transport.close()
