#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module containing lights item class"#information describing the purpose of this module
__status__ = "Prototype"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "1.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2022"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = ["Rob xxx", "Peter xxx", "Gavin xxxx",	"Matthew xxxx"]#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### local moduls
from . import items



class Light(items.Item):
	def __init__(self,parent_index,item_index,attribs):
		items.Item.__init__(self,parent_index,item_index)
		"""
		parent_index is the item from where this light is positioned
		item_index is the reference for this light in the engine
		attribs are values and states concerning this light
		"""
		### we keep the given attributes
		self.ambient=attribs['ambient']
		self.diffuse=attribs['diffuse']
	
	
	def set_attributes(self,engine,scn_index,time,period,ambient=None,diffuse=None):
		"""
		changes the given attributes of this light
		engine is the program part in charge of sub works
		scn_index is the engine reference of the scene where this light is
		time is the amount of seconds since the start of the program
		period is the time in seconds elapsed since the last call of this function
		ambient is the color added to the objects around this light
		diffuse is the color added to the objects directly exposed to this light
		"""
		engine.set_scene_light(scn_index,self.item_index,ambient,diffuse)


