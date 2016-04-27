#coding:utf-8
class ServerInfo:
	'''
	服务器信息
	'''
	host = "localhost"
	username = "root"
	password = "root"
	port = 3306

	def __init__(self, host,username,password,post):
		self.host = host
		self.username = username
		self.password = password
		self.post = post


dumpSource = []


class MySqlDataSource():
	'''
	mysql 数据源设置
	'''
	# 源服务器
	soruce = [ServerInfo("192.168.1.1","root", "root" ,3306)
		,ServerInfo("192.168.1.1","root", "root" ,3306)]

	soruceP = {"schema":["PROCEDURE1","PROCEDURE1"]}

	# 目标服务器
	target = [ServerInfo("192.168.1.1","root", "root" ,3306)
		,ServerInfo("192.168.1.1","root", "root" ,3306)]