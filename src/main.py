#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "This is the program centerpiece,but need to be imported by other modules to be used"#information describing the purpose of this module
__status__ = "Prototype"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "5.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2016-02-25"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = ["Rob xxx", "Peter xxx", "Gavin xxxx",	"Matthew xxxx"]#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### import the required modules

### from commonz
from commonz import logger
from commonz.constants import *

### import the virtual world engine
import zvs

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
#import math
#from Numeric import*
#import numpy
#import statistics	#mathematical statistics functions
#from fractions import Fraction # int(Fraction(3, 2) + Fraction(1, 2)) = 2
#from decimal import Decimal # because: 0.1 + 0.1 + 0.1 - 0.3 = 5.551115123125783e-17

### open read and write database
### but should not need to use these modules
### the commonz.datafiles module offer better db files parsers
#import dbm #Interfaces to various Unix "database" formats.
#import shelve # data persistence, allows backup python objet in a file for later reuse
#import sqlite3	#A DB-API 2.0 implementation using SQLite 3.x.

### local moduls
import hud.loaders
import world.loaders



SCENE="world/scenes/alpha"
#SCENE="world/scenes/zulu"

### these are use to control by devices such as keyboard and mouse
VALUES_QUANTITY=100# transmitted values
STATES_QUANTITY=100# transmitted states
INDEX_QUANTITY=5#STATES,GO,BACK,SCROLLS_EMUL,POINTS_EMUL
STATES_INDEX=0
GO_INDEX=1
BACK_INDEX=2
SCROLLS_EMUL_INDEX=3
POINTS_EMUL_INDEX=4



