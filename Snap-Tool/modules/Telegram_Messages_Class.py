from time import strftime
from libPyLog import libPyLog
from .Constants_Class import Constants

"""
Class that manages the messages that are sent via Telegram.
"""
class TelegramMessages:

	def __init__(self):
		"""
		Class constructor.
		"""
		self.__logger = libPyLog()
		self.__constants = Constants()


	def indexRemovedMessage(self, index_name):
		"""
		Method that generates the message to be sent when an index is deleted.

		Returns the message to send.
		
		:arg index_name (string): Index name.
		"""
		message_telegram = u'\u26A0\uFE0F' + " " + "Snap-Tool" +  " " + u'\u26A0\uFE0F' + "\n\n" + u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n\n"
		message_telegram += u'\u2611\uFE0F' + " Action: Index removed\n"
		message_telegram += u'\u2611\uFE0F' + " Index Name: " + index_name
		return message_telegram


	def createSnapshotMessage(self, repository_name, index_name):
		"""
		Method that generates the message to send when the creation of a snapshot starts.

		Returns the message to send.
		
		:arg repository_name (string): Repository name.
		:arg index_name (string): Index name.
		"""
		message_telegram = u'\u26A0\uFE0F' + " Snap-Tool " + u'\u26A0\uFE0F' + "\n\n" + u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n\n"
		message_telegram += u'\u2611\uFE0F' + " Action: Snapshot creation has started\n"
		message_telegram += u'\u2611\uFE0F' + " Snapshot Name: " + index_name + '\n'
		message_telegram += u'\u2611\uFE0F' + " Index Name: " + index_name + '\n'
		message_telegram += u'\u2611\uFE0F' + " Repository Name: " + repository_name
		return message_telegram


	def endSnapshotMessage(self, repository_name, snapshot_name, start_time, end_time):
		"""
		Method that generates the message to be sent when the creation of a snapshot is finished.

		Returns the message to send.
		
		:arg repository_name (string): Repository name.
		:arg index_name (string): Index name.
		:arg start_time (string): Date the snapshot creation started.
		:arg end_time (string): Date the snapshot creation ended.
		"""
		message_telegram = u'\u26A0\uFE0F' + " Snap-Tool " + u'\u26A0\uFE0F' + "\n\n" + u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n\n"
		message_telegram += u'\u2611\uFE0F' + " Action: Snapshot creation completed\n"
		message_telegram += u'\u2611\uFE0F' + " Snapshot Name: " + snapshot_name + '\n'
		message_telegram += u'\u2611\uFE0F' + " Repository Name: " + repository_name + '\n'
		message_telegram += u'\u2611\uFE0F' + " Start Time: " + str(start_time) + '\n'
		message_telegram += u'\u2611\uFE0F' + " End Time: " + str(end_time)
		return message_telegram


	def snapshotRestoredMessage(self, repository_name, snapshot_name):
		"""
		Method that generates the message to send when a snapshot is restored.

		Returns the message to send.
		
		:arg repository_name (string): Repository name.
		:arg snapshot_name (string): Snapshot name.
		"""
		message_telegram = u'\u26A0\uFE0F' + " Snap-Tool " + u'\u26A0\uFE0F' + "\n\n" + u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n\n"
		message_telegram += u'\u2611\uFE0F' + " Action: Snapshot restore\n"
		message_telegram += u'\u2611\uFE0F' + " Snapshot Name: " + snapshot_name + '\n'
		message_telegram += u'\u2611\uFE0F' + " Repository Name: " + repository_name
		return message_telegram


	def mountSearchableSnapshotMessage(self, repository_name, snapshot_name):
		"""
		Method that generates the message to send when a snapshot is mounted as a searchable snapshot.

		Returns the message to send.
		
		:arg repository_name (string): Repository name.
		:arg snapshot_name (string): Snapshot name.
		"""
		message_telegram = u'\u26A0\uFE0F' + " Snap-Tool " + u'\u26A0\uFE0F' + "\n\n" + u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n\n"
		message_telegram += u'\u2611\uFE0F' + " Action: Snapshot mounted as a searchable snapshot\n"
		message_telegram += u'\u2611\uFE0F' + " Snapshot Name: " + snapshot_name + '\n'
		message_telegram += u'\u2611\uFE0F' + " Repository Name: " + repository_name
		return message_telegram


	def snapshotRemovedMessage(self, repository_name, snapshot_name):
		"""
		Method that generates the message to send when a snapshot is deleted.

		Returns the message to send.
		
		:arg repository_name (string): Repository name.
		:arg snapshot_name (string): Snapshot name.
		"""
		message_telegram = u'\u26A0\uFE0F' + " Snap-Tool " + u'\u26A0\uFE0F' + "\n\n" + u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n\n"
		message_telegram += u'\u2611\uFE0F' + " Action: Snaphot removed\n"
		message_telegram += u'\u2611\uFE0F' + " Snapshot Name: " + snapshot_name + '\n'
		message_telegram += u'\u2611\uFE0F' + " Repository Name: " + repository_name
		return message_telegram


	def createLogByTelegramCode(self, response_http_code):
		"""
		Method that creates a log based on the received HTTP code.
		
		:arg response_http_code (integer): HTTP response code.
		"""
		if response_http_code == 200:
			self.__logger.generateApplicationLog("Telegram message sent.", 1, "__sendTelegramMessage", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		elif response_http_code == 400:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Bad request.", 3, "__sendTelegramMessage", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		elif response_http_code == 401:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Unauthorized.", 3, "__sendTelegramMessage", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		elif response_http_code == 404:
			self.__logger.generateApplicationLog("Telegram message not sent. Status: Not found.", 3, "__sendTelegramMessage", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)