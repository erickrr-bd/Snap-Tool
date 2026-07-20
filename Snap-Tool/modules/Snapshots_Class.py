"""
Class that manages everything related to Snapshots.
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

class Snapshots:

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


	def create_snapshot(self) -> None:
		"""
		Method that creates a snapshot.
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
			index_name = self.dialog.create_radiolist("Select a option:", 18, 70, tuple_to_rc, "Indexes")
			if not index_name:
				return
			repositories_list = self.elasticsearch.get_repositories(conn_es)
			if not repositories_list:
				self.dialog.create_message("\nNo repositories found.", 7, 50, "Notification Message")
				return
			tuple_to_rc = self.utils.convert_list_to_tuple_rc(repositories_list, "Repository Name")
			repository_name = self.dialog.create_radiolist("Select a option:", 18, 70, tuple_to_rc, "Repositories")
			if not repository_name:
				return
			wait_for_completion_yn = self.dialog.create_yes_or_no("\nIs it necessary to wait for the snapshot creation to finish?", 8, 50, "Wait for completion")
			telegram_message = self.telegram_messages.generate_create_snapshot_message(index_name, repository_name)
			response_http_code = self.telegram.send_telegram_message(telegram_bot_token, telegram_chat_id, telegram_message)
			self.telegram_messages.create_log_by_telegram_code(response_http_code)
			self.logger.create_log(f"Snapshot creation started: {index_name}", 2, "_createSnapshot", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			self.elasticsearch.create_snapshot(conn_es, index_name, repository_name, False)
			if wait_for_completion_yn:
				while True:
					snapshot_current_status = self.elasticsearch.get_snapshot_current_status(conn_es, index_name, repository_name)
					if snapshot_current_status == "SUCCESS":
						break
					elif snapshot_current_status in ["FAILED", "PARTIAL", "INCOMPATIBLE"]:
						raise RuntimeError(f"Elasticsearch snapshot status returned: {snapshot_current_status}")
					sleep(30)				
				snapshot_info = self.elasticsearch.get_snapshot_info(conn_es, index_name, repository_name)
				telegram_message = self.telegram_messages.generate_end_snapshot_message(index_name, repository_name, snapshot_info["snapshots"][0]["start_time"], snapshot_info["snapshots"][0]["end_time"])
				response_http_code = self.telegram.send_telegram_message(telegram_bot_token, telegram_chat_id, telegram_message)
				self.telegram_messages.create_log_by_telegram_code(response_http_code)
				self.logger.create_log(f"Snapshot created: {index_name}", 2, "_createSnapshot", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
				self.dialog.create_message(f"\nSnapshot created: {index_name}", 7, 50, "Notification Message")
		except Exception as exception:
			self.dialog.create_message("\nError creating snapshot. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_createSnapshot", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		finally:
			passphrase = None
			telegram_bot_token = None
			telegram_chat_id = None
			del passphrase
			del telegram_bot_token
			del telegram_chat_id
			if conn_es and hasattr(conn_es, 'transport') and conn_es.transport:
				conn_es.transport.close()


	def delete_snapshot(self) -> None:
		"""
		Method that deletes snapshot(s) from a repository.
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
			repositories_list = self.elasticsearch.get_repositories(conn_es)
			if not repositories_list:
				self.dialog.create_message("\nNo repositories found.", 7, 50, "Notification Message")
				return
			tuple_to_rc = self.utils.convert_list_to_tuple_rc(repositories_list, "Repository Name")
			repository_name = self.dialog.create_radiolist("Select a option:", 18, 70, tuple_to_rc, "Repositories")
			if not repository_name:
				return
			snapshots_list = self.elasticsearch.get_snapshots_by_repository(conn_es, repository_name)
			if not snapshots_list:
				self.dialog.create_message("\nNo snapshots found.", 7, 50, "Notification Message")
				return
			tuple_to_rc = self.utils.convert_list_to_tuple_rc(snapshots_list, "Snapshot Name")
			snapshots = self.dialog.create_checklist("Select one or more options:", 18, 70, tuple_to_rc, "Snapshots")
			if not snapshots:
				return
			text = self.utils.get_str_from_list(snapshots, "Selected Snapshot(s):")
			self.dialog.create_scrollbox(text, 15, 60, "Delete Snapshot(s)")
			delete_snapshot_yn = self.dialog.create_yes_or_no("\nAre you sure to remove the selected snapshots?\n\n**NOTE: This action cannot be undone.", 9, 50, "Delete Snapshot(s)")
			if delete_snapshot_yn:
				for snapshot_name in snapshots:
					self.elasticsearch.delete_snapshot(conn_es, snapshot_name, repository_name)
					self.logger.create_log(f"Snapshot deleted: {snapshot_name}", 3, "_deleteSnapshot", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
					telegram_message = self.telegram_messages.generate_delete_snapshot_message(snapshot_name, repository_name)
					response_http_code = self.telegram.send_telegram_message(telegram_bot_token, telegram_chat_id, telegram_message)
					self.telegram_messages.create_log_by_telegram_code(response_http_code)
				self.dialog.create_message("\nSnapshot(s) deleted.", 7, 50, "Notification Message")
		except Exception as exception:
			self.dialog.create_message("\nError deleting snapshot(s). For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_deleteSnapshot", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		finally:
			passphrase = None
			telegram_bot_token = None
			telegram_chat_id = None
			del passphrase
			del telegram_bot_token
			del telegram_chat_id
			if conn_es and hasattr(conn_es, 'transport') and conn_es.transport:
				conn_es.transport.close()


	def restore_snapshot(self) -> None:
		"""
		Method that restores a snapshot.
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
			repositories_list = self.elasticsearch.get_repositories(conn_es)
			if not repositories_list:
				self.dialog.create_message("\nNo repositories found.", 7, 50, "Notification Message")
				return
			tuple_to_rc = self.utils.convert_list_to_tuple_rc(repositories_list, "Repository Name")
			repository_name = self.dialog.create_radiolist("Select a option:", 18, 70, tuple_to_rc, "Repositories")
			if not repository_name:
				return
			snapshots_list = self.elasticsearch.get_snapshots_by_repository(conn_es, repository_name)
			if not snapshots_list:
				self.dialog.create_message("\nNo snapshots found.", 7, 50, "Notification Message")
				return
			tuple_to_rc = self.utils.convert_list_to_tuple_rc(snapshots_list, "Snapshot Name")
			snapshot_name = self.dialog.create_radiolist("Select a option:", 18, 70, tuple_to_rc, "Snapshots")
			if not snapshot_name:
				return
			restore_snapshot_yn = self.dialog.create_yes_or_no(f"\nAre you sure to restore the snapshot?", 7, 50, "Restore Snapshot")
			if restore_snapshot_yn:
				wait_for_completion_yn = self.dialog.create_yes_or_no("\nIs it required to wait for the restoration to finish?", 8, 50, "Wait for completion")
				if wait_for_completion_yn:
					self.elasticsearch.restore_snapshot(conn_es, snapshot_name, repository_name, True)
				else:
					self.elasticsearch.restore_snapshot(conn_es, snapshot_name, repository_name, False)
				self.logger.create_log(f"Snapshot restored: {snapshot_name}", 2, "_restoreSnapshot", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
				telegram_message = self.telegram_messages.generate_restore_snapshot_message(snapshot_name, repository_name)
				response_http_code = self.telegram.send_telegram_message(telegram_bot_token, telegram_chat_id, telegram_message)
				self.telegram_messages.create_log_by_telegram_code(response_http_code)
				self.dialog.create_message(f"\nSnapshot restored: {snapshot_name}", 7, 50, "Notification Message")
		except Exception as exception:
			self.dialog.create_message("\nError restoring a snapshot. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_restoreSnapshot", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		finally:
			passphrase = None
			telegram_bot_token = None
			telegram_chat_id = None
			del passphrase
			del telegram_bot_token
			del telegram_chat_id
			if conn_es and hasattr(conn_es, 'transport') and conn_es.transport:
				conn_es.transport.close()


	def mount_searchable_snapshot(self) -> None:
		"""
		Method that mounts a snapshot as a searchable snapshot.
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
			repositories_list = self.elasticsearch.get_repositories(conn_es)
			if not repositories_list:
				self.dialog.create_message("\nNo repositories found.", 7, 50, "Notification Message")
				return
			tuple_to_rc = self.utils.convert_list_to_tuple_rc(repositories_list, "Repository Name")
			repository_name = self.dialog.create_radiolist("Select a option:", 18, 70, tuple_to_rc, "Repositories")
			if not repository_name:
				return
			snapshots_list = self.elasticsearch.get_snapshots_by_repository(conn_es, repository_name)
			if not snapshots_list:
				self.dialog.create_message("\nNo snapshots found.", 7, 50, "Notification Message")
				return
			tuple_to_rc = self.utils.convert_list_to_tuple_rc(snapshots_list, "Snapshot Name")
			snapshot_name = self.dialog.create_radiolist("Select a option:", 18, 70, tuple_to_rc, "Snapshots")
			if not snapshot_name:
				return
			mount_snapshot_yn = self.dialog.create_yes_or_no(f"\nAre you sure to mount the snapshot as a searchable snapshot?", 8, 50, "Mount Snapshot as a searchable snapshot")
			if mount_snapshot_yn:
				wait_for_completion_yn = self.dialog.create_yes_or_no("\nIs it necessary to wait for the snapshot mount to finish?", 8, 50, "Wait for completion")
				if wait_for_completion_yn:
					self.elasticsearch.mount_searchable_snapshot(conn_es, snapshot_name, repository_name, True)
				else:
					self.elasticsearch.mount_searchable_snapshot(conn_es, snapshot_name, repository_name, False)
				self.logger.create_log(f"Snapshot mounted: {snapshot_name}", 2, "_mountSnapshot", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
				telegram_message = self.telegram_messages.generate_mount_snapshot_message(snapshot_name, repository_name)
				response_http_code = self.telegram.send_telegram_message(telegram_bot_token, telegram_chat_id, telegram_message)
				self.telegram_messages.create_log_by_telegram_code(response_http_code)
				self.dialog.create_message(f"\nSnapshot mounted: {snapshot_name}", 7, 50, "Notification Message")
		except Exception as exception:
			self.dialog.create_message("\nError mounting a snapshot as a searchable snapshot. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_mountSnapshot", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		finally:
			passphrase = None
			telegram_bot_token = None
			telegram_chat_id = None
			del passphrase
			del telegram_bot_token
			del telegram_chat_id
			if conn_es and hasattr(conn_es, 'transport') and conn_es.transport:
				conn_es.transport.close()


	def get_snapshot_status(self) -> None:
		"""
		Method that obtains the current status of all snapshots of a specific repository.
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
			repositories_list = self.elasticsearch.get_repositories(conn_es)
			if not repositories_list:
				self.dialog.create_message("\nNo repositories found.", 7, 50, "Notification Message")
				return
			tuple_to_rc = self.utils.convert_list_to_tuple_rc(repositories_list, "Repository Name")
			repository_name = self.dialog.create_radiolist("Select a option:", 18, 70, tuple_to_rc, "Repositories")
			if not repository_name:
				return
			snapshots_list = self.elasticsearch.get_snapshots_by_repository(conn_es, repository_name)
			if not snapshots_list:
				self.dialog.create_message("\nNo snapshots found.", 7, 50, "Notification Message")
				return
			text = f"Repository: {repository_name}\n\nSnapshots:\n"
			for snapshot_name in snapshots_list:
				snapshot_status = self.elasticsearch.get_snapshot_current_status(conn_es, snapshot_name, repository_name)
				text += f"- {snapshot_name}: {snapshot_status}\n"
			self.dialog.create_scrollbox(text, 16, 60, "Snapshots' Current Status")
		except Exception as exception:
			self.dialog.create_message("\nError getting snapshot's status. For more information, see the logs.", 8, 50, "Error Message")
			self.logger.create_log(exception, 4, "_getSnapshotStatus", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
		finally:
			passphrase = None
			telegram_bot_token = None
			telegram_chat_id = None
			del passphrase
			del telegram_bot_token
			del telegram_chat_id
			if conn_es and hasattr(conn_es, 'transport') and conn_es.transport:
				conn_es.transport.close()
