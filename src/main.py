#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "This is the program centerpiece,can be imported or use by a starter."#information describing the purpose of this module
__status__ = "Prototype"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "3.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2016-02-25"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = ["Rob xxx", "Peter xxx", "Gavin xxxx",	"Matthew xxxx"]#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### import the required modules

import os # use for exit status

### for output messages to logs systems
from common import logger

import extra#



### The same log message can be used in many cases with different variables
### And here can be displayed a larger part of the complete lines.
LOG1='test module function and class instance'
LOG2='template constante={}'
LOG3='template fonction result:{}'



class App():
	"""main software application as object"""
	def __init__(self,user_name,prog_name,cfg,dirs,env):
		"""initialization of the application"""
		
		### setup names
		self.prog_name=prog_name
		self.user_name=user_name
		
		### setup path
		self.working_dir=dirs['cwd']
		self.home_dir=dirs['home']
		self.cache_dir=dirs['cache']
		self.data_dir= dirs['data']
		
		### test module function and class instance
		logger.log_debug(LOG1)
		self.b=extra.template_fonction()
		self.o=extra.Template_Class_Enfant(template_argument_enfant=12,template_argument_parent=1)


	def run(self):
		"""operates the software object"""

		### test module function and class instance
		logger.log_debug(LOG2.format(extra.TEMPLATE_CONSTANTE))
		self.o.template_method_parent(3)
		extra.log_test()
		self.o.template_method_enfant(3)		
		logger.log_debug(LOG3.format(self.b))
		
		return os.EX_OK
