#coding:utf-8
# from LogHandle import Logger
import sys
import getopt
from MySQL.MySqlHandle import MySqlHandle

if __name__ == "__main__":
	opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
	for op, value in opts:
		if op == "-i":
			MySqlHandle.MySQLImportProcedure()
		elif op == "-o":
			MySqlHandle.MySQLDumpProcedure()
		elif op == "-h":
			print("-i 导入, -o导出")
			# usage()
			sys.exit()
