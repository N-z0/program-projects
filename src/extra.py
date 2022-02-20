#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "an importable additional supplement for the main core module"#information describing the purpose of this module
__status__ = "Prototype"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "4.1.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2016-02-25"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = ["Rob xxx", "Peter xxx", "Gavin xxxx",	"Matthew xxxx"]#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### import the required modules

### for output messages to logs systems
from commonz import logger

import time


EXTRA_CONSTANTE=3 # some description



def template_fonction():
	"""information describing the use of this function"""
	#print( "My name is {0[name]}".format(dict(name='Fred')) )
	#time.sleep(3)
	#input("Press Enter to continue")
	return True


def log_test():
	"""information describing the use of this function"""
	logger.log_debug(36)
	logger.log_info(37)
	logger.log_warning(38)
	logger.log_error(39)
	logger.log_critical(40)
