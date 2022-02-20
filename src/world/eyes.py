#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module containing eyes item class"#information describing the purpose of this module
__status__ = "Prototype"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "1.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2022"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = ["Rob xxx", "Peter xxx", "Gavin xxxx",	"Matthew xxxx"]#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



###  built-in modules
import math#.radians()

### local moduls
from . import items



class Eye(items.Item):
	def __init__(self,parent_index,item_index,attribs):
		items.Item.__init__(self,parent_index,item_index)
		"""
		parent_index is the item from where this light is positioned
		item_index is the reference for this light in the engine
		attribs are values and states concerning this light
		"""
		### we keep the given attributes
		self.frame_position=attribs['frame']['position']
		self.frame_size=attribs['frame']['size']
		self.size=attribs['size']
		self.scope=attribs['scope']
		### for the focal we need some specials attributes
		self.zoom=1
		self.focal=self.focal_normal=attribs['focal_normal']
		self.focal_limits=(attribs['focal_min'],attribs['focal_max'])
		self.zoom_limits=(attribs['zoom_min'],attribs['zoom_max'])
	
	
	def post_compute(self,engine,scene_index,time,period,focal,zoom,reset):
		"""
		proceed to the change of state due to the result of the new transformations
		engine is the program part in charge of sub works
		scn_index is the engine reference of the scene where this light is
		time is the amount of seconds since the start of the program
		period is the time in seconds elapsed since the last call of this function
		focal the angle of view
		zoom a factor of the angle of view
		reset if true the zoom is removed
		"""
		### reckon the new focal value
		new_focal= self.focal_normal+focal
		new_good_focal= self.get_correct_value(new_focal,self.focal_limits)
		### reckon the new zoom value
		new_zoom= int(reset) or self.zoom+zoom*period
		new_good_zoom= self.get_correct_value(new_zoom,self.zoom_limits)
		### order the engine to update the eye if any changes
		if new_good_focal!=self.focal or new_good_zoom!=self.zoom :
			engine.set_scene_eye(scene_index,self.item_index,focal=math.radians(new_good_focal*new_good_zoom))
			### and keep the new values
			self.zoom= new_good_zoom
			self.focal= new_good_focal


