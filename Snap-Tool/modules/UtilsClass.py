import os
import sys
import yaml
from Crypto import Random
from hashlib import sha256
from Crypto.Cipher import AES
from modules.LoggerClass import Logger
from base64 import b64encode, b64decode
from Crypto.Util.Padding import pad, unpad

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
	Constructor for the Utils class.

	Parameters:
	self -- An instantiated object of the Utils class.
	"""
	def __init__(self):
		self.passphrase = self.getPassphrase()
		self.logger = Logger()

	"""
	Method that obtains the content of a file with the extension yaml.

	Parameters:
	self -- An instantiated object of the Utils class.
	file_yaml -- Yaml file path.

	Return:
	data_yaml -- Contents of the .yaml file stored in a list.

	Exceptions:
	IOError -- It is an error raised when an input/output operation fails.
	"""
	def readFileYaml(self, file_yaml):
		try:
			with open(file_yaml, 'r') as file:
				data_yaml = yaml.safe_load(file)
			return data_yaml
		except IOError as exception:
			self.logger.createLogTool("Error" + str(exception), 4)
			sys.exit(1)

	"""
	Method that creates a new route from the root path of Snap-Tool.

	Parameters:
	self -- An instantiated object of the Utils class.
	path_dir -- Folder or directory that will be added to the source path of Snap-Tool.

	Return:
	path_final -- Final directory.
	"""
	def getPathSTool(self, path_dir):
		path_root = "/etc/Snap-Tool"
		path_final = os.path.join(path_root, path_dir)
		return path_final

	"""
	Method that obtains the passphrase used for the process of encrypting and decrypting a file.

	Parameters:
	self -- An instantiated object of the Utils class.

	Return:
	pass_key -- Passphrase in a character string.

	Exceptions:
	FileNotFoundError -- his is an exception in python and it comes when a file does not exist and we want to use it. 
	"""
	def getPassphrase(self):
		try:
			file_key = open(self.getPathSTool('conf') + '/key','r')
			pass_key = file_key.read()
			file_key.close()
			return pass_key
		except FileNotFoundError as exceptions:
			self.logger.createLogTool(str(exceptions), 4)
			sys.exit(1)

	"""
	Method that validates data from a regular expression.

	self -- An instantiated object of the Utils class.
	regular_expression -- Regular expression with which the data will be validated.
	data -- Data to be validated.
	"""
	def validateRegularExpression(self, regular_expression, data):
		if(not regular_expression.match(data)):
			return False
		return True

	"""
	Method that obtains the hash of a particular file.

	Parameters:
	self -- An instantiated object of the Utils class.
	file -- Path of the file from which the hash function will be obtained.

	Return:
	Hash obtained.

	Exceptions:
	Exception -- Thrown when any mistake happens.
	"""
	def getSha256File(self, file):
		try:
			hashsha = sha256()
			with open(file, "rb") as file_hash:
				for block in iter(lambda: file_hash.read(4096), b""):
					hashsha.update(block)
			return hashsha.hexdigest()
		except Exception as exception:
			self.logger.createLogTool("Error: " + str(exception), 4)

	"""
	Method that encrypts a text string.

	Parameters:
	self -- An instantiated object of the Utils class.
	text -- Text to encrypt.

	Return:
	Encrypted text.
	"""
	def encryptAES(self, text):
		text_bytes = bytes(text, 'utf-8')
		key = sha256(self.passphrase.encode()).digest()
		IV = Random.new().read(AES.block_size)
		aes = AES.new(key, AES.MODE_CBC, IV)
		return b64encode(IV + aes.encrypt(pad(text_bytes, AES.block_size)))

	"""
	Method that decrypts a text string.

	Parameters:
	self -- An instantiated object of the Utils class.
	text_encrypt -- Text to decipher.

	Return:
	Character string with decrypted text.

	Exceptions:
	binascii.Error -- Is raised if were incorrectly padded or if there are non-alphabet characters present in the string. 
	"""
	def decryptAES(self, text_encrypt):
		try:
			key = sha256(self.passphrase.encode()).digest()
			text_encrypt = b64decode(text_encrypt)
			IV = text_encrypt[:AES.block_size]
			aes = AES.new(key, AES.MODE_CBC, IV)
			return unpad(aes.decrypt(text_encrypt[AES.block_size:]), AES.block_size)
		except binascii.Error as exception:
			self.logger.createLogTool("Decrypt Error: " + str(exception), 4)
			sys.exit(1)