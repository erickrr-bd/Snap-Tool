from time import strftime
from datetime import datetime
from pycurl import Curl, HTTP_CODE
from urllib.parse import urlencode
from modules.UtilsClass import Utils
from modules.LoggerClass import Logger

"""
Class that allows you to manage the sending of alerts through Telegram.
"""
class Telegram:
	"""
	Property that stores an object of type Utils.
	"""
	utils = None

	"""
	Property that stores an object of type Logger.
	"""
	logger = None

	"""
	Constructor for the Telegram class.

	Parameters:
	self -- An instantiated object of the Telegram class.
	form_dialog -- FormDialog class object.
	"""
	def __init__(self, form_dialog):
		self.logger = Logger()
		self.utils = Utils(form_dialog)

	"""
	Method that sends the alert to the telegram channel.

	Parameters:
	self -- Instance object.
	telegram_chat_id -- Telegram channel identifier to which the letter will be sent.
	telegram_bot_token -- Token of the Telegram bot that is the administrator of the Telegram channel to which the alerts will be sent.
	message -- Message to be sent to the Telegram channel.
	"""
	def sendTelegramAlert(self, telegram_chat_id, telegram_bot_token, message):
		if len(message) > 4096:
			message = "The size of the message in Telegram (4096) has been exceeded. Overall size: " + str(len(message))
		c = Curl()
		url = 'https://api.telegram.org/bot' + str(telegram_bot_token) + '/sendMessage'
		c.setopt(c.URL, url)
		data = { 'chat_id' : telegram_chat_id, 'text' : message }
		pf = urlencode(data)
		c.setopt(c.POSTFIELDS, pf)
		c.perform_rs()
		status_code = c.getinfo(HTTP_CODE)
		c.close()
		self.getStatusByTelegramCode(status_code)

	"""
	Method that creates the header of the message that will be sent to Telegram.

	Parameters:
	self -- An instantiated object of the Telegram class.

	Return:
	header -- Header of the message.
	"""
	def getHeaderMessage(self):
		header = u'\u26A0\uFE0F' + " " + 'Snap-Tool' +  " " + u'\u26A0\uFE0F' + "\n\n" + u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n\n"
		return header

	"""
	Method that generates the message in Telegram for when a repository is created.

	Parameters:
	self -- An instantiated object of the Telegram class.
	repository_name -- Name of the repository created.
	path_repository -- Path of the repository created.
	compress_repository -- Whether the repository will have compression or not.

	Return:
	message -- Message to send.
	"""
	def getMessageCreateRepository(self, repository_name, path_repository, compress_repository):
		message = self.getHeaderMessage()
		message += u'\u2611\uFE0F' + " Action: Repository created\n"
		message += u'\u2611\uFE0F' + " Repository name: " + repository_name + '\n'
		message += u'\u2611\uFE0F' + " Repository path: " + path_repository + '\n'
		message += u'\u2611\uFE0F' + " Repository compression: " + compress_repository
		return message

	"""
	Method that generates the message in Telegram for when a repository is deleted.

	Parameters:
	self -- An instantiated object of the Telegram class.
	repository_name -- Deleted repository name.

	Return:
	message -- Message to send.
	"""
	def getMessageDeleteRepository(self, repository_name):
		message = self.getHeaderMessage()
		message += u'\u2611\uFE0F' + " Action: Repository deleted\n"
		message += u'\u2611\uFE0F' + " Repository name: " + repository_name
		return message

	"""
	Method that generates the message in Telegram for when a snapshot is deleted.

	Parameters:
	self -- An instantiated object of the Telegram class.
	snapshot_name -- Name of the deleted snapshot.

	Return:
	message -- Message to send.
	"""
	def getMessageDeleteSnapshot(self, snapshot_name):
		message = self.getHeaderMessage()
		message += u'\u2611\uFE0F' + " Action: Snaphot removed\n"
		message += u'\u2611\uFE0F' + " Snapshot name: " + snapshot_name + '\n'
		message += u'\u2611\uFE0F' + " Index name: " + snapshot_name
		return message

	"""
	Method that generates the message in Telegram for when a snapshot is restored.

	Parameters:
	self -- An instantiated object of the Telegram class.
	repository_name -- Name of the repository where the snapshot to be restored is hosted.
	snapshot_name -- Name of the restored snapshot.

	Return:
	message -- Message to send.
	"""
	def getMessageRestoreSnapshot(self, repository_name, snapshot_name):
		message = self.getHeaderMessage()
		message += u'\u2611\uFE0F' + " Action: Snapshot restore\n"
		message += u'\u2611\uFE0F' + " Snapshot name: " + snapshot_name + '\n'
		message += u'\u2611\uFE0F' + " Repository name: " + repository_name
		return message

	"""
	Method that generates the message in Telegram for when a snapshot is mounted as a searchable snapshot.

	Parameters:
	self -- An instantiated object of the Telegram class.
	repository_name -- Name of the repository where the snapshot that will be mounted as a searchable snapshot is stored.
	snapshot_name -- Name of the snapshot to be mounted as a searchable snapshot.

	Return:
	message -- Message to send.
	"""
	def getMessageSearchableSnapshot(self, repository_name, snapshot_name):
		message = self.getHeaderMessage()
		message += u'\u2611\uFE0F' + " Action: Snapshot mounted as a searchable snapshot\n"
		message += u'\u2611\uFE0F' + " Snapshot name: " + snapshot_name + '\n'
		message += u'\u2611\uFE0F' + " Repository name: " + repository_name
		return message

	"""
	Method that generates the message in Telegram for when the creation of a snapshot has begun.

	Parameters:
	self -- An instantiated object of the Telegram class.
	index_name -- Name of the index that will be saved in the snapshot.
	repository_name -- Name of the repository where the snapshot will be saved.

	Return:
	message -- Message to send.
	"""
	def getMessageStartCreationSnapshot(self, index_name, repository_name):
		message = self.getHeaderMessage()
		message += u'\u2611\uFE0F' + " Action: Snapshot creation has started\n"
		message += u'\u2611\uFE0F' + " Snapshot name: " + index_name + '\n'
		message += u'\u2611\uFE0F' + " Index name: " + index_name + '\n'
		message += u'\u2611\uFE0F' + " Repository name: " + repository_name
		return message

	"""
	Method that generates the message in Telegram for when the creation of a snapshot has finished.

	Parameters:
	self -- An instantiated object of the Telegram class.
	snapshot_name -- Name of the snapshot created.
	repository_name -- Name of the repository where the snapshot was saved.
	start_time -- Time when snapshot creation started.
	end_time -- Time when snapshot creation finished.

	Return:
	message -- Message to send.
	"""
	def getMessageEndSnapshot(self, snapshot_name, repository_name, start_time, end_time):
		message = self.getHeaderMessage()
		message += u'\u2611\uFE0F' + " Action: Snapshot creation completed\n"
		message += u'\u2611\uFE0F' + " Snapshot name: " + snapshot_name + '\n'
		message += u'\u2611\uFE0F' + " Repository name: " + repository_name + '\n'
		message += u'\u2611\uFE0F' + " Start time: " + str(start_time) + '\n'
		message += u'\u2611\uFE0F' + " End time: " + str(end_time)
		return message

	"""
	Method that generates the message in Telegram for when an index is eliminated.

	Parameters:
	self -- An instantiated object of the Telegram class.
	index_name -- Index name removed.

	Return:
	message -- Message to send.
	"""
	def getMessageDeleteIndex(self, index_name):
		message = self.getHeaderMessage()
		message += u'\u2611\uFE0F' + " Action: Index removed\n"
		message += u'\u2611\uFE0F' + " Index name: " + index_name
		return message
	
	"""
	Method that prints the status of the alert delivery based on the response HTTP code.

	Parameters:
	self -- An instantiated object of the Telegram class.
	telegram_code -- HTTP code in response to the request made to Telegram.
	"""
	def getStatusByTelegramCode(self, telegram_code):
		if telegram_code == 200:
			self.logger.createSnapToolLog("Telegram message sent.", 1)
		elif telegram_code == 400:
			self.logger.createSnapToolLog("Telegram message not sent. Status: Bad request.", 3)
		elif telegram_code == 401:
			self.logger.createSnapToolLog("Telegram message not sent. Status: Unauthorized.", 3)
		elif telegram_code == 404:
			self.logger.createSnapToolLog("Telegram message not sent. Status: Not found.", 3)