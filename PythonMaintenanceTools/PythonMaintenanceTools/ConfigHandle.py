#coding:utf-8
import os
import xml.etree.ElementTree as ET 
from LogHandle import Logger

class ConfigHandle():
	'''
	配置文件处理
	'''

	tree = ET.parse("config.xml")
	root = tree.getroot()
	dumpInfo = {}
	ImportInfo = {}

	def __init__(self):
		'''
		构造函数
		'''
		Logger.debug("ConfigHandle load config.xml")
		self.tree = ET.parse('config.xml')
		self.root = self.tree.getroot()

		Logger.debug("ConfigHandle dumpInfo [start]")
		dumpInfoNode = self.root.find('DumpInfo')
		self.dumpInfo['home'] = dumpInfoNode.get('home')
		self.dumpInfo['servers'] = []
		for server in dumpInfoNode.findall('server'):
			host, user, password, port = ConfigHandle.GetMySQLConnectionInfo(server)
			serverInfo = {'host':host
				, 'user':user
				, 'password':password
				, 'port':port
				,'schemas':{}}
			for schema in server.findall("schema"):
				schemaName = schema.get("name")
				serverInfo['schemas'][schemaName] = []
				for procedure in schema.findall("procedure"):
					serverInfo['schemas'][schemaName].append(procedure.text)
			self.dumpInfo['servers'].append(serverInfo)

		Logger.debug("ConfigHandle dumpInfo [end]")
		
		Logger.debug("ConfigHandle importInfo [begin]")
		importInfoNode = self.root.find("ImportInfo")
		self.ImportInfo['home'] = importInfoNode.find("from").text
		to = importInfoNode.find("to")
		self.ImportInfo['servers'] = []
		for server in to.findall("server"):
			host, user, password, port = ConfigHandle.GetMySQLConnectionInfo(server)
			serverInfo = {'host':host
				, 'user':user
				, 'password':password
				, 'port':port
				,'schemas':{}}
			for schema in server.findall("schema"):
				schemaName = schema.get("name")
				serverInfo['schemas'][schemaName] = []
				for procedure in schema.findall("procedure"):
					procedureName = procedure.text
					procedureName = os.path.join(self.ImportInfo['home'],procedureName)
					if os.path.exists(procedureName):
						serverInfo['schemas'][schemaName].append(procedureName)
					else:
						portion = os.path.splitext(procedureName)
						procedureName = portion[0] + ".sql"
						if os.path.exists(procedureName):
							serverInfo['schemas'][schemaName].append(procedureName)
						else:
							procedureName = portion[0] + ".txt"
							if os.path.exists(procedureName):
								serverInfo['schemas'][schemaName].append(procedureName)
							else:
								Logger.error("procedure not exist [%s]" % portion[0])
			self.ImportInfo['servers'].append(serverInfo)
		Logger.info("导入[结束]")
		Logger.debug("ConfigHandle importInfo [end]")


	@classmethod
	def GetMySQLConnectionInfo(self,node):
		'''
		获取mysql服务器配置信息
		'''
		host = node.get("host")
		user = node.get("username")
		password = node.get("password")
		port = int(node.get("port"))
		return host,user,password,port