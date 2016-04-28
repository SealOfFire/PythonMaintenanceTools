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

		# 读取导出数据部分设置
		self.LoadExportInfo()
		
		#读取导入数据部分设置
		self.LoadImportInfo()


	def LoadExportInfo(self):
		'''
		读取导出数据部分设置
		'''
		Logger.info("ConfigHandle dumpInfo [start]")
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
			for schemaNode in server.findall('schema'):
				schemaName = schemaNode.get('name')
				schemaInfo = {'procedures':{},'functions':{}}
				# 存储过程配置
				proceduresNode = schemaNode.find('procedures')
				for procedureNode in proceduresNode.findall('procedure'):
					schemaInfo['procedures'][procedureNode.text] = ''
				# 函数配置
				functionsNode = schemaNode.find('functions')
				for functionNode in functionsNode.findall('function'):
					schemaInfo['functions'][functionNode.text] = ''
				# 表
				# schema综合
				serverInfo['schemas'][schemaName] = schemaInfo

			self.dumpInfo['servers'].append(serverInfo)
		Logger.info("ConfigHandle dumpInfo [end]")


	def LoadImportInfo(self):
		'''
		读取导入数据部分设置
		'''
		Logger.info("ConfigHandle importInfo [begin]")
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
			for schemaNode in server.findall("schema"):
				schemaName = schemaNode.get("name")
				schemaInfo = {'procedures':{},'functions':{}}
				# serverInfo['schemas'][schemaName] = []
				# 存储过程配置
				proceduresNode = schemaNode.find('procedures')
				for procedureNode in proceduresNode.findall('procedure'):
					exists,procedureFullName = self.Exists(self.ImportInfo['home'],procedureNode.text)
					if exists:
						schemaInfo['procedures'][procedureNode.text] = procedureFullName
				# 函数配置
				functionsNode = schemaNode.find('functions')
				for functionNode in functionsNode.findall('function'):
					exists,functionFullName = self.Exists(self.ImportInfo['home'],functionNode.text)
					if exists:
						schemaInfo['functions'][functionNode.text] = functionFullName
				# 表
				# schema综合
				serverInfo['schemas'][schemaName] = schemaInfo
			self.ImportInfo['servers'].append(serverInfo)
		Logger.info("ConfigHandle importInfo [end]")


	def Exists(self,home, fileName):
		'''
		判断文件存在
		'''
		fullFileName = os.path.join(home,fileName)
		if os.path.exists(fullFileName):
			return True,fullFileName
		else:
			portion = os.path.splitext(fullFileName)
			fullFileName = portion[0] + ".sql"
			if os.path.exists(fullFileName):
				return True,fullFileName
			else:
				fullFileName = portion[0] + ".txt"
				if os.path.exists(fullFileName):
					return True,fullFileName
				else:
					Logger.error("file not exist [%s]" % portion[0])
					return False,''


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