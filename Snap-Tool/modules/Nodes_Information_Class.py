from libPyElk import libPyElk
from libPyLog import libPyLog
from libPyUtils import libPyUtils
from libPyDialog import libPyDialog
from .Constants_Class import Constants

"""
Class that manages ElasticSearch Node's Information.
"""
class NodesInformation:

	def __init__(self, action_to_cancel):
		"""
		Method that corresponds to the constructor of the class.

		:arg action_to_cancel (object): Method to be called when the user chooses the cancel option.
		"""
		self.__logger = libPyLog()
		self.__utils = libPyUtils()
		self.__constants = Constants()
		self.__elasticsearch = libPyElk()
		self.__action_to_cancel = action_to_cancel
		self.__dialog = libPyDialog(self.__constants.BACKTITLE, action_to_cancel)


	def displayNodesInformation(self):
		"""
		Method that displays ElasticSearch Node's Information.
		"""
		try:
			snap_tool_data = self.__utils.readYamlFile(self.__constants.PATH_SNAP_TOOL_CONFIGURATION_FILE)
			if snap_tool_data["use_authentication_method"] == True:
				if snap_tool_data["authentication_method"] == "API Key":
					conn_es = self.__elasticsearch.createConnectionToElasticSearchAPIKey(snap_tool_data, self.__constants.PATH_KEY_FILE)
				elif snap_tool_data["authentication_method"] == "HTTP Authentication":
					conn_es = self.__elasticsearch.createConnectionToElasticSearchHTTPAuthentication(snap_tool_data, self.__constants.PATH_KEY_FILE)
			else:
				conn_es = self.__elasticsearch.createConnectionToElasticSearchWithoutAuthentication(snap_tool_data)
			es_nodes_info = self.__elasticsearch.getNodesInformation(conn_es)
			message_to_display = "\nElasticSearch Nodes Information:\n\n"
			for es_node_info in es_nodes_info:
				message_to_display += "- " + es_nodes_info[es_node_info]["name"] + '\n'
				total_size_disk = es_nodes_info[es_node_info]["fs"]["total"]["total_in_bytes"]
				total_size_available_disk = es_nodes_info[es_node_info]["fs"]["total"]["available_in_bytes"]
				total_size_occupied_in_percentage = 100 - (total_size_available_disk * 100 / total_size_disk)
				message_to_display += "Total Size Occupied: " + str(round(total_size_occupied_in_percentage, 2)) +"%\n\n"
			conn_es.transport.close()
			self.__dialog.createScrollBoxDialog(message_to_display, 16, 70, "ElasticSearch Nodes Information")
		except Exception as exception:
			self.__dialog.createMessageDialog("\nError displaying ElasticSearch Nodes Information. For more information, see the logs.", 8, 50, "Error Message")
			self.__logger.generateApplicationLog(exception, 3, "__displayNodesInformation", use_file_handler = True, name_file_log = self.__constants.NAME_FILE_LOG)
		finally:
			self.__action_to_cancel()