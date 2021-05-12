import os
import yaml
from modules.UtilsClass import Utils
from modules.LoggerClass import Logger

"""
Class that manages everything related to the Snap-Tool configuration file.
"""
class Configuration:
	"""
	Property that stores an object of type Utils.
	"""
	utils = None

	"""
	Property that stores an object of type Logger.
	"""
	logger = None

	"""
	Constructor for the Configuration class.

	Parameters:
	self -- An instantiated object of the Configuration class.
	"""
	def __init__(self):
		self.utils = Utils()
		self.logger = Logger()

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
				cert_file = form_dialog.getFileOrDirectory('/etc/Snap-Tool', "Select the CA certificate:")
				data_conf.append(cert_file)
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
		telegram_bot_token = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram bot token:", "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"))
		telegram_chat_id = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram channel identifier:", "-1002365478941"))
		data_conf.append(repository_name)
		data_conf.append(telegram_bot_token)
		data_conf.append(telegram_chat_id)
		self.createFileConfiguration(data_conf)
		if os.path.exists(self.utils.getPathSTool("conf") + "/es_conf.yaml"):
			form_dialog.d.msgbox("\nConfiguration file created", 7, 50, title = "Notification message")
			self.logger.createLogTool("Configuration file created", 2)
		else:
			form_dialog.d.msgbox("\nError creating configuration file. For more information, see the logs.", 7, 50, title = "Error message")
		form_dialog.mainMenu()
	
	"""
	Method that modifies one or more fields of the Snap-Tool configuration file.

	Parameters:
	self -- An instantiated object of the Configuration class.
	form_dialog -- A FormDialogs class object.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	"""
	def modifyConfiguration(self, form_dialog):
		options_conf_prop = [("Version", "ElasticSearch Version", 0),
							("Host", "ElasticSearch Host", 0),
							("Port", "ElasticSearch Port", 0),
							("Use SSL/TLS", "Enable or disable SSL/TLS connection", 0),
							("Use HTTP auth", "Enable or disable Http authentication", 0),
							("Repository name", "Snapshot repository", 0),
							("Bot token", "Telegram bot token", 0),
							("Chat ID", "Telegram chat ID", 0)]

		options_ssl_true = [("To disable", "Disable SSL/TLS communication", 0),
							("Modify", "Modify certificate validation", 0)]

		options_ssl_false = [("Enable", "Enable SSL/TLS communication", 0)]

		options_valid_cert_true = [("To disable", "Disable certificate validation", 0),
									("Modify", "Change certificate file", 0)]

		options_valid_cert_false = [("Enable", "Enable certificate validation", 0)]

		options_http_auth_true = [("To disable", "Disable HTTP Authentication", 0),
								 ("Modify data", "Modify HTTP Authentication data", 0)]

		options_http_auth_false = [("Enable", "Enable HTTP Authentication", 0)]

		options_http_auth_data = [("Username", "Username for HTTP Authentication", 0),
								 ("Password", "User password", 0)]

		flag_version = 0
		flag_host = 0
		flag_port = 0
		flag_use_ssl = 0
		flag_http_auth = 0
		flag_repository_name = 0
		flag_bot_token = 0
		flag_chat_id = 0
		opt_conf_prop = form_dialog.getDataCheckList("Select one or more options", options_conf_prop, "Update configuration file")
		for opt_prop in opt_conf_prop:
			if opt_prop == "Version":
				flag_version = 1
			if opt_prop == "Host":
				flag_host = 1
			if opt_prop == "Port":
				flag_port = 1
			if opt_prop == "Use SSL/TLS":
				flag_use_ssl = 1
			if opt_prop == "Validate certificates":
				flag_validate_cert = 1
			if opt_prop == "Use HTTP auth":
				flag_http_auth = 1
			if opt_prop == "Repository name":
				flag_repository_name = 1
			if opt_prop == "Bot token":
				flag_bot_token = 1
			if opt_prop == "Chat ID":
				flag_chat_id = 1
		try:
			with open(self.utils.getPathSTool('conf') + '/es_conf.yaml', "rU") as f:
				data_conf = yaml.safe_load(f)
			hash_origen = self.utils.getSha256File(self.utils.getPathSTool('conf') + '/es_conf.yaml')
			if flag_version == 1:
				version_es = form_dialog.getDataNumberDecimal("Enter the ElasticSearch version:", str(data_conf['es_version']))
				data_conf['es_version'] = str(version_es)
			if flag_host == 1:
				host_es = form_dialog.getDataIP("Enter the ElasticSearch IP address:", str(data_conf['es_host']))
				data_conf['es_host'] = str(host_es)
			if flag_port == 1:
				port_es = form_dialog.getDataPort("Enter the ElasticSearch listening port:", str(data_conf['es_port']))
				data_conf['es_port'] = int(port_es)
			if flag_use_ssl == 1:
				if data_conf['use_ssl'] == True:
					opt_ssl_true = form_dialog.getDataRadioList("Select a option:", options_ssl_true, "Connection via SSL/TLS")
					if opt_ssl_true == "To disable":
						del data_conf['valid_certificates']
						if 'path_cert' in data_conf:
							del data_conf['path_cert']
						data_conf['use_ssl'] = False
					if opt_ssl_true == "Modify":
						if data_conf['valid_certificates'] == True:
							opt_valid_cert_true = form_dialog.getDataRadioList("Select a option:", options_valid_cert_true, "Certificate Validation")
							if opt_valid_cert_true == "To disable":
								if 'path_cert' in data_conf:
									del data_conf['path_cert']
								data_conf['valid_certificates'] = False
							if opt_valid_cert_true == "Modify":
								cert_file = form_dialog.getFileOrDirectory(data_conf['path_cert'], "Select the CA certificate:")
								data_conf['path_cert'] = str(cert_file)
						else:
							opt_valid_cert_false = form_dialog.getDataRadioList("Select a option:", options_valid_cert_false, "Certificate Validation")
							if opt_valid_cert_false == "Enable":
								data_conf['valid_certificates'] = True
								cert_file = form_dialog.getFileOrDirectory('/etc/Snap-Tool', "Select the CA certificate:")
								cert_file_json = { 'path_cert' : str(cert_file) }
								data_conf.update(cert_file_json)
				else:
					opt_ssl_false = form_dialog.getDataRadioList("Select a option:", options_ssl_false, "Connection via SSL/TLS")
					if opt_ssl_false == "Enable":
						data_conf['use_ssl'] = True
						valid_certificates = form_dialog.getDataYesOrNo("\nDo you want the certificates for SSL/TLS communication to be validated?", "Certificate Validation")
						if valid_certificates == "ok":
							cert_file = form_dialog.getFileOrDirectory('/etc/Snap-Tool', "Select the CA certificate:")
							valid_certificates_json = { 'valid_certificates' : True, 'path_cert' : str(cert_file)}
						else:
							valid_certificates_json = { 'valid_certificates' : False }
						data_conf.update(valid_certificates_json)
			if flag_http_auth == 1:
				if data_conf['use_http_auth'] == True:
					opt_http_auth_true = form_dialog.getDataRadioList("Select a option:", options_http_auth_true, "HTTP Authentication")
					if opt_http_auth_true == "To disable":
						del(data_conf['http_auth_user'])
						del(data_conf['http_auth_pass'])
						data_conf['use_http_auth'] = False
					if opt_http_auth_true == "Modify data":
						flag_http_auth_user = 0
						flag_http_auth_pass = 0
						opt_mod_http_auth = form_dialog.getDataCheckList("Select one or more options:", options_http_auth_data, "HTTP Authentication")
						for opt_mod in opt_mod_http_auth:
							if opt_mod == "Username":
								flag_http_auth_user = 1
							if opt_mod == "Password":
								flag_http_auth_pass = 1
						if flag_http_auth_user == 1:
							user_http_auth_mod = self.utils.encryptAES(form_dialog.getDataInputText("Enter the username for HTTP authentication:", self.utils.decryptAES(data_conf['http_auth_user']).decode('utf-8')))
							data_conf['http_auth_user'] = user_http_auth_mod.decode('utf-8')
						if flag_http_auth_pass == 1:
							pass_http_auth_mod = self.utils.encryptAES(form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
							data_conf['http_auth_pass'] = pass_http_auth_mod.decode('utf-8')
				else:
					opt_http_auth_false = form_dialog.getDataRadioList("Select a option:", options_http_auth_false, "HTTP Authentication")
					if opt_http_auth_false == "Enable":
						user_http_auth = self.utils.encryptAES(form_dialog.getDataInputText("Enter the username for HTTP authentication:", "user_http"))
						pass_http_auth = self.utils.encryptAES(form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
						http_auth_data = {'http_auth_user': user_http_auth.decode('utf-8'), 'http_auth_pass': pass_http_auth.decode('utf-8')}
						data_conf.update(http_auth_data)
						data_conf['use_http_auth'] = True
			if flag_repository_name == 1:
				repository_name = form_dialog.getDataInputText("Enter the name of the repository where the created snapshots will be saved:", str(data_conf['repository_name']))
				data_conf['repository_name'] = str(repository_name)
			if flag_bot_token == 1:
				telegram_bot_token = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram bot token:", self.utils.decryptAES(data_conf['telegram_bot_token']).decode('utf-8')))
				data_conf['telegram_bot_token'] = telegram_bot_token.decode('utf-8')
			if flag_chat_id == 1:
				telegram_chat_id = self.utils.encryptAES(form_dialog.getDataInputText("Enter the Telegram channel identifier:", self.utils.decryptAES(data_conf['telegram_chat_id']).decode('utf-8')))
				data_conf['telegram_chat_id'] = telegram_chat_id.decode('utf-8')
			with open(self.utils.getPathSTool('conf') + '/es_conf.yaml', "w") as file_update:
				yaml.safe_dump(data_conf, file_update, default_flow_style = False)
			hash_modify = self.utils.getSha256File(self.utils.getPathSTool('conf') + '/es_conf.yaml')
			if hash_origen == hash_modify:
				form_dialog.d.msgbox("\nConfiguration file not modified", 7, 50, title = "Notification message")
			else:
				self.logger.createLogTool("Modified configuration file", 2)
				form_dialog.d.msgbox("\nModified configuration file", 7, 50, title = "Notification message")
			form_dialog.mainMenu()	
		except KeyError as exception:
			self.logger.createLogTool("Key Error: " + str(exception), 4)
			form_dialog.d.msgbox("\nKey Error: " + str(exception), 7, 50, title = "Error message")
			form_dialog.mainMenu()
		except OSError as exception:
			self.logger.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nError modifying the configuration file. For more information, see the logs.", 7, 50, title = "Error message")
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
			if data_conf[4] == True:
				valid_certificates_json = { 'valid_certificates' : data_conf[4] , 'path_cert' : str(data_conf[5]) }
				last_index = 5
			else:
				valid_certificates_json = { 'valid_certificates' : data_conf[4] }
				last_index = 4
			d.update(valid_certificates_json)
		else:
			last_index = 3
		if data_conf[last_index + 1] == True:
			http_auth_json = { 'use_http_auth' : True, 'http_auth_user' : data_conf[last_index + 2].decode("utf-8"), 'http_auth_pass' : data_conf[last_index + 3].decode("utf-8") }
			data_aux_json = { 'repository_name' : str(data_conf[last_index + 4]), 'telegram_bot_token' : data_conf[last_index + 5].decode('utf-8'), 'telegram_chat_id' : data_conf[last_index + 6].decode('utf-8') }
			d.update(http_auth_json)
		else:
			data_aux_json = { 'use_http_auth' : False, 'repository_name' : str(data_conf[last_index + 2]), 'telegram_bot_token' : data_conf[last_index + 3].decode('utf-8'), 'telegram_chat_id' : data_conf[last_index + 4].decode('utf-8') }
		d.update(data_aux_json)
		try:
			with open(self.utils.getPathSTool('conf') + '/es_conf.yaml', 'w') as yaml_file:
				yaml.dump(d, yaml_file, default_flow_style = False)
		except OSError as exception:
			self.logger.createLogTool(str(exception), 4)