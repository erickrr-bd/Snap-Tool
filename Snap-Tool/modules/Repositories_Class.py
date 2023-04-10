from libPyElk import libPyElk
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram
from .Telegram_Messages_Class import TelegramMessages

"""
Class that manages the ElasticSearch repositories.
"""
class Repositories:

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


	def createRepository(self):
		"""
		Method that creates an ElasticSearch repository.
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
			passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
			telegram_bot_token = self.__utils.decryptDataWithAES(snap_tool_data["telegram_bot_token"], passphrase).decode("utf-8")
			telegram_chat_id = self.__utils.decryptDataWithAES(snap_tool_data["telegram_chat_id"], passphrase).decode("utf-8")
			repository_name = self.__dialog.createInputBoxDialog("Enter the repository name:", 8, 50, "repository_name")
			path_repository = self.__dialog.createFolderDialog("/etc/Snap-Tool/configuration", 8, 50, "Path Repository")
			use_compress_repository = self.__dialog.createYesOrNoDialog("\nDo you require metadata files to be stored compressed?", 8, 50, "Compress Repository")
			use_compress_repository = True if use_compress_repository == "ok" else False
			self.__elasticsearch.createRepository(conn_es, repository_name, path_repository, use_compress_repository)
			message_telegram = self.__messages.createRepositoryMessage(repository_name, path_repository, use_compress_repository)
			response_http_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_telegram)
			self.__messages.createLogByTelegramCode(response_http_code)
			conn_es.transport.close()
		except Exception as exception:
			self.__dialog.createMessageDialog("\nError creating repository. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createRepository", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		finally:
			self.__action_to_cancel()


	def deleteRepositories(self):
		"""
		Method that deletes one or more repositories.
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
			list_all_repositories = self.__elasticsearch.getRepositories(conn_es)
			if list_all_repositories:
				list_to_dialog = self.__utils.convertListToDialogList(list_all_repositories, "Repository Name")
				options_delete_repositories = self.__dialog.createCheckListDialog("Select one or more options:", 18, 70, list_to_dialog, "Delete ElasticSearch Repositories")
				message_to_display = self.__utils.getStringFromList(options_delete_repositories, "Selected ElasticSearch repositories:")
				self.__dialog.createScrollBoxDialog(message_to_display, 15, 60, "Delete ElasticSearch Repositories")
				delete_repositories_confirmation = self.__dialog.createYesOrNoDialog("\nAre you sure to remove the selected repositories?", 8, 50, "Delete ElasticSearch Repositories")
				if delete_repositories_confirmation == "ok":
					passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
					password_privileged_actions = self.__dialog.createPasswordBoxDialog("Enter the password for privileged actions:", 8, 50, "password", True)
					if password_privileged_actions == self.__utils.decryptDataWithAES(snap_tool_data["password_privileged_actions"], passphrase).decode("utf-8"):
						telegram_bot_token = self.__utils.decryptDataWithAES(snap_tool_data["telegram_bot_token"], passphrase).decode("utf-8")
						telegram_chat_id = self.__utils.decryptDataWithAES(snap_tool_data["telegram_chat_id"], passphrase).decode("utf-8")
						for repository in options_delete_repositories:
							self.__elasticsearch.deleteRepository(conn_es, repository)
							self.__logger.generateApplicationLog("Repository removed: " + repository, "2", "__deleteRepositories", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
							message_telegram = self.__messages.deleteRepositoryMessage(repository)
							response_http_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_telegram)
							self.__messages.createLogByTelegramCode(response_http_code)
						self.__dialog.createMessageDialog("\nDeleted repositories.", 7, 50, "Notification Message")
					else:
						self.__dialog.createMessageDialog("\nError deleting repositories. Authentication failed.", 8, 50, "Notification Message")
			else:
				self.__dialog.createMessageDialog("\nNo repositories found.", 7, 50, "Notification Message")
			conn_es.transport.close()
		except Exception as exception:
			self.__dialog.createMessageDialog("\nFailed to delete repositories. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__deleteRepositories", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		finally:
			self.__action_to_cancel()