import re
import os
import sys
from dialog import Dialog
from modules.UtilsClass import Utils
from modules.ElasticClass import Elastic
from modules.ConfigClass import Configuration

"""
Class that allows you to manage everything related to forms and data entry.
"""
class FormDialogs:
	"""
	Object of type Dialog.
	"""
	d = Dialog(dialog = "dialog")

	"""
	The title that will appear in the background of Telk-Alert-Tool is assigned.
	"""
	d.set_background_title("SNAP-TOOL")

	"""
	Property that contains the options for the graphical interface buttons.
	"""
	button_names = {d.OK:	  "OK",
					d.CANCEL: "Cancel",
					d.HELP:	  "Help",
					d.EXTRA:  "Extra"}

	"""
	Utils type object.
	"""
	utils = Utils()

	"""
	Configuration type object.
	"""
	configuration = Configuration()

	"""
	Elastic type object.
	"""
	elastic = Elastic()

	"""
	Property that contains the options when the configuration file is not created.
	"""
	options_conf_false = [("Create configuration", "Create the configuration file", 0)]

	"""
	Property that contains the options when the configuration file is created.
	"""
	options_conf_true = [("Modify configuration", "Modify the configuration file", 0)]

	"""
	Method that generates the menu interface.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	options -- List of options that make up the menu.
	title -- Title that will be given to the interface and that will be shown to the user.

	Return:
	tag_mm -- The option chosen by the user.
	"""
	def getMenu(self, options, title):
		code_mm, tag_mm = self.d.menu("Choose an option", choices=options,title=title)
		if code_mm == self.d.OK:
			return tag_mm
		if code_mm == self.d.CANCEL:
			sys.exit(0)

	"""
	Method that generates the interface with a list of options, where only one can be chosen.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	options -- List of options that make up the interface.
	title -- Title that will be given to the interface and that will be shown to the user.

	Return:
	tag_rl -- The option chosen by the user.
	"""
	def getDataRadioList(self, text, options, title):
		while True:
			code_rl, tag_rl = self.d.radiolist(
					  text,
					  width = 65,
					  choices = options,
					  title = title)
			if code_rl == self.d.OK:
				if len(tag_rl) == 0:
					self.d.msgbox("Select at least one option", 5, 50, title = "Error Message")
				else:
					return tag_rl
			if code_rl == self.d.CANCEL:
				self.mainMenu()

		"""
	Method that generates the interface with a list of options, where you can choose one or more.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	options -- List of options that make up the interface.
	title -- Title that will be given to the interface and that will be shown to the user.

	Return:
	tag_cl -- List with the chosen options.
	"""
	def getDataCheckList(self, text, options, title):
		while True:
			code_cl, tag_cl = self.d.checklist(
					 text,
					 width = 75,
					 choices = options,
					 title = title)
			if code_cl == self.d.OK:
				if len(tag_cl) == 0:
					self.d.msgbox("Select at least one option", 5, 50, title = "Error message")
				else:
					return tag_cl
			if code_cl == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates the interface for entering decimal or floating type data.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	initial_value -- Default value that will be shown to the user in the interface.

	Return:
	tag_nd -- Decimal value entered.
	"""
	def getDataNumberDecimal(self, text, initial_value):
		decimal_reg_exp = re.compile(r'^[1-9](\.[0-9]+)?$')
		while True:
			code_nd, tag_nd = self.d.inputbox(text, 10, 50, initial_value)
			if code_nd == self.d.OK:
				if(not self.utils.validateRegularExpression(decimal_reg_exp, tag_nd)):
					self.d.msgbox("Invalid value", 5, 50, title = "Error message")
				else:
					if(float(tag_nd) <= 7.0):
						self.d.msgbox("ElasticSearch version not supported", 5, 50, title = "Error message")
					else:
						return tag_nd
			if code_nd == self.d.CANCEL:
				self.mainMenu()
	"""
	Method that generates the interface for the entry of data of type IP address.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	initial_value -- Default value that will be shown to the user in the interface.

	Return:
	tag_ip -- IP address entered.
	"""
	def getDataIP(self, text, initial_value):
		ip_reg_exp = re.compile(r'^(?:(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(?:[1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$|^localhost$')
		while True:
			code_ip, tag_ip = self.d.inputbox(text, 10, 50, initial_value)
			if code_ip == self.d.OK:
				if(not self.utils.validateRegularExpression(ip_reg_exp, tag_ip)):
					self.d.msgbox("Invalid IP address", 5, 50, title = "Error message")
				else:
					return tag_ip
			if code_ip == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates the interface for entering data type communication port.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	initial_value -- Default value that will be shown to the user in the interface.

	Return:
	tag_port -- Port entered.
	"""
	def getDataPort(self, text, initial_value):
		port_reg_exp = re.compile(r'^([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$')
		while True:
			code_port, tag_port = self.d.inputbox(text, 10, 50, initial_value)
			if code_port == self.d.OK:
				if(not self.utils.validateRegularExpression(port_reg_exp, tag_port)):
					self.d.msgbox("Invalid port", 5 , 50, title = "Error message")
				else:
					return tag_port
		if code_port == self.d.CANCEL:
			self.mainMenu()

	"""
	Method that generates the interface for entering questioning type data with two possible yes or no values.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	title -- Title that will be given to the interface and that will be shown to the user.

	Return:
	tag_yesorno -- Chosen option (yes or no).
	"""
	def getDataYesOrNo(self, text, title):
		tag_yesorno = self.d.yesno(text, 10, 50, title = title)
		return tag_yesorno

	"""
	Method that generates the interface for entering text type data.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	initial_value -- Default value that will be shown to the user in the interface.

	Return:
	tag_input -- Text entered.
	"""
	def getDataInputText(self, text, initial_value):
		while True:
			code_input, tag_input = self.d.inputbox(text, 10, 50, initial_value)
			if code_input == self.d.OK:
				if tag_input == "":
					self.d.msgbox("The value cannot be empty", 5, 50, title = "Error message")
				else:
					return tag_input
			if code_input == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that generates the interface for entering password type data.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	text -- Text that will be shown to the user.
	initial_value -- Default value that will be shown to the user in the interface.

	Return:
	tag_pass -- Password entered.
	"""
	def getDataPassword(self, text, initial_value):
		while True:
			code_pass, tag_pass = self.d.passwordbox(text, 10, 50, initial_value, insecure = True)
			if code_pass == self.d.OK:
				if tag_pass == "":
					self.d.msgbox("Password cannot be empty", 5, 50, title = "Error message")
				else:
					return tag_pass
			if code_pass == self.d.CANCEL:
				self.mainMenu()

	"""
	Method that defines the action to be performed on the Snap-Tool configuration file (creation or modification).

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	"""
	def getDataConf(self):
		if not os.path.exists(self.utils.getPathSTool("conf") + "/es_conf.yaml"):
			opt_conf_false = self.getDataRadioList("Select a option", self.options_conf_false, "Configuration options")
			if opt_conf_false == "Create configuration":
				self.configuration.createConfiguration(FormDialogs())
		else:
			opt_conf_true = self.getDataRadioList("Select a option", self.options_conf_true, "Configuration options")
			if opt_conf_true == "Modify configuration":
				print("SI hay archivo")
				#self.create_conf.modifyConfiguration(FormDialogs())

	"""
	Method that obtains the list of indexes and select one of them to create a snapshot of it.

	Parameters:
	self -- An instantiated object of the FormDialogs class.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict).
	"""
	def getCreateSnapshot(self):
		snap_tool_conf = self.utils.readFileYaml(self.utils.getPathSTool('conf') + '/es_conf.yaml')
		conn_es = self.elastic.getConnectionElastic(snap_tool_conf, FormDialogs())
		list_indices = self.elastic.getIndices(conn_es)
		option_index = self.getDataRadioList("Select a option:", list_indices, "ElasticSearch Indexes")
		try:
			self.elastic.createSnapshot(conn_es, snap_tool_conf['repository_name'], option_index, FormDialogs())
			status_snapshot = self.elastic.getStatusSnapshot(conn_es, snap_tool_conf['repository_name'], option_index)
			if status_snapshot == 'SUCCESS':
				self.d.msgbox("\nSnapshot created", 7, 50, title = "Notification message")
				delete_index = self.getDataYesOrNo("\nDo you want to delete the index that was backed up in the snapshot?", "Delete Index")
				if delete_index == "ok":
					self.elastic.deleteIndex(conn_es, option_index)
					self.d.msgbox("\nThe index has been removed", 7, 50, title = "Notification message")
		except KeyError as exception:
			self.d.msgbox("\nKey Error: " + str(exception), 7, 50, title = "Error message")
			self.logger.createLogTool("Key Error: " + str(exception), 4)
			sys.exit(1)

	"""
	Method that lists all the snapshots created and allows one or more to be selected for deletion.

	Parameters:
	self -- An instantiated object of the FormDialogs class.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	"""
	def getDeleteSnapshot(self):
		snap_tool_conf = self.utils.readFileYaml(self.utils.getPathSTool('conf') + '/es_conf.yaml')
		conn_es = self.elastic.getConnectionElastic(snap_tool_conf, FormDialogs())
		try:
			list_snapshots = self.elastic.getSnapshots(conn_es, snap_tool_conf['repository_name'], FormDialogs())
			option_snapshot = self.getDataCheckList("Select a option:", list_snapshots, "ElasticSearch Snapshots")
			delete_snapshot = self.getDataYesOrNo("\nAre you sure to delete the selected snapshot (s)?\n\n- " + ",".join(option_snapshot), "Delete Snapshot")
			if delete_snapshot == "ok":
				for snapshot in option_snapshot:
					self.elastic.deleteSnapshot(conn_es, snap_tool_conf['repository_name'], snapshot, FormDialogs())
				self.d.msgbox("\nThe snapshot (s) have been deleted", 7, 50, title = "Notification message")
		except KeyError as exception:
			self.d.msgbox("\nKey Error: " + str(exception), 7, 50, title = "Error message")
			self.logger.createLogTool("Key Error: " + str(exception), 4)
			sys.exit(1)

	"""
	Method that launches an action based on the option chosen in the main menu.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	option -- Chosen option.
	"""
	def switchMmenu(self, option):
		if option == 1:
			self.getDataConf()
		if option == 2:
			self.getCreateSnapshot()
		if option == 3:
			self.getDeleteSnapshot()
		if option == 6:
			sys.exit(0)

	"""
	Method that defines the menu on the actions to be carried out in the main menu.

	Parameters:
	self -- An instantiated object of the FormDialogs class.
	"""
	def mainMenu(self):
		options_mm = [("1", "Snap-Tool Configuration"),
					  ("2", "Create Snapshot"),
					  ("3", "Delete Snapshot"),
					  ("4", "Create Searchable Snapshot"),
					  ("5", "About"),
					  ("6", "Exit")]

		option_mm = self.getMenu(options_mm, "Main Menu")
		self.switchMmenu(int(option_mm))