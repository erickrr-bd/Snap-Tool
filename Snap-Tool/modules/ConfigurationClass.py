from os import path
from modules.UtilsClass import Utils
from modules.LoggerClass import Logger

"""
Class that manages everything related to the Snap-Tool
configuration file.
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
	Property that stores an object of type FormDialogs.
	"""
	form_dialog = None

	"""
	Property that stores the path of the configuration file.
	"""
	conf_file = None

	"""
	Constructor for the Configuration class.

	Parameters:
	self -- An instantiated object of the Configuration class.
	"""
	def __init__(self, form_dialog):
		self.logger = Logger()
		self.form_dialog = form_dialog
		self.utils = Utils(form_dialog)
		self.conf_file = self.utils.getPathSnapTool("conf") + "/snap_tool_conf.yaml"

	"""
	Method that requests the data for the creation of the
	Snap-Tool configuration file.

	Parameters:
	self -- An instantiated object of the Configuration class.
	"""
	def createConfiguration(self):
		data_conf = []
		version_es = self.form_dialog.getDataNumberDecimal("Enter the ElasticSearch version:", "7.15")
		data_conf.append(version_es)
		host_es = self.form_dialog.getDataIP("Enter the ElasticSearch IP address:", "localhost")
		data_conf.append(host_es)
		port_es = self.form_dialog.getDataPort("Enter the ElasticSearch listening port:", "9200")
		data_conf.append(port_es)
		use_ssl = self.form_dialog.getDataYesOrNo("\nDo you want Snap-Tool to connect to ElasticSearch using the SSL/TLS protocol?", "Connection Via SSL/TLS")		
		if use_ssl == "ok":
			data_conf.append(True)
			valid_certificate = self.form_dialog.getDataYesOrNo("\nDo you want the certificate for SSL/TLS communication to be validated?", "Certificate Validation")
			if valid_certificate == "ok":
				data_conf.append(True)
				path_cert_file = self.form_dialog.getFile('/etc/Snap-Tool', "Select the CA certificate:")
				data_conf.append(path_cert_file)
			else:
				data_conf.append(False)
		else:
			data_conf.append(False)
		http_auth = self.form_dialog.getDataYesOrNo("\nIs the use of HTTP authentication required to connect to ElasticSearch?", "HTTP Authentication")
		if http_auth == "ok":
			data_conf.append(True)
			user_http_auth = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the username for HTTP authentication:", "snap_tool_user"))
			data_conf.append(user_http_auth.decode('utf-8'))
			pass_http_auth = self.utils.encryptAES(self.form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
			data_conf.append(pass_http_auth.decode('utf-8'))
		else:
			data_conf.append(False)
		telegram_bot_token = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the Telegram bot token:", "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"))
		data_conf.append(telegram_bot_token.decode('utf-8'))
		telegram_chat_id = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the Telegram channel identifier:", "-1002365478941"))
		data_conf.append(telegram_chat_id.decode('utf-8'))
		is_delete_index = self.form_dialog.getDataYesOrNo("\nDo you want to enable automatic index removal?", "Automatic index removal")
		if is_delete_index == "ok":
			data_conf.append(True)
		else:
			data_conf.append(False)
		self.createFileConfiguration(data_conf)
		if path.exists(self.conf_file):
			self.form_dialog.d.msgbox("\nConfiguration file created", 7, 50, title = "Notification Message")
			self.logger.createSnapToolLog("Configuration file created", 2)
		else:
			self.form_dialog.d.msgbox("\nError creating configuration file. For more information, see the logs.", 8, 50, title = "Error Message")
		self.form_dialog.mainMenu()
	
	"""
	Method that modifies one or more fields of the Snap-Tool
	configuration file.

	Parameters:
	self -- An instantiated object of the Configuration class.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised
				when you try to access a key that isn’t in a
				dictionary (dict). 
	"""
	def updateConfiguration(self):
		options_conf_fields = [("Version", "ElasticSearch Version", 0),
							("Host", "ElasticSearch Host", 0),
							("Port", "ElasticSearch Port", 0),
							("SSL/TLS", "Enable or disable SSL/TLS connection", 0),
							("HTTP Authentication", "Enable or disable Http authentication", 0),
							("Bot Token", "Telegram bot token", 0),
							("Chat ID", "Telegram channel identifier", 0),
							("Delete Index", "Enable or disable automatic index removal", 0)]

		options_ssl_true = [("Disable", "Disable SSL/TLS communication", 0),
							("Certificate Validation", "Modify certificate validation", 0)]

		options_ssl_false = [("Enable", "Enable SSL/TLS communication", 0)]

		options_valid_cert_true = [("Disable", "Disable certificate validation", 0),
								   ("Certificate File", "Change certificate file", 0)]

		options_valid_cert_false = [("Enable", "Enable certificate validation", 0)]

		options_http_auth_true = [("Disable", "Disable HTTP authentication", 0),
								  ("Data", "Modify HTTP authentication data", 0)]

		options_http_auth_false = [("Enable", "Enable HTTP authentication", 0)]

		options_http_auth_data = [("Username", "Username for HTTP authentication", 0),
								 ("Password", "User password", 0)]

		options_delete_index_true = [("Disable", "Disable automatic index deletion", 0)]

		options_delete_index_false = [("Enable", "Enables automatic index deletion", 0)]

		flag_version = 0
		flag_host = 0
		flag_port = 0
		flag_use_ssl = 0
		flag_http_auth = 0
		flag_bot_token = 0
		flag_chat_id = 0
		flag_delete_index = 0
		opt_conf_fields = self.form_dialog.getDataCheckList("Select one or more options:", options_conf_fields,  "Configuration File Fields")
		for option in opt_conf_fields:
			if option == "Version":
				flag_version = 1
			elif option == "Host":
				flag_host = 1
			elif option == "Port":
				flag_port = 1
			elif option == "SSL/TLS":
				flag_use_ssl = 1
			elif option == "HTTP Authentication":
				flag_http_auth = 1
			elif option == "Bot Token":
				flag_bot_token = 1
			elif option == "Chat ID":
				flag_chat_id = 1
			elif option == "Delete Index":
				flag_delete_index = 1
		try:
			data_conf = self.utils.readYamlFile(self.conf_file, 'rU')
			hash_data_conf = self.utils.getHashToFile(self.conf_file)
			if flag_version == 1:
				version_es = self.form_dialog.getDataNumberDecimal("Enter the ElasticSearch version:", data_conf['es_version'])
				data_conf['es_version'] = version_es
			if flag_host == 1:
				host_es = self.form_dialog.getDataIP("Enter the ElasticSearch IP address:", data_conf['es_host'])
				data_conf['es_host'] = host_es
			if flag_port == 1:
				port_es = self.form_dialog.getDataPort("Enter the ElasticSearch listening port:", str(data_conf['es_port']))
				data_conf['es_port'] = int(port_es)
			if flag_use_ssl == 1:
				if data_conf['use_ssl'] == True:
					opt_ssl_true = self.form_dialog.getDataRadioList("Select a option:", options_ssl_true, "Connection via SSL/TLS")
					if opt_ssl_true == "Disable":
						del data_conf['valid_certificate']
						if 'path_certificate' in data_conf:
							del data_conf['path_certificate']
						data_conf['use_ssl'] = False
					elif opt_ssl_true == "Certificate Validation":
						if data_conf['valid_certificate'] == True:
							opt_valid_cert_true = self.form_dialog.getDataRadioList("Select a option:", options_valid_cert_true, "Certificate Validation")
							if opt_valid_cert_true == "Disable":
								if 'path_certificate' in data_conf:
									del data_conf['path_certificate']
								data_conf['valid_certificate'] = False
							elif opt_valid_cert_true == "Certificate File":
								path_cert_file = self.form_dialog.getFile(data_conf['path_certificate'], "Select the CA certificate:")
								data_conf['path_certificate'] = path_cert_file
						else:
							opt_valid_cert_false = self.form_dialog.getDataRadioList("Select a option:", options_valid_cert_false, "Certificate Validation")
							if opt_valid_cert_false == "Enable":
								data_conf['valid_certificate'] = True
								path_cert_file = self.form_dialog.getFile('/etc/Snap-Tool', "Select the CA certificate:")
								valid_cert_json = { 'path_certificate' : path_cert_file }
								data_conf.update(valid_cert_json)
				else:
					opt_ssl_false = self.form_dialog.getDataRadioList("Select a option:", options_ssl_false, "Connection via SSL/TLS")
					if opt_ssl_false == "Enable":
						data_conf['use_ssl'] = True
						valid_certificate = self.form_dialog.getDataYesOrNo("\nDo you want the certificates for SSL/TLS communication to be validated?", "Certificate Validation")
						if valid_certificate == "ok":
							path_cert_file = self.form_dialog.getFile('/etc/Snap-Tool', "Select the CA certificate:")
							valid_cert_json = { 'valid_certificate' : True, 'path_certificate' : path_cert_file }
						else:
							valid_cert_json = { 'valid_certificate' : False }
						data_conf.update(valid_cert_json)
			if flag_http_auth == 1:
				if data_conf['use_http_auth'] == True:
					opt_http_auth_true = self.form_dialog.getDataRadioList("Select a option:", options_http_auth_true, "HTTP Authentication")
					if opt_http_auth_true == "Disable":
						del(data_conf['http_auth_user'])
						del(data_conf['http_auth_pass'])
						data_conf['use_http_auth'] = False
					elif opt_http_auth_true == "Data":
						flag_http_auth_user = 0
						flag_http_auth_pass = 0
						opt_http_auth_data = self.form_dialog.getDataCheckList("Select one or more options:", options_http_auth_data, "HTTP Authentication")
						for option in opt_http_auth_data:
							if option == "Username":
								flag_http_auth_user = 1
							elif option == "Password":
								flag_http_auth_pass = 1
						if flag_http_auth_user == 1:
							user_http_auth = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the username for HTTP authentication:", "snap_tool_user"))
							data_conf['http_auth_user'] = user_http_auth.decode('utf-8')
						if flag_http_auth_pass == 1:
							pass_http_auth = self.utils.encryptAES(self.form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
							data_conf['http_auth_pass'] = pass_http_auth.decode('utf-8')
				else:
					opt_http_auth_false = self.form_dialog.getDataRadioList("Select a option:", options_http_auth_false, "HTTP Authentication")
					if opt_http_auth_false == "Enable":
						user_http_auth = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the username for HTTP authentication:", "snap_tool_user"))
						pass_http_auth = self.utils.encryptAES(self.form_dialog.getDataPassword("Enter the user's password for HTTP authentication:", "password"))
						http_auth_data_json = { 'http_auth_user': user_http_auth.decode('utf-8'), 'http_auth_pass': pass_http_auth.decode('utf-8') }
						data_conf.update(http_auth_data_json)
						data_conf['use_http_auth'] = True
			if flag_bot_token == 1:
				telegram_bot_token = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the Telegram bot token:", self.utils.decryptAES(data_conf['telegram_bot_token']).decode('utf-8')))
				data_conf['telegram_bot_token'] = telegram_bot_token.decode('utf-8')
			if flag_chat_id == 1:
				telegram_chat_id = self.utils.encryptAES(self.form_dialog.getDataInputText("Enter the Telegram channel identifier:", self.utils.decryptAES(data_conf['telegram_chat_id']).decode('utf-8')))
				data_conf['telegram_chat_id'] = telegram_chat_id.decode('utf-8')
			if flag_delete_index == 1:
				if data_conf['is_delete_index'] == True:
					opt_delete_index_true = self.form_dialog.getDataRadioList("Select a option:", options_delete_index_true, "Automatic index removal")
					if opt_delete_index_true == "Disable":
						data_conf['is_delete_index'] = False
				else:
					opt_delete_index_false = self.form_dialog.getDataRadioList("Select a option:", options_delete_index_false, "Automatic index removal")
					if opt_delete_index_false == "Enable":
						data_conf['is_delete_index'] = True
			self.utils.createYamlFile(data_conf, self.conf_file, 'w')
			hash_data_conf_upd = self.utils.getHashToFile(self.conf_file)
			if hash_data_conf == hash_data_conf_upd:
				self.form_dialog.d.msgbox("\nThe configuration file was not modified.", 7, 50, title = "Notification Message")
			else:
				self.logger.createSnapToolLog("The configuration file was modified", 1)
				self.form_dialog.d.msgbox("\nThe configuration file was modified.", 7, 50, title = "Notification Message")
			self.form_dialog.mainMenu()	
		except (OSError, KeyError) as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox("\nError modifying the configuration file. For more information, see the logs.", 8, 50, title = "Error Message")
			self.form_dialog.mainMenu()

	"""
	Method that creates the YAML file with the data entered
	for the Snap-Tool configuration file.

	Parameters:
	self -- An instantiated object of the Configuration class.
	data_conf -- List containing all the data entered for
				 the configuration file.
	
	Exceptions:
	OSError -- This exception is raised when a system
			   function returns a system-related error,
			   including I/O failures such as “file not
			   found” or “disk full” (not for illegal
			   argument types or other incidental errors).
	"""
	def createFileConfiguration(self, data_conf):
		data_json = {'es_version' : data_conf[0],
					'es_host' : data_conf[1],
					'es_port' : int(data_conf[2]),
					'use_ssl' : data_conf[3]}

		if data_conf[3] == True:
			if data_conf[4] == True:
				valid_certificate_json = { 'valid_certificate' : data_conf[4] , 'path_certificate' : data_conf[5] }
				last_index = 5
			else:
				valid_certificate_json = { 'valid_certificate' : data_conf[4] }
				last_index = 4
			data_json.update(valid_certificate_json)
		else:
			last_index = 3
		if data_conf[last_index + 1] == True:
			http_auth_json = { 'use_http_auth' : data_conf[last_index + 1], 'http_auth_user' : data_conf[last_index + 2], 'http_auth_pass' : data_conf[last_index + 3] }
			last_index += 3
		else:
			http_auth_json = { 'use_http_auth' : data_conf[last_index + 1] }
			last_index += 1
		data_json.update(http_auth_json)
		aux_json = { 'telegram_bot_token' : data_conf[last_index + 1], 'telegram_chat_id' : data_conf[last_index + 2], 'is_delete_index' : data_conf[last_index + 3] }
		data_json.update(aux_json)
		
		self.utils.createYamlFile(data_json, self.conf_file, 'w')
		