#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "This module implements a 3D space where different types of objects can be added"#information describing the purpose of this module
__status__ = "Prototype"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "2.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2022"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = ["Rob xxx", "Peter xxx", "Gavin xxxx",	"Matthew xxxx"]#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



###  built-in modules
import math # math.sin()

### local moduls
from . import lights
from . import eyes
from . import ears
from . import items
from . import objects

### from commonz
#from commonz.constants import *
#from commonz.ds import array



OBJECT_TYPE= 'type'
EMPTY_OBJECT="empty"
SOLID_OBJECT="solid"
GYRO_OBJECT= "gyro"
BODY_OBJECT= "body"
HEAD_OBJECT= "head"



class Scene(items.Item) :
	def __init__(self,scene_index,shader_index,background_color,background_fog,blend_factor,position=(0,0,0),orientation=(0,1,0,0),scale=(1,1,1)):
		#items.Item.__init__(self,True,position,orientation,scale)
		
		### keep the reference of this scene to be able to use it with the engine
		self.index=scene_index
		
		### keep a local copy of the colors attributes
		self.background_color=background_color
		self.background_fog=background_fog
		self.blend_factor=blend_factor
		
		### we store all items in dedicated lists
		self.objects_list = []
		self.bodys_list = []
		self.heads_list = []
		### for special items also
		self.eyes_list = []
		self.ears_list = []
		self.lights_list = []
	
	
	def select(self,engine):
		"""command the engine to use this scene as current scene"""
		engine.select_scene(self.index)
	
	
	def add_eye(self,parent_index,item_index,attribs):
		"""
		create and append a new eye object into the local scene
		parent_index is the ref of the item that will hold the new eye
		item_index is the ref of the eye in the engine
		attribs are values and states concerning the new eye
		"""
		eye= eyes.Eye(parent_index,item_index,attribs)
		self.eyes_list.append(eye)
	
	
	def add_ear(self,parent_index,item_index,attribs):
		"""
		create and append a new ear object into the local scene
		parent_index is the ref of the item that will hold the new ear
		item_index is the ref of the ear in the engine
		attribs are values and states concerning the new ear
		"""
		ear= ears.Ear(parent_index,item_index,attribs)
		self.ears_list.append(ear)
	
	
	def add_light(self,parent_index,item_index,attribs):
		"""
		create and append a new light object into the local scene
		parent_index is the ref of the item that will hold the new light
		item_index is the ref of the light in the engine
		attribs are values and states concerning the new light
		"""
		light= lights.Light(parent_index,item_index,attribs)
		self.lights_list.append(light)
	
	
	def add_object(self,parent_index,item_index,attribs,obj_models_lib,obj_sounds_lib):
		"""
		create and append a new object into the local scene
		parent_index is the ref of the item that will hold the new object
		item_index is the ref of the object in the engine
		attribs are values and states concerning the new object
		obj_models_lib the 3d shapes available for the new object
		obj_sounds_lib the 3d souds available for the new object
		"""
		tip=attribs[OBJECT_TYPE]
		if tip==EMPTY_OBJECT :
			obj= objects.Object(parent_index,item_index)
			self.objects_list.append(obj)
		elif tip==SOLID_OBJECT :
			obj= objects.Solid(parent_index,item_index,attribs,obj_models_lib,obj_sounds_lib)
			self.objects_list.append(obj)
		elif tip==GYRO_OBJECT :
			obj= objects.Gyro(parent_index,item_index,attribs,obj_models_lib,obj_sounds_lib)
			self.objects_list.append(obj)
		elif tip==BODY_OBJECT :
			body= objects.Body(parent_index,item_index,attribs,obj_models_lib,obj_sounds_lib)
			self.bodys_list.append(body)
		elif tip==HEAD_OBJECT :
			head= objects.Head(parent_index,item_index,attribs,obj_models_lib,obj_sounds_lib)
			self.heads_list.append(head)
	
	
	def pre_compute(self,time,period,values,states,engine):
		"""
		reckon relative transformations changes
		time is the amount of seconds since the start of the program
		period is the time in seconds elapsed since the last call of this function
		values are numbers entered by the control devices
		states are True or False statues set by the control devices
		engine is the program part in charge of sub works
		"""
		### get the speed factor
		speed_factor = values[6]+1
		
		### get a factor 1 if pressing some key/button for allowing rotation,
		### else the factor is 0
		active_rot=int(states[2])
		
		### reckon relative changes for special objects
		self.bodys_list[0].pre_compute(engine,self.index,time,period,values[0]*speed_factor,values[1]*speed_factor,values[2]*speed_factor,values[3]*speed_factor*active_rot)
		self.heads_list[0].pre_compute(engine,self.index,time,period,values[4]*speed_factor*active_rot)
		
		### reckon relative changes to all others objects
		for obj in self.objects_list :
			obj.pre_compute(engine,self.index,time,period)
	
	
	def post_compute(self,time,period,values,states,engine):
		"""
		proceed to the change of state due to the result of the new transformations
		time is the amount of seconds since the start of the program
		period is the time in seconds elapsed since the last call of this function
		values are numbers entered by the control devices
		states are True or False statues set by the control devices
		engine is the program part in charge of sub works
		"""
		### change scene color during time
		light=(math.sin(time/3)*0.9+1.1)/2# from 0.1 to 1
		color=(light,light/2,light/4,1)
		engine.set_scene(self.index,background=color)
		self.lights_list[0].set_attributes(engine,self.index,time,period,diffuse=color)
		
		### check and change states of objects
		for obj in self.objects_list :
			obj.post_compute(engine,self.index,time,period)
		
		### eventually change the eye aspect
		self.eyes_list[0].post_compute(engine,self.index,time,period,values[8],values[9],states[1])


