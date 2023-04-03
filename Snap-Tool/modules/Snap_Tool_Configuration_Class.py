from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages the Snap-Tool configuration.
"""
class SnapToolConfiguration:

	def __init__(self, action_to_cancel):
		"""
		Method that corresponds to the constructor of the class.

		:arg action_to_cancel (object): Method to be called when the user chooses the cancel option.
		"""
		self.__logger = libPyLog()
		self.__utils = libPyUtils()
		self.__constants = Constants()
		self.__action_to_cancel = action_to_cancel
		self.__dialog = libPyDialog(self.__constants.BACKTITLE, action_to_cancel)


	def createConfiguration(self):
		"""
		Method that creates the Snap-Tool configuration file.
		"""
		snap_tool_data = []
		try:
			passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
			total_es_nodes = self.__dialog.createInputBoxToNumberDialog("Enter the total number of ElasticSearch's master nodes:", 9, 50, "1")
			list_to_form_dialog = self.__utils.createListToDialogForm(int(total_es_nodes), "IP Address")
			es_host = self.__dialog.createFormDialog("Enter the IP addresses:", list_to_form_dialog, 15, 50, "ElasticSearch Hosts")
			snap_tool_data.append(es_host)
			es_port = self.__dialog.createInputBoxToPortDialog("Enter the ElasticSearch's listening port:", 8, 50, "9200")
			snap_tool_data.append(es_port)
			use_ssl_tls = self.__dialog.createYesOrNoDialog("\nDo you require that Snap-Tool communicates with ElasticSearch using the SSL/TLS protocol?", 8, 50, "SSL/TLS Connection")
			if use_ssl_tls == "ok":
				snap_tool_data.append(True)
				verificate_certificate_ssl = self.__dialog.createYesOrNoDialog("\nDo you require Snap-Tool to verificate the SSL certificate?", 8, 50, "Certificate Verification")
				if verificate_certificate_ssl == "ok":
					snap_tool_data.append(True)
					path_certificate_file = self.__dialog.createFileDialog("/etc/Snap-Tool", 8, 50, "Select the CA certificate:", ".pem")
					snap_tool_data.append(path_certificate_file)
				else:
					snap_tool_data.append(False)
			else:
				snap_tool_data.append(False)
			use_authentication_method = self.__dialog.createYesOrNoDialog("\nIs it required to use an authentication mechanism (HTTP authentication or API key) to connect to ElasticSearch?", 9, 50, "Authentication Method")
			if use_authentication_method == "ok":
				snap_tool_data.append(True)
				option_authentication_method = self.__dialog.createRadioListDialog("Select a option:", 9, 55, self.__constants.OPTIONS_AUTHENTICATION_METHOD, "Authentication Method")
				snap_tool_data.append(option_authentication_method)
				if option_authentication_method == "HTTP Authentication":
					user_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the username for HTTP authentication:", 8, 50, "user_http"), passphrase)
					snap_tool_data.append(user_http_authentication.decode("utf-8"))
					password_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the user's password for HTTP authentication:", 9, 50, "password", True), passphrase)
					snap_tool_data.append(password_http_authentication.decode("utf-8"))
				elif option_authentication_method == "API Key":
					api_key_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key Identifier:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
					snap_tool_data.append(api_key_id.decode("utf-8"))
					api_key = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
					snap_tool_data.append(api_key.decode("utf-8"))
			else:
				snap_tool_data.append(False)
			delete_index_automatic = self.__dialog.createYesOrNoDialog("\nDo you want the index to be deleted automatically at the end of the snapshot creation?", 9, 50, "Delete Index Automatically")
			if delete_index_automatic == "ok":
				snap_tool_data.append(True)
			else:
				snap_tool_data.append(False)
			password_privileged_actions = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the password", 8, 50, "password", True), passphrase)
			snap_tool_data.append(password_privileged_actions.decode("utf-8"))
			telegram_bot_token = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), passphrase)
			snap_tool_data.append(telegram_bot_token.decode("utf-8"))
			telegram_chat_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, "-1002365478941"), passphrase)
			snap_tool_data.append(telegram_chat_id.decode("utf-8"))
			self.__createYamlFileConfiguration(snap_tool_data)
			if path.exists(self.__constants.PATH_SNAP_TOOL_CONFIGURATION_FILE):
				self.__dialog.createMessageDialog("\nSnap-Tool configuration file created.", 7, 50, "Notification Message")
				self.__logger.generateApplicationLog("Snap-Tool configuration file created", 3, "__createConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		except Exception as exception:
			self.__dialog.createMessageDialog("\nError to create Snap-Tool configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		finally:
			self.__action_to_cancel()


	def updateConfiguration(self):
		"""
		Method that updates one or more values in the Snap-Tool configuration file.
		"""
		try:
			options_configuration_snap_tool_update = self.__dialog.createCheckListDialog("Select one or more options:", 15, 65, self.__constants.OPTIONS_CONFIGURATION_SNAP_TOOL_UPDATE, "Snap-Tool Configuration Fields")
			snap_tool_data = self.__utils.readYamlFile(self.__constants.PATH_SNAP_TOOL_CONFIGURATION_FILE)
			hash_file_configuration_original = self.__utils.getHashFunctionToFile(self.__constants.PATH_SNAP_TOOL_CONFIGURATION_FILE)
			if "Host" in options_configuration_snap_tool_update:
				option_es_hosts_update = self.__dialog.createMenuDialog("Select a option:", 10, 50, self.__constants.OPTIONS_ES_HOSTS_UPDATE, "ELasticSearch Hosts Menu")
				if option_es_hosts_update == "1":
					number_master_nodes_es = self.__dialog.createInputBoxToNumberDialog("Enter the total number of master nodes to enter:", 9, 50, "1")
					list_to_form_dialog = self.__utils.createListToDialogForm(int(number_master_nodes_es), "IP Address")
					es_hosts = self.__dialog.createFormDialog("Enter IP addresses of the ElasticSearch master nodes:", list_to_form_dialog, 15, 50, "Add ElasticSearch Hosts")
					snap_tool_data["es_hosts"].extend(es_hosts)
				elif option_es_hosts_update == "2":
					list_to_form_dialog = self.__utils.convertListToDialogForm(snap_tool_data["es_host"], "IP Address")
					es_hosts = self.__dialog.createFormDialog("Enter IP addresses of the ElasticSearch master nodes:", list_to_form_dialog, 15, 50, "Update ElasticSearch Hosts")
					snap_tool_data["es_host"] = es_hosts
				elif option_es_hosts_update == "3":
					list_to_dialog = self.__utils.convertListToDialogList(snap_tool_data["es_host"], "IP Address")
					options_remove_es_hosts = self.__dialog.createCheckListDialog("Select one or more options:", 15, 50, list_to_dialog, "Remove ElasticSearch Hosts")
					for option in options_remove_es_hosts:
						snap_tool_data["es_host"].remove(option)
			if "Port" in options_configuration_snap_tool_update:
				es_port = self.__dialog.createInputBoxToPortDialog("Enter the ElasticSearch listening port:", 8, 50, str(snap_tool_data['es_port']))
				snap_tool_data['es_port'] = int(es_port)
			if "SSL/TLS" in options_configuration_snap_tool_update:
				if snap_tool_data["use_ssl_tls"] == True:
					option_ssl_tls_true = self.__dialog.createRadioListDialog("Select a option:", 10, 70, self.__constants.OPTIONS_SSL_TLS_TRUE, "SSL/TLS Connection")
					if option_ssl_tls_true == "Disable":
						del snap_tool_data['verificate_certificate_ssl']
						if "path_certificate_file" in snap_tool_data:
							del snap_tool_data["path_certificate_file"]
						snap_tool_data["use_ssl_tls"] = False
					elif option_ssl_tls_true == "Certificate Verification":
						if snap_tool_data["verificate_certificate_ssl"] == True:
							option_verificate_certificate_true = self.__dialog.createRadioListDialog("Select a option:", 10, 70, self.__constants.OPTIONS_VERIFICATE_CERTIFICATE_TRUE, "Certificate Verification")
							if option_verificate_certificate_true == "Disable":
								if "path_certificate_file" in snap_tool_data:
									del snap_tool_data["path_certificate_file"]
								snap_tool_data["verificate_certificate_ssl"] = False
							elif option_verificate_certificate_true == "Certificate File":
								path_certificate_file = self.__dialog.createFileDialog(snap_tool_data["path_certificate_file"], 8, 50, "Select the CA certificate:", ".pem")
								snap_tool_data["path_certificate_file"] = path_certificate_file
						else:
							option_verificate_certificate_false = self.__dialog.createRadioListDialog("Select a option:", 8, 70, self.__constants.OPTIONS_VERIFICATE_CERTIFICATE_FALSE, "Certificate Verification")
							if option_verificate_certificate_false == "Enable":
								snap_tool_data["verificate_certificate_ssl"] = True
								path_certificate_file = self.__dialog.createFileDialog("/etc/Snap-Tool/configuration", 8, 50, "Select the CA certificate:", ".pem")
								verificate_certificate_ssl_json = {"path_certificate_file" : path_certificate_file}
								snap_tool_data.update(verificate_certificate_ssl_json)
				else:
					option_ssl_tls_false = self.__dialog.createRadioListDialog("Select a option:", 8, 70, self.__constants.OPTIONS_SSL_TLS_FALSE, "SSL/TLS Connection")
					snap_tool_data['use_ssl_tls'] = True
					verificate_certificate_ssl = self.__dialog.createYesOrNoDialog("\nDo you require that Snap-Tool verificates the SSL certificate?", 8, 50, "Certificate Verification")
					if verificate_certificate_ssl == "ok":
						path_certificate_file = self.__dialog.createFileDialog("/etc/Snap-Tool/configuration", 8, 50, "Select the CA certificate:", ".pem")
						verificate_certificate_ssl = {"verificate_certificate_ssl" : True, "path_certificate_file" : path_certificate_file}
					else:
						verificate_certificate_ssl = {"verificate_certificate_ssl" : False}
					snap_tool_data.update(verificate_certificate_ssl)
			if "Authentication" in options_configuration_snap_tool_update:
				if snap_tool_data["use_authentication_method"] == True:
					option_authentication_true = self.__dialog.createRadioListDialog("Select a option:", 9, 50, self.__constants.OPTIONS_AUTHENTICATION_TRUE, "Authentication Method")
					if option_authentication_true == "Data":
						if snap_tool_data["authentication_method"] == "HTTP Authentication":
							option_authentication_method_true = self.__dialog.createRadioListDialog("Select a option:", 9, 60, self.__constants.OPTIONS_AUTHENTICATION_METHOD_TRUE, "HTTP Authentication")
							if option_authentication_method_true == "Data":
								options_http_authentication_data = self.__dialog.createCheckListDialog("Select one or more options:", 9, 60, self.__constants.OPTIONS_HTTP_AUTHENTICATION_DATA, "HTTP Authentication")	
								if "Username" in options_http_authentication_data:
									passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
									user_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the username for HTTP authentication:", 8, 50, "user_http"), passphrase)									
									snap_tool_data["user_http_authentication"] = user_http_authentication.decode("utf-8")
								if "Password" in options_http_authentication_data:
									passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
									password_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the user's password for HTTP authentication:", 8, 50, "password", True), passphrase)
									snap_tool_data["password_http_authentication"] = password_http_authentication.decode("utf-8")
							elif option_authentication_method_true == "Disable":
								passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
								api_key_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key Identifier:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
								api_key = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
								del snap_tool_data["user_http_authentication"]
								del snap_tool_data["password_http_authentication"]
								snap_tool_data["authentication_method"] = "API Key"
								api_key_json = {"api_key_id" : api_key_id.decode("utf-8"), "api_key" : api_key.decode("utf-8")}
								snap_tool_data.update(api_key_json)
						elif snap_tool_data["authentication_method"] == "API Key":
							option_authentication_method_true = self.__dialog.createRadioListDialog("Select a option:", 9, 60, self.__constants.OPTIONS_AUTHENTICATION_METHOD_TRUE, "API Key")
							if option_authentication_method_true == "Data":
								options_api_key_data = self.__dialog.createCheckListDialog("Select one or more options:", 9, 50, self.__constants.OPTIONS_API_KEY_DATA, "API Key")
								if "API Key ID" in options_api_key_data:
									passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
									api_key_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key Identifier:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
									snap_tool_data["api_key_id"] = api_key_id.decode("utf-8")
								if "API Key" in options_api_key_data:
									passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
									api_key = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
									snap_tool_data["api_key"] = api_key.decode("utf-8")
							elif option_authentication_method_true == "Disable":
								passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
								user_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the username for HTTP authentication:", 8, 50, "user_http"), passphrase)
								password_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the user's password for HTTP authentication:", 8, 50, "password", True), passphrase)
								del snap_tool_data["api_key_id"]
								del snap_tool_data["api_key"]
								snap_tool_data["authentication_method"] = "HTTP Authentication"
								http_authentication_json = {"user_http_authentication" : user_http_authentication.decode("utf-8"), "password_http_authentication" : password_http_authentication.decode("utf-8")}
								snap_tool_data.update(http_authentication_json)
					elif option_authentication_true == "Disable":
						snap_tool_data["use_authentication_method"] = False
						if snap_tool_data["authentication_method"] == "HTTP Authentication":
							del snap_tool_data["user_http_authentication"]
							del snap_tool_data["password_http_authentication"]
						elif snap_tool_data["authentication_method"] == "API Key":
							del snap_tool_data["api_key_id"]
							del snap_tool_data["api_key"]
						del snap_tool_data["authentication_method"]
				else:
					option_authentication_false = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_AUTHENTICATION_FALSE, "Authentication Method")
					if option_authentication_false == "Enable":
						snap_tool_data["use_authentication_method"] = True
						option_authentication_method = self.__dialog.createRadioListDialog("Select a option:", 10, 55, self.__constants.OPTIONS_AUTHENTICATION_METHOD, "Authentication Method")
						if option_authentication_method == "HTTP Authentication":
							passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
							user_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the username for HTTP authentication:", 8, 50, "user_http"), passphrase)
							password_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the user's password for HTTP authentication:", 8, 50, "password", True), passphrase)
							http_authentication_json = {"authentication_method" : "HTTP Authentication", "user_http_authentication" : user_http_authentication.decode("utf-8"), "password_http_authentication" : password_http_authentication.decode("utf-8")}
							snap_tool_data.update(http_authentication_json)
						elif option_authentication_method == "API Key":
							passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
							api_key_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key Identifier:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
							api_key = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
							api_key_json = {"authentication_method" : "API Key", "api_key_id" : api_key_id.decode("utf-8"), "api_key" : api_key.decode("utf-8")}
							snap_tool_data.update(api_key_json)
			if "Delete Index" in options_configuration_snap_tool_update:
				if snap_tool_data["delete_index_automatic"] == True:
					option_delete_index_true = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_DELETE_INDEX_TRUE, "Delete Index Automatically")
					if option_delete_index_true == "Disable":
						snap_tool_data["delete_index_automatic"] = False
				else:
					option_delete_index_false = self.__dialog.createRadioListDialog("Select a option:", 8, 50, self.__constants.OPTIONS_DELETE_INDEX_FALSE, "Delete Index Automatically")
					if option_delete_index_false == "Enable":
						snap_tool_data["delete_index_automatic"] = True
			if "Password" in options_configuration_snap_tool_update:
				passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
				password_privileged_actions = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the password", 8, 50, "password", True), passphrase)
				snap_tool_data["password_privileged_actions"] = password_privileged_actions.decode("utf-8")
			if "Bot Token" in options_configuration_snap_tool_update:
				passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
				telegram_bot_token = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, self.__utils.decryptDataWithAES(snap_tool_data["telegram_bot_token"], passphrase).decode("utf-8")), passphrase)
				snap_tool_data["telegram_bot_token"] = telegram_bot_token.decode("utf-8")
			if "Chat ID" in options_configuration_snap_tool_update:
				passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
				telegram_chat_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, self.__utils.decryptDataWithAES(snap_tool_data["telegram_chat_id"], passphrase).decode("utf-8")), passphrase)
				snap_tool_data["telegram_chat_id"] = telegram_chat_id.decode("utf-8")
			self.__utils.createYamlFile(snap_tool_data, self.__constants.PATH_SNAP_TOOL_CONFIGURATION_FILE)
			hash_file_configuration_new = self.__utils.getHashFunctionToFile(self.__constants.PATH_SNAP_TOOL_CONFIGURATION_FILE)
			if hash_file_configuration_new == hash_file_configuration_original:
				self.__dialog.createMessageDialog("\nSnap-Tool configuration file not modified.", 7, 50, "Notification Message")
			else:
				self.__dialog.createMessageDialog("\nSnap-Tool configuration file modified.", 7, 50, "Notification Message")
				self.__logger.generateApplicationLog("Snap-Tool configuration file modified", 2, "__updateConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		except Exception as exception:
			self.__dialog.createMessageDialog("\nError to update Snap-Tool configuration. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__updateConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		finally:
			self.__action_to_cancel()


	def displayConfigurationData(self):
		"""
		Method that displays the data stored in the Snap-Tool configuration file.
		"""
		try:
			snap_tool_data = self.__utils.convertDataYamlFileToString(self.__constants.PATH_SNAP_TOOL_CONFIGURATION_FILE)
			message_to_display = "\nSnap-Tool Configuration Data:\n\n" + snap_tool_data
			self.__dialog.createScrollBoxDialog(message_to_display, 18, 70, "Snap-Tool Configuration")
		except Exception as exception:
			self.__dialog.createMessageDialog("\nError displaying Snap-Tool configuration data. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__displayConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		finally:
			self.__action_to_cancel()


	def __createYamlFileConfiguration(self, snap_tool_data):
		"""
		Method that creates the YAML file corresponding to the Snap-Tool configuration.

		:arg snap_tool_data (dict): Dictionary with data to be stored in the configuration file.
		"""
		snap_tool_data_json = {
			"es_host" : snap_tool_data[0],
			"es_port" : int(snap_tool_data[1]),
			"use_ssl_tls" : snap_tool_data[2]
		}

		if snap_tool_data[2] == True:
			if snap_tool_data[3] == True:
				verificate_certificate_ssl_json = {"verificate_certificate_ssl" : snap_tool_data[3], "path_certificate_file" : snap_tool_data[4]}
				last_index = 4
			else:
				verificate_certificate_ssl_json = {"verificate_certificate_ssl" : snap_tool_data[3]}
				last_index = 3
			snap_tool_data_json.update(verificate_certificate_ssl_json)
		else:
			last_index = 2
		if snap_tool_data[last_index + 1] == True:
			if snap_tool_data[last_index + 2] == "HTTP Authentication":
				http_authentication_json = {"use_authentication_method" : snap_tool_data[last_index + 1], "authentication_method" : snap_tool_data[last_index + 2], "user_http_authentication" : snap_tool_data[last_index + 3], "password_http_authentication" : snap_tool_data[last_index + 4]}
				snap_tool_data_json.update(http_authentication_json)
			elif snap_tool_data[last_index + 2] == "API Key":
				api_key_json = {"use_authentication_method" : snap_tool_data[last_index + 1], "authentication_method" : snap_tool_data[last_index + 2], "api_key_id" : snap_tool_data[last_index + 3], "api_key" : snap_tool_data[last_index + 4]}
				snap_tool_data_json.update(api_key_json)
			last_index += 4
		else:
			authentication_method_json = {"use_authentication_method" : snap_tool_data[last_index + 1]}
			snap_tool_data_json.update(authentication_method_json)
			last_index += 1
		aux_snap_tool_data_json = {"delete_index_automatic" : snap_tool_data[last_index + 1], "password_privileged_actions" : snap_tool_data[last_index + 2], "telegram_bot_token" : snap_tool_data[last_index + 3], "telegram_chat_id" : snap_tool_data[last_index + 4]}
		snap_tool_data_json.update(aux_snap_tool_data_json)

		self.__utils.createYamlFile(snap_tool_data_json, self.__constants.PATH_SNAP_TOOL_CONFIGURATION_FILE)