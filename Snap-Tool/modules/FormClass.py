from sys import exit
from os import path
from time import sleep
from pathlib import Path
from dialog import Dialog
from re import compile as re_compile
from modules.UtilsClass import Utils
from modules.ElasticClass import Elastic
from modules.TelegramClass import Telegram
from modules.ConfigurationClass import Configuration

"""
"""
class FormDialog:
	"""
	Property that stores an object of type Dialog.
	"""
	d = None

	"""
	Property that stores an object of type Utils.
	"""
	utils = None

	"""
	Property that stores an object of type Elastic.
	"""
	elastic = None

	telegram = None

	path_conf_file = None

	"""
	Constructor for the FormDialog class.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def __init__(self):
		self.d = Dialog(dialog = "dialog")
		self.utils = Utils(self)
		self.elastic = Elastic(self)
		self.telegram = Telegram(self)
		self.d.set_background_title("SNAP-TOOL")
		self.path_conf_file = self.utils.getPathSnapTool("conf") + "/snap_tool_conf.yaml"

	"""
	Method that generates the menu interface.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	options -- List of options that make up the menu.
	title -- Title displayed on the interface.

	Return:
	tag_menu -- Chosen option.
	"""
	def getMenu(self, text, options, title):
		code_menu, tag_menu = self.d.menu(text = text,
										  choices = options,
										  title = title)
		if code_menu == self.d.OK:
			return tag_menu
		if code_menu == self.d.CANCEL:
			exit(0)

	"""
	Method that generates the interface for entering decimal
	or floating type data.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_inputbox -- Decimal or float value entered.
	"""
	def getDataNumberDecimal(self, text, initial_value):
		decimal_reg_exp = re_compile(r'^[1-9](\.[0-9]+)?$')
		while True:
			code_inputbox, tag_inputbox = self.d.inputbox(text = text,
											  			  height = 10,
											  			  width = 50,
											  			  init = initial_value)
			if code_inputbox == self.d.OK:
				if(not self.utils.validateRegularExpression(decimal_reg_exp, tag_inputbox)):
					self.d.msgbox("\nInvalid data entered. Required value (decimal or float).", 8, 50, title = "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to enter an IP
	address.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_inputbox -- IP address entered.
	"""
	def getDataIP(self, text, initial_value):
		ip_reg_exp = re_compile(r'^(?:(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$|^localhost$')
		while True:
			code_inputbox, tag_inputbox = self.d.inputbox(text = text,
														  height = 10,
														  width = 50,
														  init = initial_value)
			if code_inputbox == self.d.OK:
				if(not self.utils.validateRegularExpression(ip_reg_exp, tag_inputbox)):
					self.d.msgbox("\nInvalid data entered. Required value (IP address).", 8, 50, title = "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to enter a port.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_inputbox -- Port entered.
	"""
	def getDataPort(self, text, initial_value):
		port_reg_exp = re_compile(r'^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')
		while True:
			code_inputbox, tag_inputbox = self.d.inputbox(text = text,
														  height = 10,
														  width = 50,
														  init = initial_value)
			if code_inputbox == self.d.OK:
				if(not self.utils.validateRegularExpression(port_reg_exp, tag_inputbox)):
					self.d.msgbox("\nInvalid data entered. Required value (0 - 65535).", 8, 50, title = "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to enter text.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_inputbox -- Text entered.
	"""
	def getDataInputText(self, text, initial_value):
		while True:
			code_inputbox, tag_inputbox = self.d.inputbox(text = text,
														  height = 10,
														  width = 50,
														  init = initial_value)
			if code_inputbox == self.d.OK:
				if tag_inputbox == "":
					self.d.msgbox("\nInvalid data entered. Required value (not empty).", 8, 50, title = "Error Message")
				else:
					return tag_inputbox
			elif code_inputbox == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to enter a password.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	initial_value -- Default value shown on the interface.

	Return:
	tag_passwordbox -- Password entered.
	"""
	def getDataPassword(self, text, initial_value):
		while True:
			code_passwordbox, tag_passwordbox = self.d.passwordbox(text = text,
																   height = 10,
																   width = 50,
																   init = initial_value,
																   insecure = True)
			if code_passwordbox == self.d.OK:
				if tag_passwordbox == "":
					self.d.msgbox("\nInvalid data entered. Required value (not empty).", 8, 50, title = "Error Message")
				else:
					return tag_passwordbox
			elif code_passwordbox == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates a decision-making interface
	(yes / no).

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	title -- Title displayed on the interface.

	Return:
	tag_yesno -- Chosen option (yes or no).
	"""
	def getDataYesOrNo(self, text, title):
		tag_yesno = self.d.yesno(text = text,
								 height = 10,
								 width = 50,
								 title = title)
		return tag_yesno

	"""
	Method that generates an interface with several
	available options, and where only one of them can be
	chosen.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	options -- List of options that make up the interface.
	title -- Title displayed on the interface.

	Return:
	tag_radiolist -- Chosen option.
	"""
	def getDataRadioList(self, text, options, title):
		while True:
			code_radiolist, tag_radiolist = self.d.radiolist(text = text,
					  										 width = 65,
					  										 choices = options,
					  										 title = title)
			if code_radiolist == self.d.OK:
				if len(tag_radiolist) == 0:
					self.d.msgbox("\nSelect at least one option.", 7, 50, title = "Error Message")
				else:
					return tag_radiolist
			elif code_radiolist == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface with several
	available options, and where you can choose one or more
	of them.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	options -- List of options that make up the interface.
	title -- Title displayed on the interface.

	Return:
	tag_checklist -- List with the chosen options.
	"""
	def getDataCheckList(self, text, options, title):
		while True:
			code_checklist, tag_checklist = self.d.checklist(text = text,
					 										 width = 75,
					 										 choices = options,
					 										 title = title)
			if code_checklist == self.d.OK:
				if len(tag_checklist) == 0:
					self.d.msgbox("\nSelect at least one option.", 7, 50, title = "Error Message")
				else:
					return tag_checklist
			elif code_checklist == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates an interface to select a file.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	initial_path -- Initial path in the interface.
	title -- Title displayed on the interface.

	Return:
	tag_fselect -- Path of the selected file.
	"""
	def getFile(self, initial_path, title):
		while True:
			code_fselect, tag_fselect = self.d.fselect(filepath = initial_path,
													   height = 8,
													   width = 50,
													   title = title)
			if code_fselect == self.d.OK:
				if tag_fselect == "":
					self.d.msgbox("\nSelect a file. Required value (PEM file).", 7, 50, title = "Error Message")
				else:
					ext_file = Path(tag_fselect).suffix
					if not ext_file == ".pem":
						self.d.msgbox("\nSelect a file. Required value (PEM file).", 7, 50, title = "Error Message")
					else:
						return tag_fselect
			elif code_fselect == self.d.CANCEL:
				self.mainMenu()
				
	"""
	Method that generates an interface with scroll box.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text displayed on the interface.
	title -- Title displayed on the interface.
	"""
	def getScrollBox(self, text, title):
		code_scrollbox = self.d.scrollbox(text = text,
										  height = 15,
										  width = 70,
										  title = title)
		if code_scrollbox == self.d.OK:
			self.mainMenu()

	"""
	Method that defines the action to be performed on the
	Snap-Tool configuration file (creation or modification).

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def defineConfiguration(self):
		configuration = Configuration(self)

		options_conf_false = [("Create", "Create the configuration file", 0)]

		options_conf_true = [("Modify", "Modify the configuration file", 0)]

		if not path.exists(self.path_conf_file):
			opt_conf_false = self.getDataRadioList("Select a option:", options_conf_false, "Configuration Options")
			if opt_conf_false == "Create":
				configuration.createConfiguration()
		else:
			opt_conf_true = self.getDataRadioList("Select a option:", options_conf_true, "Configuration Options")
			if opt_conf_true == "Modify":
				configuration.updateConfiguration()

	def createRepository(self):
		print("Hola")

	"""
	Method that creates a snapshot of a particular index and
	allows the index to be deleted or not.

	Parameters:
	self -- An instantiated object of the FormDialog class.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised
				when you try to access a key that isn’t in a
				dictionary (dict). 
	"""
	def createSnapshot(self):
		try:
			if not path.exists(self.path_conf_file):
				self.d.msgbox("\nConfiguration file not found.", 7, 50, title = "Error Message")
			else:
				snap_tool_conf = self.utils.readYamlFile(self.path_conf_file, 'r')
				conn_es = self.elastic.getConnectionElastic()
				list_aux_indices = self.elastic.getIndices(conn_es)
				list_all_indices = self.utils.convertListToCheckOrRadioList(list_aux_indices)
				opt_index = self.getDataRadioList("Select a option:", list_all_indices, "Indices")
				list_aux_repositories = self.elastic.getAllRepositories(conn_es)
				list_all_repositories = self.utils.convertListToCheckOrRadioList(list_aux_repositories)
				opt_repo = self.getDataRadioList("Select a option:", list_all_repositories, "Repositories")
				self.elastic.createSnapshot(conn_es, opt_repo, opt_index)
				while True:
					status_snapshot = self.elastic.getStatusSnapshot(conn_es, opt_repo, opt_index)
					if status_snapshot == "SUCCESS":
						break
					sleep(60)
				self.d.msgbox("\nSnapshot created: " + opt_index, 7, 50, title = "Notification Message")
				if snap_tool_conf['is_delete_index'] == True:
					self.elastic.deleteIndex(conn_es, opt_index)
					if not conn_es.indices.exists(opt_index):
						self.d.msgbox("\nIndex removed: " + opt_index, 7, 50, title = "Notification Message")
				else:
					delete_index = self.getDataYesOrNo("\nDo you want to delete the index?\n\n- " + opt_index, "Delete Index")
					if delete_index == "ok":
						self.elastic.deleteIndex(conn_es, opt_index)
						if not conn_es.indices.exists(opt_index):
							self.d.msgbox("\nIndex removed: " + opt_index, 7, 50, title = "Notification Message")
				conn_es.transport.close()
			self.mainMenu()
		except KeyError as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.d.msgbox("\nFailed to create snapshot. For more information, see the logs.", 8, 50, title = "Error Message")
			self.mainMenu()

	"""
	Method that removes one or more snapshots from
	ElasticSearch.

	Parameters:
	self -- An instantiated object of the FormDialog class.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised
				when you try to access a key that isn’t in a
				dictionary (dict). 
	"""
	def deleteSnapshot(self):
		try:
			if not path.exists(self.path_conf_file):
				self.d.msgbox("\nConfiguration file not found.", 7, 50, title = "Error Message")
			else:
				snap_tool_conf = self.utils.readYamlFile(self.path_conf_file, 'r')
				conn_es = self.elastic.getConnectionElastic()
				list_aux_repositories = self.elastic.getAllRepositories(conn_es)
				if len(list_aux_repositories) == 0:
					self.d.msgbox("\nThere are no repositories created.", 7, 50, title = "Notification Message")
				else:
					list_all_repositories = self.utils.convertListToCheckOrRadioList(list_aux_repositories, "Repository Name")
					opt_repo = self.getDataRadioList("Select a option:", list_all_repositories, "Repositories")
					list_aux_snapshots = self.elastic.getAllSnapshots(conn_es, opt_repo)
					if len(list_aux_snapshots) == 0:
						self.d.msgbox("\nThere are no snapshots created.", 7, 50, title = "Notification Message")
					else:
						list_all_snapshots = self.utils.convertListToCheckOrRadioList(list_aux_snapshots, "Snapshot Name")
						opt_snapshots = self.getDataCheckList("Select one or more options:", list_all_snapshots, "Snapshots")
						delete_snapshot = self.getDataYesOrNo("\nAre you sure to delete the selected snapshot(s)?", "Delete Snapshot(s)")
						if delete_snapshot == "ok":
							for snapshot in opt_snapshots:
								self.elastic.deleteSnapshotElastic(conn_es, opt_repo, snapshot)
								message_telegram = self.telegram.getMessageDeleteSnapshot(snapshot)
								self.telegram.sendTelegramAlert(self.utils.decryptAES(snap_tool_conf['telegram_chat_id']).decode('utf-8'), self.utils.decryptAES(snap_tool_conf['telegram_bot_token']).decode('utf-8'), message_telegram)
							message = "\nThe following snapshots were removed:\n\n"
							message += self.utils.convertListToString(opt_snapshots)
							self.getScrollBox(message, "Snapshot(s) deleted")
				conn_es.transport.close()
		except KeyError as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.d.msgbox("\nFailed to delete snapshot(s). For more information, see the logs.", 8, 50, title = "Error Message")
			self.mainMenu()

	"""
	Method that displays information related to the percentage
	of occupied disk space of the nodes of the elasticsearch
	cluster.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def showNodesDiskSpace(self):
		message = "Occupied space in nodes:\n\n"
		conn_es = self.elastic.getConnectionElastic()
		nodes_info = self.elastic.getNodesInformation(conn_es)
		for node in nodes_info:
				message += "- " + nodes_info[node]['name'] + "\n"
				total_disk = nodes_info[node]['fs']['total']['total_in_bytes']
				available_disk = nodes_info[node]['fs']['total']['available_in_bytes']
				percentage = 100 - (available_disk * 100 / total_disk)
				message += "Percent occupied on disk: " + str(round(percentage, 2)) + "%\n\n"
		conn_es.transport.close()
		self.getScrollBox(message, "Node Information")

	"""
	Method that displays a message on the screen with
	information about the application.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def getAbout(self):
		message = "\nCopyright@2021 Tekium. All rights reserved.\nSnap-Tool v3.1\nAuthor: Erick Rodriguez\nEmail: erodriguez@tekium.mx, erickrr.tbd93@gmail.com\n" + "License: GPLv3\n\nSnap-Tool is a tool that allows the management of snaphots in\nElasticSearch through a graphical interface."
		self.getScrollBox(message, "About")

	"""
	Method that launches an action based on the option chosen
	in the main menu.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	option -- Chosen option.
	"""
	def switchMmenu(self, option):
		if option == 1:
			self.defineConfiguration()
		elif option == 2:
			self.createRepository()
		elif option == 3:
			self.createSnapshot()
		elif option == 4:
			self.deleteSnapshot()
		"""
		if option == 4:
			self.getCreateSearchSnapshot()
		if option == 5:
			self.getAbout()"""
		if option == 7:
			self.showNodesDiskSpace()
		elif option == 8:
			self.getAbout()
		elif option == 9:
			exit(0)

	"""
	Method that defines the menu on the actions to be carried
	out in the main menu.

	Parameters:
	self -- An instantiated object of the FormDialog class.
	"""
	def mainMenu(self):
		options_mm = [("1", "Snap-Tool Configuration"),
					  ("2", "Create repository"),
					  ("3", "Create Snapshot"),
					  ("4", "Delete Snapshot"),
					  ("5", "Delete indexes"),
					  ("6", "Create Searchable Snapshot"),
					  ("7", "Nodes information"),
					  ("8", "About"),
					  ("9", "Exit")]

		option_mm = self.getMenu("Select a option:", options_mm, "Main Menu")
		self.switchMmenu(int(option_mm))