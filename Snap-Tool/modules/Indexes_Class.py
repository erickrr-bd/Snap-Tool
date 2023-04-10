from time import strftime
from libPyLog import libPyLog
from libPyElk import libPyElk
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram
from .Telegram_Messages_Class import TelegramMessages

"""
Class that manages ElasticSearch indexes.
"""
class Indexes:

	def __init__(self, action_to_cancel):
		"""
		Class constructor.

		:arg action_to_cancel (object): Method that is executed when the cancel option is selected.
		"""
		self.__logger = libPyLog()
		self.__utils = libPyUtils()
		self.__constants = Constants()
		self.__elasticsearch = libPyElk()
		self.__telegram = libPyTelegram()
		self.__messages = TelegramMessages()
		self.__action_to_cancel = action_to_cancel
		self.__dialog = libPyDialog(self.__constants.BACKTITLE, action_to_cancel)


	def deleteIndexes(self):
		"""
		Method that removes one or more indexes.
		"""
		try:
			snap_tool_data = self.__utils.readYamlFile(self.__constants.PATH_SNAP_TOOL_CONFIGURATION_FILE)
			if snap_tool_data["use_authentication_method"] == True:
				if snap_tool_data["authentication_method"] == "API Key":
					conn_es = self.__elasticsearch.createConnectionToElasticSearchAPIKey(snap_tool_data, self.__constants.PATH_KEY_FILE)
				elif snap_tool_data["authentication_method"] == "HTTP Authentication":
					conn_es = self.__elasticsearch.createConnectionToElasticSearchHTTPAuthentication(snap_tool_data, self.__constants.PATH_KEY_FILE)
			else:
				conn_es = self.__elasticsearch.createConnectionToElasticSearchWithoutAuthentication(snap_tool_data)
			list_all_indexes = self.__elasticsearch.getIndexes(conn_es)
			if list_all_indexes:
				list_to_dialog = self.__utils.convertListToDialogList(list_all_indexes, "Index Name")
				options_delete_indexes = self.__dialog.createCheckListDialog("Select one or more options:", 18, 70, list_to_dialog, "Delete ElasticSearch Indexes")
				message_to_display = self.__utils.getStringFromList(options_delete_indexes, "Selected ElasticSearch indexes:")
				self.__dialog.createScrollBoxDialog(message_to_display, 15, 60, "Delete ElasticSearch Indexes")
				delete_indexes_confirmation = self.__dialog.createYesOrNoDialog("\nAre you sure to remove the selected indexes?", 7, 50, "Delete ElasticSearch Indexes")
				if delete_indexes_confirmation == "ok":
					passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
					password_privileged_actions = self.__dialog.createPasswordBoxDialog("Enter the password for privileged actions:", 8, 50, "password", True)
					if password_privileged_actions == self.__utils.decryptDataWithAES(snap_tool_data["password_privileged_actions"], passphrase).decode("utf-8"):
						telegram_bot_token = self.__utils.decryptDataWithAES(snap_tool_data["telegram_bot_token"], passphrase).decode("utf-8")
						telegram_chat_id = self.__utils.decryptDataWithAES(snap_tool_data["telegram_chat_id"], passphrase).decode("utf-8")
						for index_name in options_delete_indexes:
							self.__elasticsearch.deleteIndex(conn_es, index_name)
							self.__logger.generateApplicationLog("Index deleted: " + index_name, 2, "__deleteIndexes", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
							message_telegram = self.__messages.indexRemovedMessage(index_name)
							response_http_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_telegram)
							self.__messages.createLogByTelegramCode(response_http_code)
						self.__dialog.createMessageDialog("\nIndexes removed.", 7, 50, "Notification Message")
					else:
						self.__dialog.createMessageDialog("\nError deleting selected indexes. Authentication Error.", 8, 50, "Notification Message")
			else:
				self.__dialog.createMessageDialog("\nNo indexes found.", 7, 50, "Notification Message")
			conn_es.transport.close()
		except Exception as exception:
			self.__dialog.createMessageDialog("\nError deleting ElasticSearch indexes. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__deleteIndexes", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		finally:
			self.__action_to_cancel()