class Main :
	"""Basic main class"""
	def __init__(self,data_pathnames):
		"""
		data_pathnames must contents all necessary data files path
		"""
		
		###  keep it because need for later loading scene and overlay
		self.data_pathnames=data_pathnames
		
		### we can have many scenes
		self.scenes=[]
		self.current_scene=None
		### and we can have many overlays too
		### but for this simple program we just use one
		self.overlay=None
		
		### for a regular timing
		self.period=0.01
		
		### implement the graphic engine
		self.engine= zvs.Interface()
		### become true when the graphic engine displayed the contents
		self.displayed=False
		
		### the default states and values setting
		self.scrollers_emulators_cfg_states=[False]*VALUES_QUANTITY
		self.pointers_emulators_cfg_states=[False]*VALUES_QUANTITY
		self.offsets_cfg_values=[0]*VALUES_QUANTITY
		self.scales_cfg_values=[1]*VALUES_QUANTITY
		### the default values for keyboards and joysticks
		self.total_states= STATES_QUANTITY+VALUES_QUANTITY*(INDEX_QUANTITY-1)
		self.keys_values= [0]*self.total_states
		self.buttons_values= [0]*self.total_states
		### the others default states
		self.inputs_states= [False]*STATES_QUANTITY
		self.scrollers_emulators_states= [False]*VALUES_QUANTITY
		self.pointers_emulators_states= [False]*VALUES_QUANTITY
		self.keys_buttons_go_states= [False]*VALUES_QUANTITY
		self.keys_buttons_back_states= [False]*VALUES_QUANTITY
		### the default values for reset
		self.default_values=[0]*VALUES_QUANTITY
		### the default values for scrolls
		self.scrollers_values= self.default_values.copy()
		self.scrollers_buffer_values= self.default_values.copy()
		self.scrollers_emulators_values= self.default_values.copy()
		### the default values for pointers
		self.pointers_values= self.default_values.copy()
		self.pointers_buffer_values= self.default_values.copy()
		self.pointers_emulators_values= self.default_values.copy()
		### the default values for keys and buttons go/back actions
		self.keys_buttons_go_back_values= self.default_values.copy()
		
		### the function to call by the app loop
		self.proceed= self.start
		
		
	def set_scroller_emulator_cfg(self,index,state=False):
		"""
		change the scroller emulators configuration
		state must be equal to False or True
		"""
		self.scrollers_emulators_cfg_states[index]=state
	
	
	def set_pointer_emulator_cfg(self,index,state=False):
		"""
		change the pointer emulators configuration
		state must be equal to False or True
		"""
		self.pointers_emulators_cfg_states[index]=state
	
	
	def set_offset_cfg(self,index,value=0):
		"""
		change the offset configuration
		value must be a number
		"""
		self.offsets_cfg_values[index]=value
	
	
	def set_scale_cfg(self,index,value=1):
		"""
		change the scale configuration
		value must be a number
		"""
		self.scales_cfg_values[index]=value
	
	
	def set_state(self,index):
		"""check and eventually change the related states"""
		### keys buttons states can be greater than 1
		### but keys buttons states should never be less than zero
		state= bool(self.keys_values[index] or self.buttons_values[index])
		
		### first need to know what type of state is concerned
		if index < STATES_QUANTITY :
			mod_index=0
			data_index=index
		else :
			index-=STATES_QUANTITY
			mod_index=index//VALUES_QUANTITY+1
			data_index=index%VALUES_QUANTITY
		
		### for each type of state there is some particular things todo
		if mod_index==STATES_INDEX :
			self.inputs_states[data_index]= state
		elif mod_index==BACK_INDEX and state!=self.keys_buttons_back_states[data_index] :
			self.keys_buttons_back_states[data_index]=state
			self.keys_buttons_go_back_values[data_index]= (int(self.keys_buttons_go_states[data_index])-int(state))*self.scales_cfg_values[data_index]
		elif mod_index==GO_INDEX and state!=self.keys_buttons_go_states[data_index] :
			self.keys_buttons_go_states[data_index]=state
			self.keys_buttons_go_back_values[data_index]= (int(state)-int(self.keys_buttons_back_states[data_index]))*self.scales_cfg_values[data_index]
		elif mod_index==SCROLLS_EMUL_INDEX and state!=self.scrollers_emulators_states[data_index] :
			self.scrollers_emulators_states[data_index]=state
			if state!=self.scrollers_emulators_cfg_states[data_index] :
				### reset the pointers_value because instead the scroller emulator will be use
				self.pointers_values[data_index]= 0
			else:
				### get back pointers_value because the scroller emulator stop to be used
				self.pointers_values[data_index]= self.pointers_buffer_values[data_index]
		elif mod_index==POINTS_EMUL_INDEX and state!=self.pointers_emulators_states[data_index] :
			self.pointers_emulators_states[data_index]=state
			if state!=self.pointers_emulators_cfg_states[data_index] :
				### set the pointers_emulators_value because the pointers_emulators start to be use
				self.pointers_emulators_values[data_index]= self.scrollers_buffer_values[data_index]
			else:
				### reset the pointers_emulators_values because the pointers_emulators_values stop to be used
				self.pointers_emulators_values[data_index]=0
		else :
			#means: mod_index==GO_INDEX and state==self.keys_buttons_go_states[data_index]
			pass
	
	
	def set_key_press(self,index,string,time):
		"""apply key press"""
		### self.keys_states[index] can be greater than 1
		### but self.keys_states[index] should never be less than zero
		self.keys_values[index]+=1
		self.set_state(index)
	
	
	def set_key_release(self,index,string,time):
		"""apply key release"""
		### self.keys_values[index] can be greater than 1
		### but self.keys_values[index] should never be less than zero
		self.keys_values[index]-=1
		self.set_state(index)
	
	
	def set_button_press(self,index,position,time):
		"""apply button press"""
		### self.buttons_values[index] can be greater than 1
		### but self.buttons_values[index] should never be less than zero
		self.buttons_values[index]+=1
		self.set_state(index)
	
	
	def set_button_release(self,index,position,time):
		"""apply button release"""
		### self.buttons_values[index] can be greater than 1
		### but self.buttons_values[index] should never be less than zero
		self.buttons_values[index]-=1
		self.set_state(index)
	
	
	def set_scroller_value(self,index,step,position,time):
		"""apply scroll movement"""
		new_value= step*self.scales_cfg_values[index]
		if self.pointers_emulators_states[index]!=self.pointers_emulators_cfg_states[index] :
			pointer_value= self.scrollers_buffer_values[index]+new_value
			self.pointers_emulators_values[index]= pointer_value
			self.scrollers_buffer_values[index]=pointer_value
		else:
			self.scrollers_values[index] += new_value
	
	
	def set_pointer_value(self,index,value,time):
		"""apply pointer movement"""
		new_value= (value+self.offsets_cfg_values[index])*self.scales_cfg_values[index]
		if self.scrollers_emulators_states[index]!=self.scrollers_emulators_cfg_states[index] :
			scroll_value= new_value - self.pointers_buffer_values[index]
			self.scrollers_emulators_values[index]+= scroll_value
			self.pointers_buffer_values[index]= new_value
		else:
			self.pointers_values[index]= new_value
	
	
	def focus_out(self):
		"""unfocus the area"""
		### when the focus is lost the app modul will not send any release event
		### so we must reset keys and buttons states
		self.keys_values= [0]*self.total_states
		self.buttons_values= [0]*self.total_states
		self.inputs_states=[False]*STATES_QUANTITY
		self.keys_buttons_go_states= [False]*VALUES_QUANTITY
		self.keys_buttons_back_states= [False]*VALUES_QUANTITY
		self.keys_buttons_go_back_values= self.default_values.copy()
		
		### reset to the default values for scrolls
		self.scrollers_values= self.default_values.copy()
		self.scrollers_buffer_values= self.default_values.copy()
		self.scrollers_emulators_values= self.default_values.copy()
		self.scrollers_emulators_states= [False]*VALUES_QUANTITY
		
		### reset to the default values for pointers
		self.pointers_values= self.default_values.copy()
		self.pointers_buffer_values= self.default_values.copy()
		self.pointers_emulators_values= self.default_values.copy()
		self.pointers_emulators_states= [False]*VALUES_QUANTITY
	
	
	def focus_in(self):
		"""give the focus to the area"""
		### nothing to do
		pass
	
	
	def start(self,frame,time,lapse):
		"""
		initialize the first frame
		frame is the number of how many times this function been called
		time is the amount of seconds since the start of the program
		lapse is the time in seconds elapsed since the last call of this function
		"""
		### the frame number should be 0
		if not frame==0 :
			logger.log_warning(70,[str(frame)])
		
		### get informations
		#print(self.engine.get_info_opengl())
		#print(self.engine.get_info_openal())
		
		### when openGL setting is done we can get the shaders repertory
		shaders_repertory=self.engine.get_shaders_repertory()
		#print(shaders_repertory)
		
		### load scene
		scn_loader= world.loaders.Loader(self.data_pathnames,self.engine)
		scene=scn_loader.load_scene_file(SCENE)
		self.scenes.append(scene)
		self.current_scene=self.scenes[0]
		self.current_scene.select(self.engine)
		
		### load HUD
		### for this program we will just use a single simple hud
		self.overlay=hud.loaders.load_hud(self.data_pathnames,self.engine)
		self.overlay.select(self.engine)
		
		### after this starting the app module will call another function
		self.proceed= self.pursue
		
		### return False because no need to redraw the gl_area
		return False
	
	
	def pursue(self,frame,time,lapse):
		"""
		proceed to changes
		frame is the number of how many times this function been called
		time is the amount of seconds since the start of the program
		lapse is the time in seconds elapsed since the last call of this function
		"""
		### collect an instant snapshot of states and values for no changes during process
		states  = self.inputs_states.copy()
		scrollers_values = [ v[0] or v[1] for v in zip(self.scrollers_values,self.scrollers_emulators_values) ]
		#scrollers_values = self.scrollers_values + self.scrollers_emulators_values
		pointers_values = [ v[0] or v[1] for v in zip(self.pointers_values,self.pointers_emulators_values) ]
		#pointers_values = self.pointers_values + self.pointers_emulators_values
		values = [ v[0]+v[1]+v[2] for v in zip(pointers_values,scrollers_values,self.keys_buttons_go_back_values) ]
		#values = scrollers_values + pointers_values + self.keys_buttons_go_back_values
		### reset scrollers values
		self.scrollers_values= self.default_values.copy()
		self.scrollers_emulators_values= self.default_values.copy()
		
		### periodic calculation for a regular timing
		### we don’t want to move from 1 unit each frame
		### because having a better computer is not an excuse for moving faster
		### so we need to scale the moves by the “time since the last frame”(deltaTime)
		while lapse>0 :
			if lapse>self.period :
				period=self.period
			else :
				period=lapse
			lapse-=period
			
			### reckon relative transformations changes
			for scene in self.scenes :
				scene.pre_compute(time,period,values,states,self.engine)
			### apply objects absolute transformation
			self.engine.reckon()
			### check and change aspect of objects
			for scene in self.scenes :
				scene.post_compute(time,period,values,states,self.engine)
			
			### process changes into the hud
			self.overlay.compute(time,period,values,states,self.engine)
		
		### need to redraw
		self.displayed=False
		### ask to redraw the gl_area
		return True
	
	
	def display(self):
		"""request to show the contents"""
		### ask the engine to draw the contents
		self.engine.display()
		### the draw as been done
		self.displayed=True
	
	
	def resize(self,size):
		"""
		request to follows changes of the gl_area size
		size is the 2 dimensions of rectangle where the graphic engine draw
		"""
		### ask the engine to resize his area
		self.engine.resize(size)
	
	
	def stop(self):
		"""request to stop"""
		### ask the engine to stop
		self.engine.stop()

