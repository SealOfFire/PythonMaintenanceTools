#coding:utf-8
import unittest

class Test_test1(unittest.TestCase):

	 ##初始化工作
	def setUp(self): 
		pass
	#退出清理工作
	def tearDown(self): 
		pass

	def test_GetMySqlPath(self):
		from MySqlEnvironment import MySqlEnvironment
		MySqlEnvironment.GetMySqlPath()

	def test_GetMySqlDumpPath(self):
		from MySqlEnvironment import MySqlEnvironment
		MySqlEnvironment.GetMySqlDumpPath()

	def test_DumpProcedure(self):
		from MySqlHandle import MySqlHandle
		MySqlHandle.DumpProcedure()

if __name__ == '__main__':
	# unittest.main()
	test=Test_test1()
	test.test_DumpProcedure()
