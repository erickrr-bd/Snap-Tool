from sys import exit, warnoptions
from modules.UtilsClass import Utils
from ssl import create_default_context
from modules.LoggerClass import Logger
from requests.exceptions import InvalidURL
from elasticsearch import Elasticsearch, RequestsHttpConnection, exceptions	

"""
Class that allows you to manage everything related to ElasticSearch.
"""
class Elastic:
	"""
	Disable warning message.
	"""
	if not warnoptions:
		from warnings import simplefilter
		simplefilter("ignore")
	
	"""
	Property that stores an object of type Utils.
	"""
	utils = None

	"""
	Property that stores an object of type Logger.
	"""
	logger = None

	"""
	Property that stores an object of type FormDialog.
	"""
	form_dialog = None

	"""
	Property that stores the information defined in the Snap-Tool configuration file.
	"""
	snap_tool_conf = None

	"""
	Constructor for the Elastic class.

	Parameters:
	self -- An instantiated object of the Elastic class.
	form_dialog -- FormDialog class object.
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
	conn_es -- Object that contains the connection to ElasticSearch.

	Exceptions:
	KeyError -- A Python KeyError exception is what is raised when you try to access a key that isn’t in a dictionary (dict). 
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES. 
	exceptions.AuthenticationException -- Exception representing a 401 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	requests.exceptions.InvalidURL -- The URL provided was somehow invalid.
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
			self.form_dialog.d.msgbox(text = "\nFailed to connect to ElasticSearch. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			exit(1)
		else:
			return conn_es

	"""
	Method that creates a repository type FS.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Name of the repository.
	path_repository -- Repository path.
	compress_repository -- Whether the metadata files are stored compressed.

	Exceptions:
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES.
	exceptions.TransportError -- Exception raised when ES returns a non-OK (>=400) HTTP status code. Or when an actual connection error happens; in that case the status_code will be set to 'N/A'.
	"""
	def createRepositoryFS(self, conn_es, repository_name, path_repository, compress_repository):
		try:
			conn_es.snapshot.create_repository(repository = repository_name,
											   body = { "type": "fs", "settings": { "location": path_repository, "compress" : compress_repository }})
		except (exceptions.AuthorizationException, exceptions.ConnectionError, exceptions.TransportError) as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nError creating repository. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()

	"""
	Method that removes a repository type FS.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Name of the repository to delete.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES.
	"""
	def deleteRepositoryFS(self, conn_es, repository_name):
		try:
			conn_es.snapshot.delete_repository(repository = repository_name)
		except (exceptions.NotFoundError, exceptions.AuthorizationException, exceptions.ConnectionError) as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nFailed to delete repository. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()

	"""
	Method that creates a snapshot of an index.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Repository where the snapshot will be stored.
	index_name -- Name of the index to be backed up in the snapshot.

	Exceptions:
	exceptions.RequestError -- Exception representing a 400 status code. 
	exceptions.NotFoundError -- Exception representing a 404 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES.
	"""
	def createSnapshot(self, conn_es, repository_name, index_name):
		try:
			conn_es.snapshot.create(repository = repository_name, snapshot = index_name, body = { 'indices' : index_name, "include_global_state" : False }, wait_for_completion = False)
		except (exceptions.AuthorizationException, exceptions.RequestError, exceptions.NotFoundError, exceptions.ConnectionError) as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nFailed to create snapshot. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()

	"""
	Method that removes a snapshot.

	Parameters:
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Name of the repository where the snapshot to delete is stored.
	snapshot_name -- Name of the snapshot to delete.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES.
	"""
	def deleteSnapshotElastic(self, conn_es, repository_name, snapshot_name):
		try:
			conn_es.snapshot.delete(repository = repository_name, snapshot = snapshot_name, request_timeout = 7200)
		except (exceptions.NotFoundError, exceptions.AuthorizationException, exceptions.ConnectionError) as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nFailed to delete snapshot. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()

	"""
	Method that restores a snapshot.

	Parameters:
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Repository where the snapshot is stored.
	snapshot_name -- Name of the snapshot to restore.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES.
	"""
	def restoreSnapshot(self, conn_es, repository_name, snapshot_name):
		try:
			conn_es.snapshot.restore(repository = repository_name, snapshot = snapshot_name)
		except (exceptions.NotFoundError, exceptions.AuthorizationException, exceptions.ConnectionError) as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nFailed to restore snapshot. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()

	"""
	Method that mounts a snapshot as a searchable snapshot.

	Parameters:
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Name of the repository where the snapshot that will be mounted as a searchable snapshot is stored.
	snapshot_name -- Name of the snapshot to be mounted as a searchable snapshot.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES.
	"""
	def mountSearchableSnapshot(self, conn_es, repository_name, snapshot_name):
		try:
			conn_es.searchable_snapshots.mount(repository = repository_name, snapshot = snapshot_name, body = { "index" : snapshot_name }, wait_for_completion = False, request_timeout = 7200)
		except (exceptions.NotFoundError, exceptions.AuthorizationException, exceptions.ConnectionError) as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nFailed to mount snapshot as a searchable snapshot. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()

	"""
	Method that removes an index from ElasticSearch.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	index_name -- Name of the index to be removed.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES.
	"""
	def deleteIndex(self, conn_es, index_name):
		try:
			conn_es.indices.delete(index = index_name)
		except (exceptions.NotFoundError, exceptions.AuthorizationException, exceptions.ConnectionError) as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nFailed to delete index. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()
			
	"""
	Method that gets the status of a snapshot.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Repository where the snapshot is stored.
	snapshot_name -- Name of the snapshot from which the status will be obtained.

	Return:
	status_snapshot -- Status of the snapshot.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES.
	"""
	def getStatusSnapshot(self, conn_es, repository_name, snapshot_name):
		try:
			status_aux = conn_es.snapshot.status(repository = repository_name, snapshot = snapshot_name)
			status_snapshot = status_aux['snapshots'][0]['state']
		except (exceptions.NotFoundError, exceptions.AuthorizationException, exceptions.ConnectionError) as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nFailed to get snapshot status. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return status_snapshot

	"""
	Method that gets the status of a snapshot.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Repository where the snapshot is stored.
	snapshot_name -- Name of the snapshot from which the information will be obtained.

	Return:
	snapshot_info -- Information obtained from the snapshot.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES.
	"""
	def getSnapshotInfo(self, conn_es, repository_name, snapshot_name):
		try:
			snapshot_info = conn_es.snapshot.get(repository = repository_name, snapshot = snapshot_name)
		except (exceptions.NotFoundError, exceptions.AuthorizationException, exceptions.ConnectionError) as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nFailed to get snapshot status. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return snapshot_info

	"""
	Method that obtains a list with the names of the ElasticSearch indexes.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.

	Return:
	list_all_indices -- List with the names of the indices found.

	Exceptions:
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES.
	"""
	def getIndices(self, conn_es):
		list_all_indices = []
		try:
			list_all_indices = conn_es.indices.get('*')
			list_all_indices = sorted([index for index in list_all_indices if not index.startswith(".")])
		except (exceptions.AuthorizationException, exceptions.ConnectionError) as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nFailed to get created repositories. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return list_all_indices

	"""
	Method that gets a list of all the snapshots created so far.

	Parameters:
	conn_es -- Object that contains the connection to ElasticSearch.
	repository_name -- Repository where the snapshots are stored.

	Return:
	list_all_snapshots -- List with the names of all snapshots found in the repository.

	Exceptions:
	exceptions.NotFoundError -- Exception representing a 404 status code.
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES.
	"""
	def getAllSnapshots(self, conn_es, repository_name):
		list_all_snapshots = []
		try:
			snapshots_info = conn_es.snapshot.get(repository = repository_name, snapshot = '_all')
			for snapshot in snapshots_info['snapshots']:
				list_all_snapshots.append(snapshot['snapshot'])
			list_all_snapshots = sorted(list_all_snapshots)
		except (exceptions.NotFoundError, exceptions.AuthorizationException, exceptions.ConnectionError) as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nFailed to get snapshots. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return list_all_snapshots

	"""
	Method that gets the repositories created in ElasticSearch.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.

	Return:
	list_all_repositories -- List with the names of the repositories found.

	Exceptions:
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES.
	"""
	def getAllRepositories(self, conn_es):
		list_all_repositories = []
		try:
			repositories_info = conn_es.cat.repositories(format = "json")
			for repository in repositories_info:
				list_all_repositories.append(repository['id'])
		except (exceptions.AuthorizationException, exceptions.ConnectionError) as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nFailed to get created repositories. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return list_all_repositories

	"""
	Method that obtains information related to the disk space corresponding to the nodes belonging to the elasticsearch cluster.

	Parameters:
	self -- An instantiated object of the Elastic class.
	conn_es -- Object that contains the connection to ElasticSearch.

	Exceptions:
	exceptions.AuthorizationException -- Exception representing a 403 status code.
	exceptions.ConnectionError --  Error raised when there was an exception while talking to ES.
	"""
	def getNodesInformation(self, conn_es):
		try:
			nodes_info = conn_es.nodes.stats(metric = 'fs')['nodes']
		except (exceptions.AuthorizationException, exceptions.ConnectionError) as exception:
			self.logger.createSnapToolLog(exception, 3)
			self.form_dialog.d.msgbox(text = "\nError when obtaining the information of the nodes. For more information, see the logs.", height = 8, width = 50, title = "Error Message")
			self.form_dialog.mainMenu()
		else:
			return nodes_info