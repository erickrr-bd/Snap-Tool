from os import path
from Crypto import Random
from hashlib import sha256
from Crypto.Cipher import AES
from yaml import safe_load, safe_dump
from modules.LoggerClass import Logger
from base64 import b64encode, b64decode
from Crypto.Util.Padding import pad, unpad

"""
Class that allows managing all the utilities that are used for
the operation of the application.
"""
class Utils:
	"""
	Property that saves the passphrase that will be used for the decryption process.
	"""
	passphrase = None

	"""
	Property that stores an object of type Logger.
	"""
	logger = None

	"""
	Property that stores an object of type FormDialogs.
	"""
	form_dialog = None

	"""
	Constructor for the Utils class.

	Parameters:
	self -- An instantiated object of the Utils class.
	"""
	def __init__(self, form_dialog):
		self.logger = Logger()
		self.form_dialog = form_dialog
		self.passphrase = self.getPassphrase()

	"""
	Method that creates a YAML file.

	Parameters:
	self -- An instantiated object of the Utils class.
	data -- Information that will be stored in the YAML file.
	path_file_yaml -- YAML file path.
	mode -- Mode in which the YAML file will be opened.

	Exceptions:
	IOError -- It is an error raised when an input/output
	           operation fails.
	"""
	def createYamlFile(self, data, path_file_yaml, mode):
		try:
			with open(path_file_yaml, mode) as file_yaml:
				safe_dump(data, file_yaml, default_flow_style = False)
		except IOError as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox("\nError creating YAML file. For more information, see the logs.", 8, 50, title = "Error Message")
			self.form_dialog.mainMenu()

	"""
	Method that obtains and stores the content of a YAML file
	in a variable.

	Parameters:
	self -- An instantiated object of the Utils class.
	path_file_yaml -- YAML file path.
	mode -- Mode in which the YAML file will be opened.

	Return:
	data_file_yaml -- Variable that stores the content of the
					  YAML file.

	Exceptions:
	IOError -- It is an error raised when an input/output
	           operation fails.
	"""
	def readYamlFile(self, path_file_yaml, mode):
		try:
			with open(path_file_yaml, mode) as file_yaml:
				data_file_yaml = safe_load(file_yaml)
		except IOError as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox("\nError opening or reading the YAML file. For more information, see the logs.", 8, 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return data_file_yaml

	"""
	Method that defines a directory based on the main Snap-Tool
	directory.

	Parameters:
	self -- An instantiated object of the Utils class.
	path_dir -- Directory that is added to the main Snap-Tool 
	            directory.

	Return:
	path_final -- Defined final path.

	Exceptions:
	OSError -- This exception is raised when a system function
	           returns a system-related error, including I/O
	           failures such as “file not found” or “disk full”
	           (not for illegal argument types or other incidental
	           errors).
	TypeError -- Raised when an operation or function is applied
				 to an object of inappropriate type. The associated
				 value is a string giving details about the type 
				 mismatch.
	"""
	def getPathSnapTool(self, path_dir):
		path_main = "/etc/Snap-Tool"
		try:
			path_final = path.join(path_main, path_dir)
		except (OSError, TypeError) as exception:
			self.logger.createLogSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox("\nAn error has occurred. For more information, see the logs.", 8, 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return path_final

	"""
	Method that obtains the passphrase used for the process of
	encrypting and decrypting a file.

	Parameters:
	self -- An instantiated object of the Utils class.

	Return:
	pass_key -- Passphrase in a character string.

	Exceptions:
	FileNotFoundError -- This is an exception in python and it
						 comes when a file does not exist
						 and we want to use it. 
	"""
	def getPassphrase(self):
		try:
			file_key = open(self.getPathSnapTool('conf') + '/key','r')
			pass_key = file_key.read()
			file_key.close()
		except FileNotFoundError as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox("\nError opening or reading the Key file. For more information, see the logs.", 8, 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return pass_key

	"""
	Method that validates an entered value based on a defined
	regular expression.

	Parameters:
	self -- An instantiated object of the Utils class.
	regular_expression -- Regular expression with which the 
						  data will be validated.
	data_entered -- Data to be validated.

	Return:
	If the data entered is valid or not.
	"""
	def validateRegularExpression(self, regular_expression, data_entered):
		if(not regular_expression.match(data_entered)):
			return False
		return True

	"""
	Method that converts a list into a list that can be
	used for a checklist or radiolist in the application.

	Parameters:
	self -- An instantiated object of the Utils class.
	list_to_convert -- List to convert.
	text -- Text that will be displayed next to the item in
			the interface.

	Return:
	new_list_convert -- Converted list.
	"""
	def convertListToCheckOrRadioList(self, list_to_convert, text):
		new_list_convert = []
		for item in list_to_convert:
			new_list_convert.append((item, text, 0))
		return new_list_convert

	"""
	Method that converts a list of objects to text.
	
	Parameters:
	self -- An instantiated object of the Utils class.
	list_to_convert -- List to convert.

	Return:
	message -- Obtained text.
	"""
	def convertListToString(self, list_to_convert):
		message = ""
		for item in list_to_convert:
			message += "- " + item + '\n'
		return message

	"""
	Method that obtains the hash of a file.

	Parameters:
	self -- An instantiated object of the Utils class.
	file -- Path of the file from which the hash function will
	        be obtained.

	Return:
	Hash of the file.

	Exceptions:
	IOError -- It is an error raised when an input/output
	           operation fails.
	"""
	def getHashToFile(self, path_file):
		try:
			hash_sha = sha256()
			with open(path_file, 'rb') as file_to_hash:
				for block in iter(lambda: file_to_hash.read(4096), b""):
					hash_sha.update(block)
		except IOError as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox("\nError getting the file's hash function. For more information, see the logs.", 8, 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return hash_sha.hexdigest()

	"""
	Method that encrypts a text string.

	Parameters:
	self -- An instantiated object of the Utils class.
	text -- Text to encrypt.
	form_dialog -- A FormDialogs class object.

	Return:
	Encrypted text.

	Exceptions:
	binascii.Error -- Is raised if were incorrectly padded or
					  if there are non-alphabet characters
					  present in the string. 
	"""
	def encryptAES(self, text):
		try:
			text_bytes = bytes(text, 'utf-8')
			key = sha256(self.passphrase.encode()).digest()
			IV = Random.new().read(AES.block_size)
			aes = AES.new(key, AES.MODE_CBC, IV)
		except Exception as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox("\nFailed to encrypt the data. For more information, see the logs.", 8, 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return b64encode(IV + aes.encrypt(pad(text_bytes, AES.block_size)))

	"""
	Method that decrypts a text string.

	Parameters:
	self -- An instantiated object of the Utils class.
	text_encrypt -- Text to decipher.
	form_dialog -- A FormDialogs class object.

	Return:
	Character string with decrypted text.

	Exceptions:
	binascii.Error -- Is raised if were incorrectly padded or
					  if there are non-alphabet characters
					  present in the string. 
	"""
	def decryptAES(self, text_encrypt):
		try:
			key = sha256(self.passphrase.encode()).digest()
			text_encrypt = b64decode(text_encrypt)
			IV = text_encrypt[:AES.block_size]
			aes = AES.new(key, AES.MODE_CBC, IV)
		except binascii.Error as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox("\nFailed to decrypt the data. For more information, see the logs.", 8, 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return unpad(aes.decrypt(text_encrypt[AES.block_size:]), AES.block_size)