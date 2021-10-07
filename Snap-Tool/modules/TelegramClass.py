from time import strftime
from datetime import datetime
from pycurl import Curl, HTTP_CODE
from urllib.parse import urlencode
from modules.UtilsClass import Utils
from modules.LoggerClass import Logger

"""
Class that allows you to manage the sending of alerts
through Telegram.
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

	Return:
	HTTP code of the request to Telegram.
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
		return int(status_code)

	"""
	Method that generates the message that will be sent by Telegram.

	Parameters:
	self -- An instantiated object of the Telegram class.
	action -- Action performed.
	snapshot_name -- Name of the snapshot.

	Return: 
	message -- Character string with the formed message.
	"""
	def getTelegramMessage(self, action, snapshot_name):
		message = u'\u26A0\uFE0F' + " " + 'Snap-Tool' +  " " + u'\u26A0\uFE0F' + '\n\n' + u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n\n"
		if action == "create_snapshot":
			message += u'\u2611\uFE0F' + " Action: Snapshot creation started\n"
		if action == "end_snapshot":
			message += u'\u2611\uFE0F' + " Action: Snapshot creation completed\n"
		if action == "delete_snapshot":
			message += u'\u2611\uFE0F' + " Action: Snaphot removed\n"
		if action == "mount_snapshot":
			message += u'\u2611\uFE0F' + " Action: Snapshot mounted as searchable snapshot\n"
		if action == "delete_index":
			message += u'\u2611\uFE0F' + " Action: Index removed\n"
		message += u'\u2611\uFE0F' + " Snapshot name: " + snapshot_name +"\n"
		message += u'\u2611\uFE0F' + " Index name: " + snapshot_name + "\n"
		return message

	"""
	Method that creates the header of the message that will
	be sent to Telegram.

	Parameters:
	self -- An instantiated object of the Telegram class.

	Return:
	header -- Header of the message.
	"""
	def getHeaderMessage(self):
		header = u'\u26A0\uFE0F' + " " + 'Snap-Tool' +  " " + u'\u26A0\uFE0F' + '\n\n' + u'\u23F0' + " Alert sent: " + strftime("%c") + "\n\n\n"
		return header

	"""
	Method that generates the message in Telegram for when a
	snapshot is deleted.

	Parameters:
	self -- An instantiated object of the Telegram class.
	snapshot_name -- Name of the snapshot.

	Return:
	message -- Message to send.
	"""
	def getMessageDeleteSnapshot(self, snapshot_name):
		message = self.getHeaderMessage()
		message += u'\u2611\uFE0F' + " Action: Snaphot removed\n"
		message += u'\u2611\uFE0F' + " Snapshot name: " + snapshot_name +"\n"
		message += u'\u2611\uFE0F' + " Index name: " + snapshot_name + "\n"
		return message

	"""
	Method that generates the message when the snapshot has finished being created.

	Parameters:
	self -- An instantiated object of the Telegram class.
	start_time -- Snapshot creation start time.
	end_time -- Snapshot creation end time.

	Return: 
	message -- Character string with the formed message.
	"""
	def getMessageEndSnapshot(self, start_time, end_time):
		message = u'\u2611\uFE0F' + " Start time: " + str(start_time) + "\n"
		message += u'\u2611\uFE0F' + " End time: " + str(end_time)
		return message
	
	"""
	Method that prints the status of the alert delivery based
	on the response HTTP code.

	Parameters:
	self -- An instantiated object of the Telegram class.
	telegram_code -- HTTP code in response to the request made
					 to Telegram.
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