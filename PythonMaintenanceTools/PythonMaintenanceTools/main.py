#coding:utf-8
# from LogHandle import Logger
#import sys
#import getopt
#from MySQL.MySqlHandle import MySqlHandle

from ConfigHandle import ConfigHandle
import argparse
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description='data base tools',formatter_class=RawTextHelpFormatter)
parser.add_argument('-o','--operate',choices=['me','mi'],default='me',help='operate type,\n	me:MySQL database export\n	mi:MySQL database import')
parser.add_argument('-mc','--mysqlconfig',default='MySQL/MySQLConfig.xml',help='MySQL congfig file path')
args = parser.parse_args()
# print args.mysqlconfig
# print args.operate
if args.operate == 'me':
	# mysql 数据库导出操作
	# 读取mysql配置文件
	pass
elif args.operate == 'mi':
	# mysql 数据库导入操作
	# 读取mysql配置文件
	pass
mySQLConfig = ConfigHandle(args.mysqlconfig)

'''
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,help="display a square of a given number")
# parser.add_argument("-v", "--verbosity", type=int,choices=[0, 1,
# 2],help="increase output verbosity")
parser.add_argument("-v", "--verbosity", action="count",default=0,help="increase output verbosity")
#parser.add_argument("-v", "--verbose", action="store_true",help="increase
#output verbosity")
args = parser.parse_args()
answer = args.square ** 2
if args.verbosity >= 2:
	print "the square of {} equals {}".format(args.square, answer)
elif args.verbosity >= 1:
	print "{}^2 == {}".format(args.square, answer)
else:
	print answer
'''
'''
import argparse

parser = argparse.ArgumentParser(description="calculate X to the power of Y")

group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")

group2 = parser.add_mutually_exclusive_group()
group2.add_argument("-v2", "--verbose2", action="store_true")
group2.add_argument("-q2", "--quiet2", action="store_true")

parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
args = parser.parse_args()
answer = args.x ** args.y

if args.quiet:
	print answer
elif args.verbose:
	print "{} to the power {} equals {}".format(args.x, args.y, answer)
else:
	print "{}^{} == {}".format(args.x, args.y, answer)
'''

'''
if __name__ == "__main__":
	opts, args = getopt.getopt(sys.argv[1:], "hi:o:",['--help'])
	for op, value in opts:
		if op == "-i":
			MySqlHandle.MySQLImportProcedure()
		elif op == "-o":
			MySqlHandle.MySQLDumpProcedure()
		elif op in ('-h','--help'):
			print("-i 导入, -o导出")
			# usage()
			sys.exit()
'''