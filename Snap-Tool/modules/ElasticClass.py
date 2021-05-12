import sys
import requests
from modules.UtilsClass import Utils
from ssl import create_default_context
from modules.LoggerClass import Logger
from elasticsearch import Elasticsearch, RequestsHttpConnection, exceptions	

"""
Class that allows you to manage everything related to ElasticSearch.
"""
class Elastic:
	"""
	Disable warning message.
	"""
	if not sys.warnoptions:
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
	Constructor for the Elastic class.

	Parameters:
	self -- An instantiated object of the Elastic class.
	"""
	def __init__(self):
		self.utils = Utils()
		self.logger = Logger()

	"""
	Method that establishes the connection of Telk-Alert with ElasticSearch.

	Parameters:
	self -- An instantiated object of the Elastic class.
	snap_tool_conf -- List containing all the information in the Telk-Alert configuration file.
	form_dialog -- A FormDialogs class object.

	Return:
	conn_es -- Object that contains the connection to ElasticSearch.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES. 
	exceptions.AuthenticationException -- Exception representing a 401 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	requests.exceptions.InvalidURL -- The URL provided was somehow invalid
	"""
	def getConnectionElastic(self, snap_tool_conf, form_dialog):
		try:
			if (not snap_tool_conf['use_ssl'] == True) and (not snap_tool_conf['use_http_auth'] == True):
				conn_es = Elasticsearch([snap_tool_conf['es_host']], 
										port = snap_tool_conf['es_port'],
										connection_class = RequestsHttpConnection,
										use_ssl = False)
			if (not snap_tool_conf['use_ssl'] == True) and snap_tool_conf['use_http_auth'] == True:
				conn_es = Elasticsearch([snap_tool_conf['es_host']], 
										port = snap_tool_conf['es_port'],
										connection_class = RequestsHttpConnection,
										http_auth = (self.utils.decryptAES(snap_tool_conf['http_auth_user']).decode('utf-8'), self.utils.decryptAES(snap_tool_conf['http_auth_pass']).decode('utf-8')),
										use_ssl = False)
			if snap_tool_conf['use_ssl'] == True and (not snap_tool_conf['use_http_auth'] == True):
				if not snap_tool_conf['valid_certificates'] == True:
					conn_es = Elasticsearch([snap_tool_conf['es_host']], 
											port = snap_tool_conf['es_port'],
											connection_class = RequestsHttpConnection,
											use_ssl = True,
											verify_certs = False,
											ssl_show_warn = False)
				else:
					context = create_default_context(cafile = snap_tool_conf['path_cert'])
					conn_es = Elasticsearch([snap_tool_conf['es_host']], 
											port = snap_tool_conf['es_port'],
											connection_class = RequestsHttpConnection,
											http_auth = (self.utils.decryptAES(snap_tool_conf['http_auth_user']).decode('utf-8'), self.utils.decryptAES(snap_tool_conf['http_auth_pass']).decode('utf-8')),
											use_ssl = True,
											verify_certs = True,
											ssl_context = context)
			if snap_tool_conf['use_ssl'] == True and snap_tool_conf['use_http_auth'] == True:
				if not snap_tool_conf['valid_certificates'] == True:
					conn_es = Elasticsearch([snap_tool_conf['es_host']], 
											port = snap_tool_conf['es_port'],
											connection_class = RequestsHttpConnection,
											http_auth = (self.utils.decryptAES(snap_tool_conf['http_auth_user']).decode('utf-8'), self.utils.decryptAES(snap_tool_conf['http_auth_pass']).decode('utf-8')),
											use_ssl = True,
											verify_certs = False,
											ssl_show_warn = False)
				else:
					context = create_default_context(cafile = snap_tool_conf['path_cert'])
					conn_es = Elasticsearch([snap_tool_conf['es_host']], 
											port = snap_tool_conf['es_port'],
											connection_class = RequestsHttpConnection,
											http_auth = (self.utils.decryptAES(snap_tool_conf['http_auth_user']).decode('utf-8'), self.utils.decryptAES(snap_tool_conf['http_auth_pass']).decode('utf-8')),
											use_ssl = True,
											verify_certs = True,
											ssl_context = context)
			if conn_es.ping():
				self.logger.createLogTool("Connection established to: " + snap_tool_conf['es_host'] + ':' + str(snap_tool_conf['es_port']), 2)
				return conn_es
		except KeyError as exception:
			self.logger.createLogTool("Key Error: " + str(exception), 4)
			form_dialog.d.msgbox("\nKey Error: " + str(exception), 7, 50, title = "Error message")
			sys.exit(1)
		except exceptions.ConnectionError as exception:
			self.logger.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nFailed connection to: " + snap_tool_conf['es_host'] + ':' + str(snap_tool_conf['es_port']) + '. For more information, see the logs.', 7, 50, title = "Error message")
			sys.exit(1)
		except exceptions.AuthenticationException as exception:
			self.logger.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nAuthentication failed. For more information, see the logs.", 7, 50, title = "Error message")
			sys.exit(1)
		except exceptions.AuthorizationException as exception:
			self.logger.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nUnauthorized access. For more information, see the logs.", 7, 50, title = "Error message")
			sys.exit(1)
		except requests.exceptions.InvalidURL as exception:
			form_dialog.d.msgbox("\nInvalid URL. For more information, see the logs.", 7, 50, title = "Error message")
			self.logger.createLogTool(str(exception), 4)
			sys.exit(1)

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
			conn_es.snapshot.create(repository = repository_name, snapshot = index_name, body = { "indices": index_name }, wait_for_completion = True, request_timeout = 7200)
		except exceptions.RequestError as exception:
			self.logger.createLogTool(str(exception), 4)
			form_dialog.d.msgbox("\nFailed to create snapshot. For more information, see the logs.", 7, 50, title = "Error message")
			form_dialog.mainMenu()
		except exceptions.NotFoundError as exception:
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
	Method that removes an index in ElasticSearch.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	index_name -- Name of the index to remove.
	"""
	def deleteIndex(self, conn_es, index_name):
		conn_es.indices.delete(index = index_name)