#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "this modul is in charge of collecting config options and settings for starting program."#information describing the purpose of this prog
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "3.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
__date__ = "2016-02-25"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### following modules allow to know the consumption and the functioning of python progs,
### this kind of task is useful while conceptioning,
### But should normally be options of a good IDE, 
### A good IDE should also allow to display the result in sortable column or in statistics graphs
#import cProfile,profile # provide statistics that describes how often and for how long various parts of the program executed.
#import trace # list functions executed during program run.
#import tracemalloc #a debug tool to trace memory blocks allocated by Python to the running program
#import resource # This module provides measuring and controlling system resources utilized by program.

import sys
import os # operating system dedicated builtin module
#import platform # sys module provide the needed os info and is already imported for other purposes
#import sysconfig # Provide access to Python’s configuration information
import getpass#a portable way to get the current user's username

import shutil	# High-level file operations

### modules capable of changing the name of processes
##import procname # NOT available in Debian repository
##import prctl # NOT available for python3
#import setproctitle# "set proc title" must be installed (available in Debian repository)

### the freedesktop.org conventional standards modules
#import xdg # PyXDG support various freedesktop standards. must be installed (available in Debian repository)
import appdirs # python-appdirs is for determining appropriate platform-specific directories,  must be installed (available in Debian repository)

### specific modules
from common import logger
from common import config

import app



### These variables needs to be hard coded
CFG_DIRECTORY="cfg"
LOGS_DIRECTORY="logs"
CACHE_DIRECTORY="cache"
DATA_DIRECTORY="data"

DEFAULT_CFG_FILE="default.ini"
SYSTEM_CFG_FILE="system.ini"
USER_CFG_FILE="user.ini"
LOG_FILE="logs.tsv"

PLATFORMS = ('linux','darwin','netbsd','freebsd','openbsd') # are the current supported OS platforms

### for the setup of sub directories additional identity can be use, especially for windows os
PROG_AUTHOR= None # if set at None this feature will be ignored

### The same log message can be used in many cases with different variables
### And here can be displayed a larger part of the complete lines.
LOG1="this program was designed for Linux operating system.[{} detected]"
LOG2="logs systems are setup"
LOG3="{} not found"
LOG4="copy done from {}"
LOG5="unable to copy from {}"
LOG6="starting"
LOG7="ending"



### parsing files should not be integrated in this module
### because the prog have to decide later which mode to use for opening or writing files, 
### or which size of the memory buffer and prioritizing access, etc ...



def check_platform():
	"""verify that the current platform support the program"""
	### development focusing on specific os platforms may not work on others
	### can be used to detect the operating systems: os.name,os.uname(),sys.platform,platform.platform(),platform.system(),platform.system_alias(),platform.uname()
	### the operating system information should be also in the env variables, but its not certain
	if not sys.platform in PLATFORMS :
		logger.log_warning( LOG1.format(sys.platform) )


def get_env():
	"""return all environnement variables"""
	### os.getenv() is deprecated in favour of os.environ
	env= os.environ#.keys()
	#print(env)
	return env

def get_user_name():
	"""return user login name"""
	### LOGNAME is the original variable and tends to be used in System V Unix and its decendants.
	### USER was introduced by BSD to replace LOGNAME. These days lots of versions of Unix provide both in an effort to please everybody.
	### If both are present they should have the same value.
	#name=os.environ.get('USER')# when script run through sudo, "USER" is usually set to root
	#name=os.environ.get('LOGNAME')# and "USERNAME" is set with the user name running sudo.

	#name=os.getlogin() # with pipe raise OSError: Inappropriate ioctl for device
	name=getpass.getuser()# this function looks at the values of various environment variables to determine the user name.

	#print(name)
	return name

def get_working_dir():
	"""get working directory"""
	#wd= os.environ['PWD']
	wd=os.getcwd()
	#print(wd)
	return wd

def get_home_dir():
	"""get user home directory"""
	#home = os.path.expanduser("~")
	home = os.getenv("HOME")
	#home =  pathlib.Path.home()# need to import pathlib (if Python 3.5+) 
	#print(home)
	return home

def get_parent_dir():
	"""get path of the program directory"""
	start_path=__file__
	start_path=sys.argv[0]
	full_path=os.path.realpath(os.path.abspath(os.path.expanduser(os.path.normpath(start_path))))
	src_path=os.path.dirname(full_path)
	parent_path=  os.path.normpath( os.path.join(src_path,os.pardir) )
	#print(start_path,full_path,src_path,parent_path)
	return parent_path

