#coding:utf-8
import os
from LogHandle import Logger

class MySqlEnvironment:
	'''
	mysql 环境配置信息
	'''
	# mysql的路径
	home = "C:\Program Files\MySQL\MySQL Server 5.7"

	# mysql命令
	mysql = "mysql.exe"

	# 导出数据命令
	mysqldump = "mysqldump.exe"

	@classmethod
	def GetMySqlPath(self):
		"""
		获取mysql命令
		"""
		path = os.path.join(MySqlEnvironment.home,"bin")
		path = os.path.join(path,MySqlEnvironment.mysql)
		Logger.info("mysql所在路径" + path)
		return path

	@classmethod
	def GetMySqlDumpPath(self):
		"""
		获取MySqlDump命令
		"""
		path = os.path.join(MySqlEnvironment.home,"bin")
		path = os.path.join(path,MySqlEnvironment.mysqldump)
		Logger.info("mysqldump所在路径" + path)
		return path