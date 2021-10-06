from sys import exit, warnoptions
from modules.UtilsClass import Utils
from ssl import create_default_context
from modules.LoggerClass import Logger
from requests.exceptions import InvalidURL
from elasticsearch import Elasticsearch, RequestsHttpConnection, exceptions	

"""
Class that allows you to manage everything related to
ElasticSearch.
"""
class Elastic:
	"""
	Disable warning message.
	"""
	if not warnoptions:
		import warnings
		warnings.simplefilter("ignore")
	
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

	snap_tool_conf = None

	"""
	Constructor for the Elastic class.

	Parameters:
	self -- An instantiated object of the Elastic class.
	"""
	def __init__(self, form_dialog):
		self.logger = Logger()
		self.form_dialog = form_dialog
		self.utils = Utils(form_dialog)
		self.snap_tool_conf = self.utils.readYamlFile(self.utils.getPathSnapTool('conf') + '/snap_tool_conf.yaml', 'r')

	"""
	Method that creates a connection object with ElasticSearch.

	Parameters:
	self -- An instantiated object of the Elastic class.

	Return:
	conn_es -- Object that contains the connection to
			   ElasticSearch.

	Exceptions:
	KeyError -- A Python KeyError exception is what is
				raised when you try to access a key that
				isn’t in a dictionary (dict). 
	exceptions.ConnectionError --  Error raised when there
								   was an exception while
								   talking to ES. 
	exceptions.AuthenticationException -- Exception representing
										  a 401 status code.
	exceptions.AuthorizationException -- Exception representing
										 a 403 status code.
	requests.exceptions.InvalidURL -- The URL provided was
									  somehow invalid.
	"""
	def getConnectionElastic(self):
		conn_es = None
		try:
			if(not self.snap_tool_conf['use_ssl'] == True) and (not self.snap_tool_conf['use_http_auth'] == True):
				conn_es = Elasticsearch(self.snap_tool_conf['es_host'],
										port = self.snap_tool_conf['es_port'],
										connection_class = RequestsHttpConnection,
										use_ssl = False)
			if(not self.snap_tool_conf['use_ssl'] == True) and self.snap_tool_conf['use_http_auth'] == True:
				conn_es = Elasticsearch(self.snap_tool_conf['es_host'],
										port = self.snap_tool_conf['es_port'],
										connection_class = RequestsHttpConnection,
										http_auth = (self.utils.decryptAES(self.snap_tool_conf['http_auth_user']).decode('utf-8'), self.utils.decryptAES(self.snap_tool_conf['http_auth_pass']).decode('utf-8')),
										use_ssl = False)
			if self.snap_tool_conf['use_ssl'] == True and (not self.snap_tool_conf['use_http_auth'] == True):
				if not self.snap_tool_conf['valid_certificate']:
					conn_es = Elasticsearch(self.snap_tool_conf['es_host'],
											port = self.snap_tool_conf['es_port'],
											connection_class = RequestsHttpConnection,
											use_ssl = True,
											verify_certs = False,
											ssl_show_warn = False)
				else:
					context = create_default_context(cafile = self.snap_tool_conf['path_certificate'])
					conn_es = Elasticsearch(self.snap_tool_conf['es_host'],
											port = self.snap_tool_conf['es_port'],
											connection_class = RequestsHttpConnection,
											use_ssl = True,
											verify_certs = True,
											ssl_context = context)
			if self.snap_tool_conf['use_ssl'] == True and self.snap_tool_conf['use_http_auth'] == True:
				if not self.snap_tool_conf['valid_certificate'] == True:
					conn_es = Elasticsearch(self.snap_tool_conf['es_host'],
											port = self.snap_tool_conf['es_port'],
											connection_class = RequestsHttpConnection,
											http_auth = (self.utils.decryptAES(self.snap_tool_conf['http_auth_user']).decode('utf-8'), self.utils.decryptAES(self.snap_tool_conf['http_auth_pass']).decode('utf-8')),
											use_ssl = True,
											verify_certs = False,
											ssl_show_warn = False)
				else:
					context = create_default_context(cafile = self.snap_tool_conf['path_certificate'])
					conn_es = Elasticsearch(self.snap_tool_conf['es_host'],
											port = self.snap_tool_conf['es_port'],
											connection_class = RequestsHttpConnection,
											http_auth = (self.utils.decryptAES(self.snap_tool_conf['http_auth_user']).decode('utf-8'), self.utils.decryptAES(self.snap_tool_conf['http_auth_pass']).decode('utf-8')),
											use_ssl = True,
											verify_certs = True,
											ssl_context = context)
			if not conn_es == None:
				self.logger.createSnapToolLog("Established connection with: " + self.snap_tool_conf['es_host'] + ':' + str(self.snap_tool_conf['es_port']), 1)
		except (KeyError, exceptions.ConnectionError, exceptions.AuthenticationException, exceptions.AuthorizationException, InvalidURL) as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox("\nFailed to connect to ElasticSearch. For more information, see the logs.", 8, 50, title = "Error Message")
			exit(1)
		else:
			return conn_es

	"""
	Method that creates a snapshot in ElasticSearch.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Name of the repository where the snapshots will be saved.
	index_name -- Name of the index that will be backed up.
	form_dialog -- A FormDialogs class object.

	Exceptions:
	exceptions.RequestError -- Exception representing a 400 status code. 
	exceptions.NotFoundError -- Exception representing a 404 status code.
	"""
	def createSnapshot(self, conn_es, repository_name, index_name, form_dialog):
		try:
			conn_es.snapshot.create(repository = repository_name, snapshot = index_name, body = { "indices" : index_name, "include_global_state" : False }, wait_for_completion = False)
		except exceptions.RequestError as exception:
			self.logger.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nFailed to create snapshot. For more information, see the logs.", 7, 50, title = "Error message")
			form_dialog.mainMenu()
		except exceptions.NotFoundError as exception:
			self.logger.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nFailed to create snapshot. For more information, see the logs.", 7, 50, title = "Error message")
			form_dialog.mainMenu()
		except exceptions.AuthorizationException as exception:
			self.logger.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nFailed to create snapshot. For more information, see the logs.", 7, 50, title = "Error message")
			form_dialog.mainMenu()


	"""
	Method that obtains the status of a snapshot.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Name of the repository where the snapshots will be saved.
	snapshot_name -- Name of the snapshot from which its status will be validated.
	form_dialog -- A FormDialogs class object.

	Return:
	status_snapshot -- Current state of the snapshot.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	"""
	def getStatusSnapshot(self, conn_es, repository_name, snapshot_name, form_dialog):
		try:
			status_aux = conn_es.snapshot.status(repository = repository_name, snapshot = snapshot_name)
			status_snapshot = status_aux['snapshots'][0]['state']
			return status_snapshot
		except exceptions.NotFoundError as exception:
			self.logger.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nFailed to get snapshot status. For more information, see the logs.", 7, 50, title = "Error message")
			form_dialog.mainMenu()

	"""
	Method that obtains the final status of a snapshot.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Name of the repository where the snapshots will be saved.
	snapshot_name -- Name of the snapshot from which its status will be validated.
	form_dialog -- A FormDialogs class object.

	Return:
	status_aux -- Current state of the snapshot.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	"""
	def getStatus(self, conn_es, repository_name, snapshot_name, form_dialog):
		try:
			status_aux = conn_es.snapshot.get(repository = repository_name, snapshot = snapshot_name)
			return status_aux
		except exceptions.NotFoundError as exception:
			self.logger.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nFailed to get snapshot status. For more information, see the logs.", 7, 50, title = "Error message")
			form_dialog.mainMenu()

	"""
	Method that gets the list of all snapshots created in the repository.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Name of the repository where the snapshots will be saved.
	form_dialog -- A FormDialogs class object.

	Return:
	list_snapshots -- List with all snapshots found.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	"""
	def getSnapshots(self, conn_es, repository_name, form_dialog):
		list_snapshots = []
		list_aux = []		
		try:
			list_snapshots_aux = conn_es.snapshot.get(repository = repository_name, snapshot = '_all')
			for snapshots_aux in list_snapshots_aux['snapshots']:
				list_aux.append(snapshots_aux['snapshot'])
			list_aux = sorted(list_aux)
			for snapshot in list_aux:
				list_snapshots.append((snapshot, "Snapshot Name", 0))
			return list_snapshots
		except exceptions.NotFoundError as exception:
			self.logger.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nFailed to get snapshot list. For more information, see the logs.", 7, 50, title = "Error message")
			form_dialog.mainMenu()

	"""
	Method that removes a snapshot in ElasticSearch.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Name of the repository where the snapshots will be saved.
	snapshot_name -- Name of the snapshot to delete.
	form_dialog -- A FormDialogs class object.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	"""
	def deleteSnapshot(self, conn_es, repository_name, snapshot_name, form_dialog):
		try:
			conn_es.snapshot.delete(repository = repository_name, snapshot = snapshot_name, request_timeout = 7200)
		except exceptions.NotFoundError as exception:
			self.logger.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nFailed to delete snapshot(s). For more information, see the logs.", 7, 50, title = "Error message")
			form_dialog.mainMenu()
		except exceptions.AuthorizationException as exception:
			self.logger.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nFailed to delete snapshot(s). For more information, see the logs.", 7, 50, title = "Error message")
			form_dialog.mainMenu()
			

	"""
	Method that mounts a snapshot created as a searchable snapshot.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Name of the repository where the snapshot to mount is located.
	snapshot_name -- Name of the snapshot to mount.
	form_dialog -- A FormDialogs class object.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	"""
	def mountSearchableSnapshots(self, conn_es, repository_name, snapshot_name, form_dialog):
		try:
			conn_es.searchable_snapshots.mount(repository = repository_name, snapshot = snapshot_name, body = { "index" : snapshot_name }, wait_for_completion = True, request_timeout = 7200)
		except exceptions.NotFoundError as exception:
			self.logger.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nFailed to mount snapshot as a searchable snapshot. For more information, see the logs.", 7, 50, title = "Error message")
			form_dialog.mainMenu()
		except exceptions.AuthorizationException as exception:
			self.logger.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nFailed to mount snapshot as a searchable snapshot. For more information, see the logs.", 7, 50, title = "Error message")
			form_dialog.mainMenu()

	"""
	Method that obtains the list of existing indices in ElasticSearch.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.

	Return:
	list_indices -- List containing all the indices found.
	"""
	def getIndices(self, conn_es):
		list_indices = []
		list_indices_aux = conn_es.indices.get('*')
		list_indices_aux = sorted([index for index in list_indices_aux if not index.startswith(".")])
		for index_aux in list_indices_aux:
			list_indices.append((index_aux, "Index Name", 0))
		return list_indices

	"""
	Method that obtains the percentage of occupied disk space
	of the nodes of the elasticsearch cluster.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to
			   ElasticSearch.

	Exceptions:
	exceptions.AuthorizationException -- Exception representing
	  									 a 403 status code.
	"""
	def getNodesDiskSpace(self, conn_es):
		try:
			message = "Occupied space in nodes:\n\n"
			nodes_info = conn_es.nodes.stats(metric = 'fs')['nodes']
			for node in nodes_info:
				message += "- " + nodes_info[node]['name'] + "\n"
				total_disk = nodes_info[node]['fs']['total']['total_in_bytes']
				available_disk = nodes_info[node]['fs']['total']['available_in_bytes']
				percentage = 100 - (available_disk * 100 / total_disk)
				message += "Percent occupied on disk: " + str(round(percentage, 2)) + "%\n\n"
			self.form_dialog.getScrollBox(message, "Node Information")
		except exceptions.AuthorizationException as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox("\nError when obtaining the information of the nodes. For more information, see the logs.", 8, 50, title = "Error Message")
			self.form_dialog.mainMenu()

	"""
	Method that removes an index in ElasticSearch.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	index_name -- Name of the index to remove.
	"""
	def deleteIndex(self, conn_es, index_name):
		conn_es.indices.delete(index = index_name)