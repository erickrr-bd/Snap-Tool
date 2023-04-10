from time import sleep
from libPyElk import libPyElk
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants
from libPyTelegram import libPyTelegram
from .Telegram_Messages_Class import TelegramMessages

"""
Class that manages ElasticSearch snapshots.
"""
class Snapshots:

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


	def createSnapshot(self):
		"""
		Method that creates a snapshot.
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
				option_index_name = self.__dialog.createRadioListDialog("Select a option:", 18, 70, list_to_dialog, "Create Snapshot")
				list_all_repositories = self.__elasticsearch.getRepositories(conn_es)
				if list_all_repositories:
					list_to_dialog = self.__utils.convertListToDialogList(list_all_repositories, "Repository Name")
					option_repository_name = self.__dialog.createRadioListDialog("Select a option:", 18, 70, list_to_dialog, "Create Snapshot")
					passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
					telegram_bot_token = self.__utils.decryptDataWithAES(snap_tool_data["telegram_bot_token"], passphrase).decode("utf-8")
					telegram_chat_id = self.__utils.decryptDataWithAES(snap_tool_data["telegram_chat_id"], passphrase).decode("utf-8")
					self.__elasticsearch.createSnapshot(conn_es, option_repository_name, option_index_name, False)
					message_telegram = self.__messages.createSnapshotMessage(option_repository_name, option_index_name)
					response_http_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_telegram)
					self.__messages.createLogByTelegramCode(response_http_code)
					while True:
						current_status_snapshot = self.__elasticsearch.getStatusSnapshot(conn_es, option_repository_name, option_index_name)
						if current_status_snapshot == "SUCCESS":
							break
						sleep(60)
					snapshot_info = self.__elasticsearch.getSnapshotInfo(conn_es, option_repository_name, option_index_name)
					message_telegram = self.__messages.endSnapshotMessage(option_repository_name, option_index_name, snapshot_info["snapshots"][0]["start_time"], snapshot_info["snapshots"][0]["end_time"])
					response_http_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_telegram)
					self.__messages.createLogByTelegramCode(response_http_code)
					self.__dialog.createMessageDialog("\nSnapshot created: " + option_index_name, 7, 50, "Notification Message")
					if snap_tool_data["delete_index_automatic"] == True:
						self.__elasticsearch.deleteIndex(conn_es, option_index_name)
						if not conn_es.indices.exists(option_index_name):
							self.__logger.generateApplicationLog("Index removed: " + option_index_name, 2, "__createSnapshot", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
							message_telegram = self.__messages.indexRemovedMessage(option_index_name)
							response_http_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_telegram)
							self.__messages.createLogByTelegramCode(response_http_code)
							self.__dialog.createMessageDialog("\nIndex removed: " + option_index_name, 7, 50, "Notification Message")
					else:
						delete_index_confirmation = self.__dialog.createYesOrNoDialog("\nAre you sure to remove the index: " + option_index_name + "?", 8, 50, "Delete ElasticSearch Index")
						if delete_index_confirmation == "ok":
							password_privileged_actions = self.__dialog.createPasswordBoxDialog("Enter the password for privileged actions:", 8, 50, "password", True)
							if password_privileged_actions == self.__utils.decryptDataWithAES(snap_tool_data["password_privileged_actions"], passphrase).decode("utf-8"):
								self.__elasticsearch.deleteIndex(conn_es, option_index_name)
								if not conn_es.indices.exists(option_index_name):
									self.__logger.generateApplicationLog("Index removed: " + option_index_name, 2, "__createSnapshot", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
									message_telegram = self.__messages.indexRemovedMessage(option_index_name)
									response_http_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_telegram)
									self.__messages.createLogByTelegramCode(response_http_code)
									self.__dialog.createMessageDialog("\nIndex removed: " + option_index_name, 7, 50, "Notification Message")
							else:
								self.__dialog.createMessageDialog("\nError deleting index. Authentication failed.", 8, 50, "Notification Message")
				else:
					self.__dialog.createMessageDialog("\nNo repositories found.", 7, 50, "Notification Message")
			else:
				self.__dialog.createMessageDialog("\nNo indexes found.", 7, 50, "Notification Message")
			conn_es.transport.close()
		except Exception as exception:
			self.__dialog.createMessageDialog("\nError to create snapshot. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createSnapshot", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		finally:
			self.__action_to_cancel()


	def deleteSnapshots(self):
		"""
		Method that deletes one or more snapshots.
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
				option_repository_name = self.__dialog.createRadioListDialog("Select a option:", 18, 70, list_to_dialog, "Delete ElasticSearch Snapshots")
				list_all_snapshots = self.__elasticsearch.getSnapshotsbyRepository(conn_es, option_repository_name)
				if list_all_snapshots:
					list_to_dialog = self.__utils.convertListToDialogList(list_all_snapshots, "Snapshot Name")
					options_delete_snapshots = self.__dialog.createCheckListDialog("Select one or more options:", 18, 70, list_to_dialog, "Delete ElasticSearch Snapshots")
					message_to_display = self.__utils.getStringFromList(options_delete_snapshots, "Selected ElasticSearch snapshots:")
					self.__dialog.createScrollBoxDialog(message_to_display, 15, 60, "Delete ElasticSearch Snapshots")
					delete_snapshots_confirmation = self.__dialog.createYesOrNoDialog("\nAre you sure to remove the selected snapshots?", 7, 50, "Delete ElasticSearch Snapshots")
					if delete_snapshots_confirmation == "ok":
						passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
						password_privileged_actions = self.__dialog.createPasswordBoxDialog("Enter the password for privileged actions:", 8, 50, "password", True)
						if password_privileged_actions == self.__utils.decryptDataWithAES(snap_tool_data["password_privileged_actions"], passphrase).decode("utf-8"):
							telegram_bot_token = self.__utils.decryptDataWithAES(snap_tool_data["telegram_bot_token"], passphrase).decode("utf-8")
							telegram_chat_id = self.__utils.decryptDataWithAES(snap_tool_data["telegram_chat_id"], passphrase).decode("utf-8")
							for snapshot in options_delete_snapshots:
								self.__elasticsearch.deleteSnapshot(conn_es, option_repository_name, snapshot)
								self.__logger.generateApplicationLog("Snapshot removed: " + snapshot, "2", "__deleteSnapshots", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
								message_telegram = self.__messages.snapshotRemovedMessage(option_repository_name, snapshot)
								response_http_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_telegram)
								self.__messages.createLogByTelegramCode(response_http_code)
							self.__dialog.createMessageDialog("\nDeleted snapshots.", 7, 50, "Notification Message")
						else:
							self.__dialog.createMessageDialog("\nError deleting index. Authentication failed.", 8, 50, "Notification Message")
				else:
					self.__dialog.createMessageDialog("\nNo snapshots found in the repository.", 7, 50, "Notification Message")
			else:
				self.__dialog.createMessageDialog("\nNo repositories found.", 7, 50, "Notification Message")
			conn_es.transport.close()
		except Exception as exception:
			self.__dialog.createMessageDialog("\nFailed to delete snapshots. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__deleteSnapshots", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		finally:
			self.__action_to_cancel()


	def restoreSnapshot(self):
		"""
		Method that restores a snapshot.
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
				option_repository_name = self.__dialog.createRadioListDialog("Select a option:", 18, 70, list_to_dialog, "Restore ElasticSearch Snapshot")
				list_all_snapshots = self.__elasticsearch.getSnapshotsbyRepository(conn_es, option_repository_name)
				if list_all_snapshots:
					list_to_dialog = self.__utils.convertListToDialogList(list_all_snapshots, "Snapshot Name")
					option_restore_snapshot = self.__dialog.createRadioListDialog("Select a option:", 18, 70, list_to_dialog, "Restore ElasticSearch Snapshot")
					restore_snapshot_confirmation = self.__dialog.createYesOrNoDialog("\nAre you sure to restore the snapshot: " + option_restore_snapshot + "?", 8, 50, "Restore ElasticSearch Snapshot")
					if restore_snapshot_confirmation == "ok":
						passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
						telegram_bot_token = self.__utils.decryptDataWithAES(snap_tool_data["telegram_bot_token"], passphrase).decode("utf-8")
						telegram_chat_id = self.__utils.decryptDataWithAES(snap_tool_data["telegram_chat_id"], passphrase).decode("utf-8")
						self.__elasticsearch.restoreSnapshot(conn_es, option_repository_name, option_restore_snapshot, False)
						self.__logger.generateApplicationLog("Snapshot restored: " + option_restore_snapshot, 1, "__restoreSnapshot", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
						message_telegram = self.__messages.snapshotRestoredMessage(option_repository_name, option_restore_snapshot)
						response_http_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_telegram)
						self.__messages.createLogByTelegramCode(response_http_code)
						self.__dialog.createMessageDialog("\nSnapshot restored: " + option_restore_snapshot, 7, 50, "Notification Message")
				else:
					self.__dialog.createMessageDialog("\nNo snapshots found in the repository.", 7, 50, "Notification Message")
			else:
				self.__dialog.createMessageDialog("\nNo repositories found.", 7, 50, "Notification Message")
			conn_es.transport.close()
		except Exception as exception:
			self.__dialog.createMessageDialog("\nFailed to restore snapshot. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__restoreSnapshot", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		finally:
			self.__action_to_cancel()


	def mountSearchableSnapshot(self):
		"""
		Method that mounts a snapshot as a searchable snapshot.
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
				option_repository_name = self.__dialog.createRadioListDialog("Select a option:", 18, 70, list_to_dialog, "Mount Searchable Snapshot")
				list_all_snapshots = self.__elasticsearch.getSnapshotsbyRepository(conn_es, option_repository_name)
				if list_all_snapshots:
					list_to_dialog = self.__utils.convertListToDialogList(list_all_snapshots, "Snapshot Name")
					option_mount_snapshot = self.__dialog.createRadioListDialog("Select a option:", 18, 70, list_to_dialog, "Mount Searchable Snapshot")
					mount_snapshot_confirmation = self.__dialog.createYesOrNoDialog("\nAre you sure to mount the snapshot: " + option_mount_snapshot + "?", 8, 50, "Mount Searchable Snapshot")
					if mount_snapshot_confirmation == "ok":
						passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
						telegram_bot_token = self.__utils.decryptDataWithAES(snap_tool_data["telegram_bot_token"], passphrase).decode("utf-8")
						telegram_chat_id = self.__utils.decryptDataWithAES(snap_tool_data["telegram_chat_id"], passphrase).decode("utf-8")
						self.__elasticsearch.mountSearchableSnapshot(conn_es, option_repository_name, option_mount_snapshot, False)
						self.__logger.generateApplicationLog("Snapshot mounted: " + option_mount_snapshot, 1, "__mounSearchableSnapshot", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
						message_telegram = self.__messages.mountSearchableSnapshotMessage(option_repository_name, option_mount_snapshot)
						response_http_code = self.__telegram.sendMessageTelegram(telegram_bot_token, telegram_chat_id, message_telegram)
						self.__messages.createLogByTelegramCode(response_http_code)
						self.__dialog.createMessageDialog("\nSnapshot mounted: " + option_mount_snapshot, 7, 50, "Notification Message")
				else:
					self.__dialog.createMessageDialog("\nNo snapshots found in the repository.", 7, 50, "Notification Message")
			else:
				self.__dialog.createMessageDialog("\nNo repositories found.", 7, 50, "Notification Message")
			conn_es.transport.close()
		except Exception as exception:
			self.__dialog.createMessageDialog("\nFailed to mount snapshot. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__mounSearchableSnapshot", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		finally:
			self.__action_to_cancel()