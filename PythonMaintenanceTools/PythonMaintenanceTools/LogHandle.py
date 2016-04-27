#coding:utf-8
import logging
import logging.handlers

class Logger():
	"""
	日志处理
	"""
	fileName = "maintenace.log"
	fmt = '[%(asctime)s] - [%(levelname)s] - %(message)s'
	logging.basicConfig(level=logging.NOTSET, format=fmt)

	filehandler = logging.handlers.TimedRotatingFileHandler(fileName, when="M", interval=1, backupCount=0, encoding=None, delay=False, utc=False)
	filehandler.suffix = "%Y%m%d.log"
	filehandler.setFormatter(logging.Formatter(fmt))
	logging.getLogger('').addHandler(filehandler)

	logger = logging.getLogger()
	logger.debug("日志初始化完成")
	
	'''
	@classmethod
	def __init__(self):
		logger = logging.getLogger('web');
		logger.debug("日志初始化完成")
	'''
	
	@classmethod
	def msg(self, msg):
		return "%s" % (msg)
	
	
	@classmethod
	def info(self, msg):
		self.logger.info(Logger.msg(msg))
		
	@classmethod
	def debug(self, msg):
		self.logger.debug(Logger.msg(msg))
		
		
	@classmethod
	def critical(self, msg):
		self.logger.critical(Logger.msg(msg))
	
	@classmethod
	def error(self, msg):
		self.logger.error(Logger.msg(msg))
		
	@classmethod
	def warning(self, msg):
		self.logger.warning(Logger.msg(msg))