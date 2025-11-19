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


	def generate_create_snapshot_message(self, index_name: str, repository_name: str) -> str:
		"""
		Method that generates the message to be sent via Telegram when a Snapshot's creation begins.

		Parameters:
			index_name (str): Index's name.
			repository_name (str): Repository's name.

		Returns:
			telegram_message (str): Message to be sent via Telegram.
		"""
		telegram_message = f"{self.EMOJI_ALERT} Snap-Tool {self.EMOJI_ALERT}\n\n{self.EMOJI_CLOCK} Alert sent: {strftime("%c")}\n\n"
		telegram_message += f"{self.EMOJI_CHECK} Action: Snapshot creation has started\n"
		telegram_message += f"{self.EMOJI_CHECK} Snapshot Name: {index_name}\n"
		telegram_message += f"{self.EMOJI_CHECK} Index Name: {index_name}\n"
		telegram_message += f"{self.EMOJI_CHECK} Repository Name: {repository_name}"
		return telegram_message


	def generate_end_snapshot_message(self, snapshot_name: str, repository_name: str, start_time: str, end_time: str) -> str:
		"""
		Method that generates the message to be sent via Telegram when a Snapshot's creation ends.

		Parameters:
			snapshot_name (str): Snapshot's name.
			repository_name (str): Repository's name.
			start_time (str): Snapshot creation start date.
			end_time (str): End date of snapshot creation.

		Returns:
			telegram_message (str): Message to be sent via Telegram.
		"""
		telegram_message = f"{self.EMOJI_ALERT} Snap-Tool {self.EMOJI_ALERT}\n\n{self.EMOJI_CLOCK} Alert sent: {strftime("%c")}\n\n"
		telegram_message += f"{self.EMOJI_CHECK} Action: Snapshot creation completed\n"
		telegram_message += f"{self.EMOJI_CHECK} Snapshot Name: {snapshot_name}\n"
		telegram_message += f"{self.EMOJI_CHECK} Repository Name: {repository_name}\n"
		telegram_message += f"{self.EMOJI_CHECK} Start Time: {start_time}\n"
		telegram_message += f"{self.EMOJI_CHECK} End Time: {end_time}"
		return telegram_message


	def generate_delete_snapshot_message(self, snapshot_name: str, repository_name: str) -> str:
		"""
		Method that generates the message to be sent via Telegram when a Snapshot is deleted.

		Parameters:
			snapshot_name (str): Snapshot's name.
			repository_name (str): Repository's name.

		Returns:
			telegram_message (str): Message to be sent via Telegram.
		"""
		telegram_message = f"{self.EMOJI_ALERT} Snap-Tool {self.EMOJI_ALERT}\n\n{self.EMOJI_CLOCK} Alert sent: {strftime("%c")}\n\n"
		telegram_message += f"{self.EMOJI_CHECK} Action: Snapshot deleted\n"
		telegram_message += f"{self.EMOJI_CHECK} Snapshot Name: {snapshot_name}\n"
		telegram_message += f"{self.EMOJI_CHECK} Repository Name: {repository_name}"
		return telegram_message


	def generate_restore_snapshot_message(self, snapshot_name: str, repository_name: str) -> str:
		"""
		Method that generates the message to be sent via Telegram when a snapshot is restored.

		Parameters:
			snapshot_name (str): Snapshot's name.
			repository_name (str): Repository's name.

		Returns:
			telegram_message (str): Message to be sent via Telegram.
		"""
		telegram_message = f"{self.EMOJI_ALERT} Snap-Tool {self.EMOJI_ALERT}\n\n{self.EMOJI_CLOCK} Alert sent: {strftime("%c")}\n\n"
		telegram_message += f"{self.EMOJI_CHECK} Action: Snapshot restored\n"
		telegram_message += f"{self.EMOJI_CHECK} Snapshot Name: {snapshot_name}\n"
		telegram_message += f"{self.EMOJI_CHECK} Repository Name: {repository_name}"
		return telegram_message


	def generate_mount_snapshot_message(self, snapshot_name: str, repository_name: str) -> str:
		"""
		Method that generates the message to be sent via Telegram when a snapshot is mounted as a searchable snapshot.

		Parameters:
			snapshot_name (str): Snapshot's name.
			repository_name (str): Repository's name.

		Returns:
			telegram_message (str): Message to be sent via Telegram.
		"""
		telegram_message = f"{self.EMOJI_ALERT} Snap-Tool {self.EMOJI_ALERT}\n\n{self.EMOJI_CLOCK} Alert sent: {strftime("%c")}\n\n"
		telegram_message += f"{self.EMOJI_CHECK} Action: Snapshot mounted as a searchable snapshot\n"
		telegram_message += f"{self.EMOJI_CHECK} Snapshot Name: {snapshot_name}\n"
		telegram_message += f"{self.EMOJI_CHECK} Repository Name: {repository_name}\n"
		telegram_message += f"{self.EMOJI_CHECK} Index Name: {snapshot_name}"
		return telegram_message
	

	def generate_delete_index_message(self, index_name: str) -> str:
		"""
		Method that generates the message to be sent via Telegram when an index is deleted.

		Parameters:
			index_name (str): Index's name.

		Returns:
			telegram_message (str): Message to be sent via Telegram.
		"""
		telegram_message = f"{self.EMOJI_ALERT} Snap-Tool {self.EMOJI_ALERT}\n\n{self.EMOJI_CLOCK} Alert sent: {strftime("%c")}\n\n"
		telegram_message += f"{self.EMOJI_CHECK} Action: Index deleted\n"
		telegram_message += f"{self.EMOJI_CHECK} Index Name: {index_name}"
		return telegram_message


	def generate_create_repository_message(self, repository_name: str, repository_path: str, compress_repository: bool) -> str:
		"""
		Method that generates the message to be sent via Telegram when a Repository's creation begins.

		Parameters:
			repository_name (str): Repository's name.
			repository_path (str): Repository's path.
			compress_repository (bool): Option that defines whether metadata files are stored compressed in the repository or not.

		Returns:
			telegram_message (str): Message to be sent via Telegram.
		"""
		telegram_message = f"{self.EMOJI_ALERT} Snap-Tool {self.EMOJI_ALERT}\n\n{self.EMOJI_CLOCK} Alert sent: {strftime("%c")}\n\n"
		telegram_message += f"{self.EMOJI_CHECK} Action: Repository Created\n"
		telegram_message += f"{self.EMOJI_CHECK} Repository Name: {repository_name}\n"
		telegram_message += f"{self.EMOJI_CHECK} Repository Path: {repository_path}\n"
		telegram_message += f"{self.EMOJI_CHECK} Repository Compression: {compress_repository}"
		return telegram_message


	def generate_delete_repository_message(self, repository_name: str) -> str:
		"""
		Method that generates the message to be sent via Telegram when a repository is deleted.

		Parameters:
			repository_name (str): Repository's name.

		Returns:
			telegram_message (str): Message to be sent via Telegram.
		"""
		telegram_message = f"{self.EMOJI_ALERT} Snap-Tool {self.EMOJI_ALERT}\n\n{self.EMOJI_CLOCK} Alert sent: {strftime("%c")}\n\n"
		telegram_message += f"{self.EMOJI_CHECK} Action: Repository Deleted\n"
		telegram_message += f"{self.EMOJI_CHECK} Repository Name: {repository_name}"
		return telegram_message


	def create_log_by_telegram_code(self, response_http_code: int) -> None:
		"""
		Method that generates an application log based on the HTTP response code of the Telegram API.

		Parameters:
			response_http_code (int): HTTP code returned by the Telegram API.
		"""
		match response_http_code:
			case 200:
				self.logger.create_log("Telegram message sent", 2, "_sendTelegramMessage", use_file_handler = True, file_name = self.constants.LOG_FILE)
			case 400:
				self.logger.create_log("Telegram message not sent. Bad request.", 4, "_sendTelegramMessage", use_file_handler = True, file_name = self.constants.LOG_FILE)
			case 401:
				self.logger.create_log("Telegram message not sent. Unauthorized.", 4, "_sendTelegramMessage", use_file_handler = True, file_name = self.constants.LOG_FILE)
			case 404:
				self.logger.create_log("Telegram message not sent. Not found.", 4, "_sendTelegramMessage", use_file_handler = True, file_name = self.constants.LOG_FILE)
