#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "This is the program centerpiece,but need to be imported by other modules to be used"#information describing the purpose of this module
__status__ = "Prototype"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "4.0.1"# version number,date or about last modification made compared to the previous version
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


### Misc
#import random
#import string # chain of char manipulation
#import collections	# provide alternatives specialized datatypes (dict, list, set, and tupl) ex: deque>list-like container with fast appends and pops on either end
#from collections import deque # storage de queue de données
#import urllib # open a URL the same way you open a local file

### asynchron
#import asyncio #provides the basic infrastructure for writing asynchronous programs.
#import threading # constructs higher-level threading interfaces
#import queue  #when information must be exchanged safely between multiple threads.
#import signal #Set handlers for asynchronous events
#import select # is low level module,Users are encouraged to use the selectors module instead
#import selectors # built upon the select module,allows high-level I/O multiplexing
#import asyncio# built upon selectors
#import multiprocessing

### Math
#import operator #For example, operator.add(x, y) is equivalent to the expression x+y.
#import math #
#from Numeric import*
#import numpy
#import statistics	#mathematical statistics functions
#from fractions import Fraction # int(Fraction(3, 2) + Fraction(1, 2)) = 2
#from decimal import Decimal # because: 0.1 + 0.1 + 0.1 - 0.3 = 5.551115123125783e-17

### open read and write database
### but should not need to use these modules
### the datafiles module offer better db files parsers
#import dbm #Interfaces to various Unix "database" formats.
#import shelve # data persistence, allows backup python objet in a file for later reuse
#import sqlite3	#A DB-API 2.0 implementation using SQLite 3.x.


import extra



TEMPLATE_CONSTANTE=1 # some description



class Main :
	"""Basic main class"""
	def __init__(self,main_template_argument=True):
		"""information describing the use of this method"""
		self.template_attribut=main_template_argument

		#template_comment

	def template_method(self,qantum):
		"""information describing the use of this method"""
		while qantum :
			qantum-=1
			logger.log_info(29,[qantum])
		extra.log_test()


class Advanced_Main(Main) :
	"""Advanced main class"""
	def __init__(self,adv_main_template_argument,main_template_argument=False):
		"""information describing the use of this method"""
		Main.__init__(self,main_template_argument)

		logger.log_info( 30,[adv_main_template_argument] )
		self.template_attribut=adv_main_template_argument*"w"
		# comment
		self.valu_list=range(len(self.template_attribut))

	def adv_template_method(self,qantum):
		"""information describing the use of this method"""
		extra.template_fonction()
		for index in range(qantum) :
			# comment
			logger.log_info(31,[index])
			valu=self.valu_list[index]
			if valu!=0 :
				logger.log_info(32)
			elif valu>=1 :
				logger.log_info(33)
			elif valu==0 :
				logger.log_info(34)
			else :
				pass
