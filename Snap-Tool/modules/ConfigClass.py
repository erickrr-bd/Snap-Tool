import os
import yaml
from modules.UtilsClass import Utils
from modules.LoggerClass import Logger

"""
Class that manages everything related to the Snap-Tool configuration file.
"""
class Configuration:
	"""
	Utils type object.
	"""
	utils = Utils()

	"""
	Logger type object.
	"""
	logger = Logger()

	"""
	Method that requests the data for the creation of the Telk-Alert configuration file.

	Parameters:
	self -- An instantiated object of the Configuration class.
	form_dialog -- A FormDialogs class object.
	"""
	def createConfiguration(self, form_dialog):
		data_conf = []
		version_es = form_dialog.getDataNumberDecimal("Enter the ElasticSearch version:", "7.12")
		host_es = form_dialog.getDataIP("Enter the ElasticSearch IP address:", "localhost")
		port_es = form_dialog.getDataPort("Enter the ElasticSearch listening port:", "9200")
		use_ssl = form_dialog.getDataYesOrNo("\nDo you want Snap-Tool to connect to ElasticSearch using the SSL/TLS protocol?", "Connection Via SSL/TLS")
		data_conf.append(version_es)
		data_conf.append(host_es)
		data_conf.append(port_es)
		if use_ssl == "ok":
			data_conf.append(True)
			valid_certificates = form_dialog.getDataYesOrNo("\nDo you want the certificates for SSL/TLS communication to be validated?", "Certificate Validation")
			if valid_certificates == "ok":
				data_conf.append(True)
			else:
				data_conf.append(False)
		else:
			data_conf.append(False)
		http_auth = form_dialog.getDataYesOrNo("\nIs the use of HTTP authentication required to connect to ElasticSearch?", "HTTP Authentication")
		if http_auth == "ok":
			data_conf.append(True)
			user_http_auth = self.utils.encryptAES(form_dialog.getDataInputText("Enter the username for HTTP authentication:", "user_http"))
			pass_http_auth = self.utils.encryptAES(form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
			data_conf.append(user_http_auth)
			data_conf.append(pass_http_auth)
		else:
			data_conf.append(False)
		repository_name = form_dialog.getDataInputText("Enter the name of the repository where the created snapshots will be saved:", "my_repository")
		write_index = form_dialog.getDataInputText("Enter the name of the index that will be created in ElasticSearch:", "snaptool")
		telegram_bot_token = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram bot token:", "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"))
		telegram_chat_id = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram channel identifier:", "-1002365478941"))
		data_conf.append(repository_name)
		data_conf.append(write_index)
		data_conf.append(telegram_bot_token)
		data_conf.append(telegram_chat_id)
		self.createFileConfiguration(data_conf)
		if os.path.exists(self.utils.getPathSTool("conf") + "/es_conf.yaml"):
			form_dialog.d.msgbox("\nConfiguration file created", 7, 50, title = "Notification message")
			self.logger.createLogTool("Configuration file created", 2)
		else:
			form_dialog.d.msgbox("\nError creating configuration file", 7, 50, title = "Error message")
		form_dialog.mainMenu()

	"""
	Method that creates the YAML file with the data entered for the Telk-Alert configuration file.

	Parameters:
	self -- An instantiated object of the Configuration class.
	data_conf -- List containing all the data entered for the configuration file.
	
	Exceptions:
	OSError -- This exception is raised when a system function returns a system-related error, including I/O failures such as “file not found” or “disk full” (not for illegal argument types or other incidental errors).
	"""
	def createFileConfiguration(self, data_conf):
		d = {'es_version' : str(data_conf[0]),
			'es_host' : str(data_conf[1]),
			'es_port' : int(data_conf[2]),
			'use_ssl' : data_conf[3]}

		if data_conf[3] == True:
			valid_certificates_json = { 'valid_certificates' : data_conf[4] }
			last_index = 4
			d.update(valid_certificates_json)
		else:
			last_index = 3
		if data_conf[last_index + 1] == True:
			http_auth_json = { 'use_http_auth' : True, 'http_auth_user' : data_conf[last_index + 2].decode("utf-8"), 'http_auth_pass' : data_conf[last_index + 3].decode("utf-8") }
			data_aux_json = { 'repository_name' : str(data_conf[last_index + 4]), 'writeback_index' : str(data_conf[last_index + 5]), 'telegram_bot_token' : data_conf[last_index + 6].decode('utf-8'), 'telegram_chat_id' : data_conf[last_index + 7].decode('utf-8') }
			d.update(http_auth_json)
		else:
			data_aux_json = { 'use_http_auth' : False, 'repository_name' : str(data_conf[last_index + 2]), 'writeback_index' : str(data_conf[last_index + 3]), 'telegram_bot_token' : data_conf[last_index + 4].decode('utf-8'), 'telegram_chat_id' : data_conf[last_index + 5].decode('utf-8') }
		d.update(data_aux_json)
		try:
			with open(self.utils.getPathSTool('conf') + '/es_conf.yaml', 'w') as yaml_file:
				yaml.dump(d, yaml_file, default_flow_style = False)
		except OSError as exception:
			self.logger.createLogTool("Error" + str(exception), 4)