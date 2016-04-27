#coding:utf-8
import sys
import os
import mysql.connector
import datetime
import codecs
from mysql.connector import errorcode
import xml.etree.ElementTree as ET 
from LogHandle import Logger
from ConfigHandle import ConfigHandle

reload(sys)
sys.setdefaultencoding('utf-8')

class MySqlHandle():
	'''
	mysql 执行
	'''

	def MySqlDump(host,username,password,post,schema,outputPath):
		'''
		mysql数据库导出
		'''
		# print("aaa");
		''' 
		mysqldump -u 数据库用户名 -p -n -t -d -R 数据库名 > 文件名
		mysqldump.exe -h192.168.1.1 -uroot -proot -n -d -t -R mydb>d:/b.sql
		-n: --no-create-db
		-d: --no-data
		-t: --no-create-info
		-R: --routines Dump stored routines 
		'''
		cmd = "%s -h %s -u %s -p%s -P %d -n -d -t %s> %s" % (MySqlEnvironment.GetMySqlDumpPath(),host,username,password,post,schema,outputPath)
		Logger.info("执行mysql导出" + cmd)


	def MySQLCreateConnect(host,user,password,port):
		'''
		创建MySQL数据库连接
		'''
		connect = None
		try:
			connect = mysql.connector.connect(host=host,user=username,password=password,port=port)
			# cursor = cnx.cursor()
			# cursor.execute(query)
			#cursor.close()
		except mysql.connector.Error as err:
			Logger.error(err)
		else:
			pass
			# connect.close()
		return connect


	def MySQLExecuteQuery(connect,schema,query):
			'''
			执行查询语句
			'''
			# 执行是否成功
			result = False
			try:
				Logger.debug("执行查询语句[开始]")
				connect.database = schema
				cursor = connect.cursor()
				for result in cursor.execute(query, multi=True):
					if result.with_rows:
						Logger.info("Rows produced by statement '{}':".format(result.statement))
						Logger.info(result.fetchall())
					else:
						Logger.info("Number of rows affected by statement '{}': {}".format(result.statement, result.rowcount))
				cursor.close()
				Logger.debug("执行查询语句[结束]")
				result = True
			except mysql.connector.Error as err:
				Logger.error(err)
				result = False
			else:
				connect.close()
			return result


	@classmethod
	def MySQLWriteProcedureToFile(self,home,host,schema,procedure,ddl):
		'''
		文本写到文件上
		'''
		Logger.info("write procedure to file [begin]")
		homeTemp = os.path.join(home,host)
		homeTemp = os.path.join(home,host)
		homeTemp = os.path.join(homeTemp,schema)
		homeTemp = os.path.join(homeTemp, datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
		if not os.path.exists(homeTemp):
			os.makedirs(homeTemp)
			Logger.debug("MySQLWriteProcedureToFile 文件夹不存在,创建文件夹")
		homeTemp = os.path.join(homeTemp,procedure + ".sql")
		# f = open(home, 'w')
		f = codecs.open(homeTemp,"w","utf-8")
		Logger.debug("MySQLWriteProcedureToFile 打开文件[%s]" % homeTemp)
		# ddl.decode("utf-8")
		f.write("DROP procedure IF EXISTS `%s`;\n " % procedure,)
		#f.write("DELIMITER $$\n")
		f.write(ddl)
		f.write(';')
		#f.write("$$\nDELIMITER ;")
		f.close()
		Logger.debug("MySQLWriteProcedureToFile 关闭文件[%s]" % homeTemp)
		Logger.info("write procedure to file [end]")


	@classmethod
	def MySQLDumpProcedure(self):
		'''
		导出存储过程
		'''
		Logger.debug("DumpProcedure [begin]")
		dumpInfo = ConfigHandle().dumpInfo
		home = dumpInfo['home']
		Logger.debug("DumpProcedure 导出文件保存根路径[%s]" % home)

		Logger.info("export procedure [begin]")
		Logger.debug("DumpProcedure 遍历所有服务器")
		for server in dumpInfo['servers']:
			Logger.debug("DumpProcedure 服务器基本信息[%s] [%s] [%s] [%s]" % (server['host'], server['user'], server['password'], server['port']))
			try:
				cnx = mysql.connector.connect(host=server['host'],user=server['user'],password=server['password'],port=server['port'])
				Logger.debug("DumpProcedure create cnx")
				Logger.info("connect [open]-[%s]" % server['host'])
				cursor = cnx.cursor()
				Logger.info("cursor [open]")
				for schema,procedures in server['schemas'].items():
					cnx.database = schema
					for procedure in procedures:
						query = ("show create procedure %s" % procedure)
						Logger.info("export procedure [begin] [%s] [%s] [%s]" % (server['host'],schema,procedure))
						cursor.execute(query)
						row = cursor.fetchone()
						procedureDDL = row[2]
						Logger.info("export procedure [end] [%s] [%s] [%s]" % (server['host'],schema,procedure))
						
						MySqlHandle.MySQLWriteProcedureToFile(home,server['host'],schema,procedure,procedureDDL)
				cursor.close()
				Logger.info("cursor [close]")
			except mysql.connector.Error as err:
				Logger.error(err)
			else:
				cnx.close()
				Logger.info("connect [close]-[%s]" % server['host'])

		Logger.info("export procedure [end]")
		Logger.debug("DumpProcedure [end]")


	@classmethod
	def MySQLImportProcedure(self):
		'''
		导入存储过程
		'''
		Logger.debug("MySQLImportProcedure [begin]")
		ImportInfo = ConfigHandle().ImportInfo
		for server in ImportInfo['servers']:
			Logger.debug("MySQLImportProcedure 服务器基本信息[%s] [%s] [%s] [%s]" % (server['host'], server['user'], server['password'], server['port']))
			try:
				cnx = mysql.connector.connect(host=server['host'],user=server['user'],password=server['password'],port=server['port'])
				Logger.info("connect [open]-[%s]" % server['host'])
				Logger.debug("MySQLImportProcedure create cnx")
				cursor = cnx.cursor()
				Logger.info("cursor [open]")
				for schema,procedures in server['schemas'].items():
					cnx.database = schema
					for procedure in procedures:
						f = codecs.open(procedure,"r","utf-8")
						ddl = f.read()
						f.close()
						Logger.info("procedure import [begin] %s" % (schema))
						for result in cursor.execute(ddl, multi=True):
							if result.with_rows:
								#Logger.info("Rows produced by statement
								#'{}':".format(result.statement))
								Logger.info(result.fetchall())
							else:
								pass
								#Logger.info("Number of rows affected by statement '{}':
								#{}".format(result.statement, result.rowcount))
						Logger.info("procedure import [end] %s" % (schema))
				cursor.close()
				Logger.info("cursor [close]")
			except mysql.connector.Error as err:
				Logger.error(err)
			else:
				cnx.close()
				Logger.info("connect [close]-[%s]" % server['host'])
		Logger.debug("MySQLImportProcedure [end]")