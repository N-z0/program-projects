#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "module containing objects item class"#information describing the purpose of this module
__status__ = "Prototype"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "1.0.1"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2022-04-01"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = ["Rob xxx", "Peter xxx", "Gavin xxxx",	"Matthew xxxx"]#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### built-in modules
import math # for degrees radian covert

### commonz imports
#from commonz.constants import *
from commonz.ds import array

### local moduls
from . import items



class Object(items.Item):
	def __init__(self,parent_index,item_index):
		items.Item.__init__(self,parent_index,item_index)
		"""
		thing having place in the space world
		parent_index is the item from where this object is positioned
		item_index is the reference for this object in the engine
		"""
	
	
class Solid(Object):
	def __init__(self,parent_index,item_index,attribs,obj_models_lib,obj_sounds_lib):
		Object.__init__(self,parent_index,item_index)
		"""
		the materials things
		parent_index is the item from where this object is positioned
		item_index is the reference for this object in the engine
		attribs are values and states concerning the new object
		obj_models_lib the 3d shapes available for the new object
		obj_sounds_lib the 3d sounds available for the new object
		"""
		### we keep some attributes
		self.mass=attribs['mass']
		self.box=attribs['box']


class Body(Solid):
	def __init__(self,parent_index,item_index,attribs,obj_models_lib,obj_sounds_lib):
		Solid.__init__(self,parent_index,item_index,attribs,obj_models_lib,obj_sounds_lib)
		"""
		low part of person
		parent_index is the item from where this object is positioned
		item_index is the reference for this object in the engine
		attribs are values and states concerning the new object
		obj_models_lib the 3d shapes available for the new object
		obj_sounds_lib the 3d souds available for the new object
		"""
		### we keep the 3d shapes and the 3d souds
		self.obj_models_lib=obj_models_lib
		self.obj_sounds_lib=obj_sounds_lib
		### also we keep the rotate attributes
		self.rotate_speeds=(attribs['rotate_speed_min'],attribs['rotate_speed_max'])
		### and we we set the speed of moves levels
		self.move_speeds=(0,attribs['move_speed_slow'],attribs['move_speed_normal'],attribs['move_speed_fast'])
		self.move_levels=[]
		self.move_levels.append( self.move_speeds[1] )
		self.move_levels.append( self.move_speeds[2]-(self.move_speeds[2]-self.move_speeds[1])/3 )
		self.move_levels.append( (self.move_speeds[3]-self.move_speeds[2])/3+self.move_speeds[2] )
		self.move_levels.append( self.move_speeds[3] )
	
	
	def pre_compute(self,engine,scene_index,time,period,move_x,move_y,move_z,rotate):
		"""proceed and project the relative transformations movement"""
		### eventually set a move vector
		if move_x or move_y or move_z :
			vector=array.vector([move_x,move_y,move_z])
			lengh= array.vector_length(vector)
			level=self.get_correct_level(lengh,self.move_levels)
			speed=self.move_speeds[level]
			vector*= speed/lengh  *period
		else :
			vector=None
		### eventually set a rotation quaternion
		if rotate :
			new_rotate= self.get_correct_increment( rotate,self.rotate_speeds)
			#if rotate!=new_rotate : print(rotate,new_rotate)
			quaternion= array.quaternion_from_yaw(math.radians(new_rotate*period))
		else:
			quaternion= None
		### order the engine to update the object if any changes
		if  vector is not None  or  quaternion is not None  :
			engine.set_scene_item(scene_index,self.item_index,position=vector,orientation=quaternion,cumulative=True)


class Head(Solid):
	def __init__(self,parent_index,item_index,attribs,obj_models_lib,obj_sounds_lib):
		Solid.__init__(self,parent_index,item_index,attribs,obj_models_lib,obj_sounds_lib)
		"""
		up part of person
		parent_index is the item from where this object is positioned
		item_index is the reference for this object in the engine
		attribs are values and states concerning the new object
		obj_models_lib the 3d shapes available for the new object
		obj_sounds_lib the 3d souds available for the new object
		"""
		### set the values for the pitch rotation
		self.angle=0
		self.angle_limits=(attribs['angle_min'],attribs['angle_max'])
		### set the values for the yaw rotation
		self.rotate_limits=(attribs['rotate_speed_min'],attribs['rotate_speed_max'])
	
	
	def pre_compute(self,engine,scene_index,time,period,rotate):
		"""proceed and project the relative transformations movement"""
		### eventually get the angle value truncated for not exceeding the thresholds
		good_rotate= self.get_correct_increment(rotate,self.rotate_limits) *period
		new_angle= self.get_correct_value(self.angle+good_rotate,self.angle_limits)
		### order the engine to update the object if the angle changed
		if new_angle!=self.angle :
			quaternion= array.quaternion_from_pitch(math.radians(new_angle))
			engine.set_scene_item(scene_index,self.item_index,orientation=quaternion,cumulative=False)#should use cumulative=True, set False for demo
			### keep the new angle
			self.angle=new_angle


class Gyro(Solid):
	def __init__(self,parent_index,item_index,attribs,obj_models_lib,obj_sounds_lib):
		Solid.__init__(self,parent_index,item_index,attribs,obj_models_lib,obj_sounds_lib)
		"""
		a rotating thing
		parent_index is the item from where this object is positioned
		item_index is the reference for this object in the engine
		attribs are values and states concerning the new object
		obj_models_lib the 3d shapes available for the new object
		obj_sounds_lib the 3d souds available for the new object
		"""
		### get the values for the rotation
		speed=attribs['speed']
		self.inc_rot= math.radians(speed)# degree by sec
		### we will use this flag for starting the object sound at the right time
		self.starting=True
	
	
	def pre_compute(self,engine,scene_index,time,period):
		"""
		proceed and project the relative transformations movement
		engine is the program part in charge of sub works
		scn_index is the engine reference of the scene where this light is
		time is the amount of seconds since the start of the program
		period is the time in seconds elapsed since the last call of this function
		"""
		### order to increment the object rotation if the object is active in the engine world
		if engine.get_scene_item_activity(scene_index,self.item_index) :
			rot = self.inc_rot*period
			quaternion= array.quaternion_from_yaw(rot)
			engine.set_scene_item(scene_index,self.item_index,orientation=quaternion,cumulative=True)
		
		
	def post_compute(self,engine,scene_index,time,period):
		"""
		proceed to the change of state due to the result of the new transformations
		engine is the program part in charge of sub works
		scn_index is the engine reference of the scene where this light is
		time is the amount of seconds since the start of the program
		period is the time in seconds elapsed since the last call of this function
		"""
		### if not yet started we the engine to play the object sound
		if self.starting==True :
			engine.set_scene_item_noise(scene_index,self.item_index,playout=True)
			### now the object sound is playing no need to keep this flag true
			self.starting=False


