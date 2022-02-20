#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module containing basic item class"#information describing the purpose of this module
__status__ = "Prototype"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "1.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2022"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = ["Rob xxx", "Peter xxx", "Gavin xxxx",	"Matthew xxxx"]#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### built-in modules
#import math # for degrees radian covert

### commonz imports
#from commonz.constants import *
#from commonz.ds import array



class Item:
	def __init__(self,parent_index,item_index):
		"""
		a common ancestor for all objects
		parent_index is the item from where this one is positioned
		item_index is the reference for this item in the engine
		"""
		### we keep the given attributes
		self.parent_index=parent_index
		self.item_index=item_index
	
	
	def get_correct_increment(self,inc,inc_levels):
		"""
		returns the value truncated for not to exceeding the given thresholds
		inc is a value that we need to evaluate
		inc_levels is a list of the minimal and maximal thresholds
		"""
		positive_inc= abs(inc)
		if positive_inc > inc_levels[1] :
			sign=positive_inc/inc
			inc = inc_levels[1] * sign
		elif positive_inc < inc_levels[0] :
			inc = 0
		return inc
	
	
	def get_correct_value(self,value,value_limits):
		"""
		returns a value between the given intervals
		value that we need to evaluate
		value_limits is a list of the minimal and maximal thresholds
		"""
		if value > value_limits[1] :
			value = value_limits[1]
		elif value < value_limits[0] :
			value = value_limits[0]
		return value
	
	
	def get_correct_level(self,value,levels):
		"""
		returns a value that matches the given thresholds
		value that we need to evaluate
		levels is a list of thresholds
		"""
		#print('level:',value,levels)
		for level in levels :
			if value<level :
				break
		return level
	
	
	def pre_compute(self,engine,scene_index,time,period,activity=None,position=None,orientation=None,scale=None,cumulative=False):
		"""proceed and project the relative transformations movement"""
		### update the item in the engine if any changes are detected
		if activity or position or orientation or scale :
			engine.set_scene_item(scene_index,self.item_index,activity,position,orientation,scale,cumulative)
	
	
	def post_compute(self,engine,scene_index,time,period):
		"""
		proceed to the change of state due to the result of the new transformations
		engine is the program part in charge of sub works
		scn_index is the engine reference of the scene where this light is
		time is the amount of seconds since the start of the program
		period is the time in seconds elapsed since the last call of this function
		"""
		### nothing to do for the basic item objects
		pass
	
	