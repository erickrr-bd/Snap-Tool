from libPyElk import libPyElk
from libPyLog import libPyLog
from libPyDialog import libPyDialog
from .Constants_Class import Constants

class Snapshots:

	def __init__(self, action_to_cancel):
		self.__logger = libPyLog()
		self.__constants = Constants()
		self.__elasticsearch = libPyElk()
		self.__action_to_cancel = action_to_cancel
		self.__dialog = libPyDialog(self.__constants.BACKTITLE, action_to_cancel)


	def createSnapshot(self):
		try:
			print("Hola")
		except Exception as exception:
			self.__dialog.createMessageDialog("\nError to create snapshot. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__createSnapshot", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		finally:
			self.__action_to_cancel()