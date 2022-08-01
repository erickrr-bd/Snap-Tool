from os import path
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages what is related to the configuration of Snap-Tool.
"""
class SnapToolConfiguration:
	"""
	Attribute that stores an object of the libPyUtils class.
	"""
	__utils = None

	"""
	Attribute that stores an object of the libPyLog class.
	"""
	__logger = None

	"""
	Attribute that stores an object of the libPyDialog class.
	"""
	__dialog = None

	"""
	Attribute that stores an object of the Constants class.
	"""
	__constants = None

	"""
	Attribute that stores the method to be called when the user chooses the cancel option.
	"""
	__action_to_cancel = None


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


	def createSnapToolConfiguration(self):
		"""
		Method that collects the information for the creation of the Snap-Tool configuration file.
		"""
		snap_tool_configuration_data = []
		try:
			passphrase = self.__utils.getPassphraseKeyFile(self.__constants.PATH_KEY_FILE)
			es_host = self.__dialog.createInputBoxToIPDialog("Enter the ElasticSearch IP address:", 8, 50, "localhost")
			snap_tool_configuration_data.append(es_host)
			es_port = self.__dialog.createInputBoxToPortDialog("Enter the ElasticSearch listening port:", 8, 50, "9200")
			snap_tool_configuration_data.append(es_port)
			use_ssl_tls = self.__dialog.createYesOrNoDialog("\nDo you require Snap-Tool to communicate with ElasticSearch using the SSL/TLS protocol?", 8, 50, "SSL/TLS Connection")
			if use_ssl_tls == "ok":
				snap_tool_configuration_data.append(True)
				verificate_certificate_ssl = self.__dialog.createYesOrNoDialog("\nDo you require Snap-Tool to verificate the SSL certificate?", 8, 50, "Certificate Verification")
				if verificate_certificate_ssl == "ok":
					snap_tool_configuration_data.append(True)
					path_certificate_file = self.__dialog.createFileDialog("/etc/Snap-Tool", 8, 50, "Select the CA certificate:", ".pem")
					snap_tool_configuration_data.append(path_certificate_file)
				else:
					snap_tool_configuration_data.append(False)
			else:
				snap_tool_configuration_data.append(False)
			use_authentication_method = self.__dialog.createYesOrNoDialog("\nIs it required to use an authentication mechanism (HTTP authentication or API key) to connect to ElasticSearch?", 8, 50, "Authentication Method")
			if use_authentication_method == "ok":
				snap_tool_configuration_data.append(True)
				option_authentication_method = self.__dialog.createRadioListDialog("Select a option:", 10, 55, self.__constants.OPTIONS_AUTHENTICATION_METHOD, "Authentication Method")
				snap_tool_configuration_data.append(option_authentication_method)
				if option_authentication_method == "HTTP authentication":
					user_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the username for HTTP authentication:", 8, 50, "user_http"), passphrase)
					snap_tool_configuration_data.append(user_http_authentication.decode("utf-8"))
					password_http_authentication = self.__utils.encryptDataWithAES(self.__dialog.createPasswordBoxDialog("Enter the user's password for HTTP authentication:", 8, 50, "password", True), passphrase)
					snap_tool_configuration_data.append(password_http_authentication.decode("utf-8"))
				elif option_authentication_method == "API Key":
					api_key_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key Identifier:", 8, 50, "VuaCfGcBCdbkQm-e5aOx"), passphrase)
					snap_tool_configuration_data.append(api_key_id.decode("utf-8"))
					api_key = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the API Key:", 8, 50, "ui2lp2axTNmsyakw9tvNnw"), passphrase)
					snap_tool_configuration_data.append(api_key.decode("utf-8"))
			else:
				snap_tool_configuration_data.append(False)
			delete_index_automatic = self.__dialog.createYesOrNoDialog("\nDo you want the index to be deleted automatically at the end of the snapshot creation?", 8, 50, "Delete Index Automatically")
			if delete_index_automatic == "ok":
				snap_tool_configuration_data.append(True)
			else:
				snap_tool_configuration_data.append(False)
			telegram_bot_token = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram bot token:", 8, 50, "751988420:AAHrzn7RXWxVQQNha0tQUzyouE5lUcPde1g"), passphrase)
			snap_tool_configuration_data.append(telegram_bot_token.decode("utf-8"))
			telegram_chat_id = self.__utils.encryptDataWithAES(self.__dialog.createInputBoxDialog("Enter the Telegram channel identifier:", 8, 50, "-1002365478941"), passphrase)
			snap_tool_configuration_data.append(telegram_chat_id.decode("utf-8"))
			self.__createYamlFileConfiguration(snap_tool_configuration_data)
			if path.exists(self.__constants.PATH_CONFIGURATION_FILE):
				self.__dialog.createMessageDialog("\nSnap-Tool configuration created.", 7, 50, "Notification Message")
				self.__logger.generateApplicationLog("Snap-Tool configuration created.", 3, "__createConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		except ValueError as exception:
			self.__dialog.createMessageDialog("\nFailed to encrypt/decrypt data. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		except (IOError, OSError, FileNotFoundError) as exception:
			self.__dialog.createMessageDialog("\nFailed to open, read or write in a file. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		finally:
			self.__action_to_cancel()


	def modifySnapToolConfiguration(self):
		try:
			print("m")
		except KeyError as exception:
			print("Error")
		finally:
			self.__action_to_cancel()


	def showSnapToolConfiguration(self):
		"""
		Method that displays the data stored in the Snap-Tool configuration file.
		"""
		try:
			snap_tool_configuration_data = self.__utils.convertDataYamlFileToString(self.__constants.PATH_CONFIGURATION_FILE)
			message_to_display = "\nSnap-Tool Configuration:\n\n" + snap_tool_configuration_data
			self.__dialog.createScrollBoxDialog(message_to_display, 18, 70, "Snap-Tool Configuration")
		except (IOError, OSError, FileNotFoundError) as exception:
			self.__dialog.createMessageDialog("\nFailed to open or read a file. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__showConfiguration", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		finally:
			self.__action_to_cancel()


	def __createYamlFileConfiguration(self, snap_tool_configuration_data):
		"""
		Method that creates the YAML file corresponding to the Snap-Tool configuration.

		:arg snap_tool_configuration_data (list): List with the data that will be stored in the configuration file.
		"""
		snap_tool_data_json = {
			"es_host" : snap_tool_configuration_data[0],
			"es_port" : int(snap_tool_configuration_data[1]),
			"use_ssl_tls" : snap_tool_configuration_data[2]
		}

		if snap_tool_configuration_data[2] == True:
			if snap_tool_configuration_data[3] == True:
				verificate_certificate_ssl_json = {"verificate_certificate_ssl" : snap_tool_configuration_data[3], "path_certificate_file" : snap_tool_configuration_data[4]}
				last_index = 4
			else:
				verificate_certificate_ssl_json = {"verificate_certificate_ssl" : snap_tool_configuration_data[3]}
				last_index = 3
			snap_tool_data_json.update(verificate_certificate_ssl_json)
		else:
			last_index = 2
		if snap_tool_configuration_data[last_index + 1] == True:
			if snap_tool_configuration_data[last_index + 2] == "HTTP authentication":
				http_authentication_json = {"use_authentication_method" : snap_tool_configuration_data[last_index + 1], "authentication_method" : snap_tool_configuration_data[last_index + 2], "user_http_authentication" : snap_tool_configuration_data[last_index + 3], "password_http_authentication" : snap_tool_configuration_data[last_index + 4]}
				snap_tool_data_json.update(http_authentication_json)
			elif snap_tool_configuration_data[last_index + 2] == "API Key":
				api_key_json = {"use_authentication_method" : snap_tool_configuration_data[last_index + 1], "authentication_method" : snap_tool_configuration_data[last_index + 2], "api_key_id" : snap_tool_configuration_data[last_index + 3], "api_key" : snap_tool_configuration_data[last_index + 4]}
				snap_tool_data_json.update(api_key_json)
			last_index += 4
		else:
			authentication_method_json = {"use_authentication_method" : snap_tool_configuration_data[last_index + 1]}
			snap_tool_data_json.update(authentication_method_json)
			last_index += 1
		aux_snap_tool_data_json = {"delete_index_automatic" : snap_tool_configuration_data[last_index + 1], "telegram_bot_token" : snap_tool_configuration_data[last_index + 2], "telegram_chat_id" : snap_tool_configuration_data[last_index + 3]}
		snap_tool_data_json.update(aux_snap_tool_data_json)

		self.__utils.createYamlFile(snap_tool_data_json, self.__constants.PATH_CONFIGURATION_FILE)