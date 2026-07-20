"""
Class that manages everything related to Telegram's Messages.
"""
from time import strftime
from libPyLog import libPyLog
from .Constants_Class import Constants
from dataclasses import dataclass, field

@dataclass
class TelegramMessages:

	EMOJI_ALERT = "\u26A0\uFE0F"
	EMOJI_CLOCK = "\u23F0"	
	EMOJI_CHECK = "\u2611\uFE0F"

	logger: libPyLog = field(default_factory = libPyLog)
	constants: Constants = field(default_factory = Constants)


	def _base_message(self, action_text: str, details: list) -> str:
		"""
		Private helper method to avoid code duplication across all alerts

		Parameters:
			action_text (str): Action.
			details (list): Details or fields of the action.

		Returns:
			message(str) : Alert template that will be sent via Telegram.
		"""
		message = f"{self.EMOJI_ALERT} Snap-Tool {self.EMOJI_ALERT}\n\n{self.EMOJI_CLOCK} Alert sent: {strftime('%c')}\n\n"
		message += f"{self.EMOJI_CHECK} Action: {action_text}\n"
		for key, value in details:
			message += f"{self.EMOJI_CHECK} {key}: {value}\n"
		return message.strip()


	def generate_create_snapshot_message(self, index_name: str, repository_name: str) -> str:
		"""
		Method that generates the message to be sent via Telegram when a Snapshot's creation begins.

		Parameters:
			index_name (str): Index's name.
			repository_name (str): Repository's name.

		Returns:
			Message to be sent via Telegram.
		"""
		details = [("Snapshot Name", index_name), ("Index Name", index_name), ("Repository Name", repository_name)]
		return self._base_message("Snapshot creation has started", details)


	def generate_end_snapshot_message(self, snapshot_name: str, repository_name: str, start_time: str, end_time: str) -> str:
		"""
		Method that generates the message to be sent via Telegram when a Snapshot's creation ends.

		Parameters:
			snapshot_name (str): Snapshot's name.
			repository_name (str): Repository's name.
			start_time (str): Snapshot creation start date.
			end_time (str): End date of snapshot creation.

		Returns:
			Message to be sent via Telegram.
		"""
		details = [("Snapshot Name", snapshot_name), ("Repository Name", repository_name), ("Start Time", start_time), ("End Time", end_time)]
		return self._base_message("Snapshot creation completed", details)


	def generate_delete_snapshot_message(self, snapshot_name: str, repository_name: str) -> str:
		"""
		Method that generates the message to be sent via Telegram when a Snapshot is deleted.

		Parameters:
			snapshot_name (str): Snapshot's name.
			repository_name (str): Repository's name.

		Returns:
			Message to be sent via Telegram.
		"""
		details = [("Snapshot Name", snapshot_name), ("Repository Name", repository_name)]
		return self._base_message("Snapshot deleted", details)


	def generate_restore_snapshot_message(self, snapshot_name: str, repository_name: str) -> str:
		"""
		Method that generates the message to be sent via Telegram when a snapshot is restored.

		Parameters:
			snapshot_name (str): Snapshot's name.
			repository_name (str): Repository's name.

		Returns:
			Message to be sent via Telegram.
		"""
		details = [("Snapshot Name", snapshot_name), ("Repository Name", repository_name)]
		return self._base_message("Snapshot restored", details)


	def generate_mount_snapshot_message(self, snapshot_name: str, repository_name: str) -> str:
		"""
		Method that generates the message to be sent via Telegram when a snapshot is mounted as a searchable snapshot.

		Parameters:
			snapshot_name (str): Snapshot's name.
			repository_name (str): Repository's name.

		Returns:
			Message to be sent via Telegram.
		"""
		details = [("Snapshot Name", snapshot_name), ("Repository Name", repository_name), ("Index Name", snapshot_name)]
		return self._base_message("Snapshot mounted as a searchable snapshot", details)
	

	def generate_delete_index_message(self, index_name: str) -> str:
		"""
		Method that generates the message to be sent via Telegram when an index is deleted.

		Parameters:
			index_name (str): Index's name.

		Returns:
			Message to be sent via Telegram.
		"""
		details = [("Index Name", index_name)]
		return self._base_message("Index deleted", details)


	def generate_create_repository_message(self, repository_name: str, repository_path: str, compress_repository: bool) -> str:
		"""
		Method that generates the message to be sent via Telegram when a Repository's creation begins.

		Parameters:
			repository_name (str): Repository's name.
			repository_path (str): Repository's path.
			compress_repository (bool): Option that defines whether metadata files are stored compressed in the repository or not.

		Returns:
			Message to be sent via Telegram.
		"""
		details = [("Repository Name", repository_name), ("Repository Path", repository_path), ("Repository Compression", compress_repository)]
		return self._base_message("Repository Created", details)


	def generate_delete_repository_message(self, repository_name: str) -> str:
		"""
		Method that generates the message to be sent via Telegram when a repository is deleted.

		Parameters:
			repository_name (str): Repository's name.

		Returns:
			Message to be sent via Telegram.
		"""
		details = [("Repository Name", repository_name)]
		return self._base_message("Repository Deleted", details)


	def create_log_by_telegram_code(self, response_http_code: int) -> None:
		"""
		Method that generates an application log based on the HTTP response code of the Telegram API.

		Parameters:
			response_http_code (int): HTTP code returned by the Telegram API.
		"""
		match response_http_code:
			case 200:
				self.logger.create_log("Telegram message sent", 2, "_sendTelegramMessage", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 400:
				self.logger.create_log("Telegram message not sent. Bad request.", 4, "_sendTelegramMessage", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 401:
				self.logger.create_log("Telegram message not sent. Unauthorized.", 4, "_sendTelegramMessage", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
			case 404:
				self.logger.create_log("Telegram message not sent. Not found.", 4, "_sendTelegramMessage", use_file_handler = True, file_name = self.constants.LOG_FILE, user = self.constants.USER, group = self.constants.GROUP)