def get_log_dir(parent_path,prog_name):
	"""get logs paths"""
	pathnames=[]
	pathnames.append( appdirs.user_log_dir(prog_name,PROG_AUTHOR) )# XDG Specification: ~/.cache/prog_name/log
	pathnames.append( os.path.join(parent_path,LOGS_DIRECTORY) )	
	#print(pathnames)
	return pathnames

def get_cache_dir(parent_path,prog_name):
	"""get cache path"""
	pathnames=[]
	pathnames.append( appdirs.user_cache_dir(prog_name,PROG_AUTHOR) )# XDG Specification: ~/.cache/prog_name
	pathnames.append( os.path.join(parent_path,CACHE_DIRECTORY) )	
	#print(pathnames)
	return pathnames

def get_data_dir(parent_path,prog_name):
	"""get data path"""
	pathnames=[]
	### this directory contain unalterable program data
	pathnames.append( appdirs.user_data_dir(prog_name,PROG_AUTHOR) )# XDG Specification: ~/.local/share/prog_name
	pathnames.append( appdirs.site_data_dir(prog_name,PROG_AUTHOR) )# should be: /usr/share but return /usr/share/xfce4
	pathnames.append( os.path.join(parent_path,DATA_DIRECTORY) )
	#print(pathnames)
	return pathnames

def get_init_dir(parent_dir,prog_name):
	"""get the init paths"""
	pathnames=[]
	pathnames.append( appdirs.user_config_dir(prog_name,PROG_AUTHOR) ) # XDG Specification:  ~/.config/prog_name/
	pathnames.append( appdirs.site_config_dir(prog_name,PROG_AUTHOR) ) # XDG Specification:  /etc/xdg/prog_name/
	pathnames.append( os.path.join(parent_dir,CFG_DIRECTORY) )
	#print(pathnames)
	return pathnames


def get_cfg(default_initfile,system_initfile,user_initfile):
	"""return command lines and configuration files options"""
	
	cfg=config.Config()
	
	cfg.read_configfile(default_initfile)
	cfg.read_optional_configfiles([system_initfile,user_initfile])
	
	
	#cfg.add_arg('input_file',str,0,'what files should be use for input data')
	#cfg.add_arg('output_file',str,1,'where to write a file containing output data')
	#cfg.add_valu('-v','--version',int,3,'assign three version numbers to the file','NUMBER','FILE','version')
	#cfg.add_valu('-e','--edit',bool,1,'define if the file need to be edited or not','yes/no','FILE','edit')
	#cfg.add_negative_flag('-u','--unsafe','disable the safety','FILE','safety')
	
	cfg.add_positive_flag('-l','--local','will not create files outside program directory','SYSTEM','local')
	
	cfg.add_choice('-fv','--logfile_verbosity',int,1,(0,1,2,3,4,5),'output verbosity level','VERBOSITY','logfile')
	cfg.add_choice('-tv','--terminal_verbosity',int,1,(0,1,2,3,4,5),'output verbosity level','VERBOSITY','terminal')
	cfg.add_choice('-sv','--syslog_verbosity',int,1,(0,1,2,3,4,5),'output verbosity level','VERBOSITY','syslog')
	
	cfg.add_valu('-s','--screen',int,1,'define which screen should be used','NUMBER','DISPLAY','screen')
	cfg.add_positive_flag('-f','--fullscreen','display in full screen mode','DISPLAY','fullscreen')
	cfg.add_negative_flag('-w','--window','display inside window','DISPLAY','fullscreen')
	cfg.add_positive_flag('-m','--maximize','maximize the window on the screen','DISPLAY','maximize')

	cfg.add_valu('-wp','--position',int,2,'set window position',('x','y'),'DISPLAY','position')
	cfg.add_valu('-ws','--size',int,2,'set window size',('x','y'),'DISPLAY','size')
	cfg.add_valu('-t','--title',str,1,'set window title','TITLE','DISPLAY','title')
	
	
	### os.path.isfile os.path.isdir etc can be use for check if filepath exist
	### but we will have to check their existence again later, before starting to use them
	### because in the meantime they can be changed / removed
	
	return cfg.get()


def get_default_init_file(directory):
	"""get default init file path"""
	initfile= os.path.join(directory,DEFAULT_CFG_FILE)
	#print(initfile)
	return initfile

def get_system_init_file(directory):
	"""get the system init file path"""
	initfile= os.path.join(directory,SYSTEM_CFG_FILE)
	#print(initfile)
	return initfile

def get_user_init_file(directory):
	"""get the user init file path"""
	initfile= os.path.join(directory,USER_CFG_FILE)
	#print(initfile)
	return initfile

def get_log_file(directory):
	"""get the log file path"""
	logfile= os.path.join(directory,LOG_FILE)
	#print(logfile)
	return logfile	
	
	
def set_logger(prog_name,syslog_verbosity,terminal_verbosity,logfile_verbosity,logfile):
	"""set the logs system"""
	os.makedirs(os.path.dirname(logfile),exist_ok=True)
	logger.setup(prog_name,logfile,syslog_verbosity,terminal_verbosity,logfile_verbosity)
	logger.log_debug(LOG2)


def check_place_initfile(source_initfile,user_initfile):
	"""if user initfile not exist try to creat it from the system initfile"""
	if not os.path.isfile(user_initfile) :
		logger.log_warning(LOG3.format(user_initfile))
		try:
			directory = os.path.dirname(user_initfile)
			os.makedirs(directory,exist_ok=True)
			shutil.copyfile(source_initfile,user_initfile)
			logger.log_info(LOG4.format(source_initfile))
		except : # IOError in Python 3 is now an alias for OSerror
			logger.log_error(LOG5.format(source_initfile))


def get_name():
	"""return the program name"""
	name = os.path.basename( os.path.splitext(__file__)[0] )
	#print(name)
	return name

def set_name(name):
	"""set process name"""
	#prctl.set_name(name)
	#prctl.set_proctitle(name)
	#print(prctl.get_name())
		
	setproctitle.setproctitle(name)
	#print(setproctitle.getproctitle())


def start(user_name,prog_name,cfg,dirs,env):
	"""start main activity"""
	logger.log_debug(LOG6)
	a = app.Application(user_name,prog_name,cfg,dirs,env)
	exit_stat = a.run()
	return exit_stat

def finsih(exit_stat):
	"""finish the prog"""
	logger.log_debug(LOG7)
	logger.shutdown()
	sys.exit(exit_stat)# 0 is the default exit code in case everything was ok, any nonzero value is considered “abnormal termination” by shells.



### This module should not be imported, otherwise the following important part will not be executed.
if __name__ == '__main__':
	"""start procedure"""
	
	env= get_env()

	user_name=get_user_name()
	
	prog_name=get_name() # use by: XDG directories, the set of name process, messages for syslogs,translate domain
	### the set of process name should be done by shell script
	### platform os may need to choose a special name for the process
	# set_name(prog_name)
	
	working_dir=get_working_dir()
	home_dir=get_home_dir()
	parent_dir= get_parent_dir() # use for default initfile and  local directories

	log_dir=get_log_dir(parent_dir,prog_name)
	cache_dir=get_cache_dir(parent_dir,prog_name)
	data_dir=get_data_dir(parent_dir,prog_name)
	init_dir=get_init_dir(parent_dir,prog_name)
	
	default_initfile=get_default_init_file(init_dir[2])
	system_initfile=get_system_init_file(init_dir[1])
	user_initfile=get_user_init_file(init_dir[0])
	
	cfg= get_cfg(default_initfile,system_initfile,user_initfile)
	
	local=cfg['SYSTEM']['local']
	#print('local:',local)
	if local :
		logfile= get_log_file(log_dir[1])
		cache_dir=cache_dir[1]
		data_dir=[data_dir[2]]
	else :
		logfile= get_log_file(log_dir[0])
		cache_dir=cache_dir[0]
		data_dir=data_dir[0:2]
		### The source for user init file depends about platform
		### better to let a starting shell script manage the copy
		# check_place_initfile( get_user_init_file(init_dir[2]),user_initfile )
	cfg_logs= cfg['VERBOSITY']
	set_logger(prog_name,cfg_logs['syslog'],cfg_logs['terminal'],cfg_logs['logfile'],logfile)
	
	check_platform() # here because need to setup the logs system first
	
	dirs={'cwd':working_dir,'home':home_dir,'cache':cache_dir,'data':data_dir}
	exit_stat=start(user_name,prog_name,cfg,dirs,env)
	
	finsih(exit_stat)
	
