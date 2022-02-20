#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "help to load hud files"#information describing the purpose of this module
__status__ = "Prototype"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "1.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2022"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = ["Rob xxx", "Peter xxx", "Gavin xxxx",	"Matthew xxxx"]#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### THE MODULE IS NOT WHAT I WANT !!!
### currently the zvs graphic engine use a rickety wonky wobbly openGL for displaying icons.
### i would like another system for displaying icons.
### maybe Cairo is more appropriate for this task
### also should have a css parser for loading icons from description files



### import the required modules
import math# for degrees to radians

### for output messages to logs systems
from commonz import logger
from commonz.constants import *



HUD_SHADER="hud"

BITMAPS_PATH_LIST=["world/overlays/bitmaps/overlay/scope",
						 "world/overlays/bitmaps/overlay/screen",
						 "world/overlays/bitmaps/status/moves",
						 "world/overlays/bitmaps/status/warning",
						 "world/overlays/bitmaps/minimap/background"]

NOISES_PATH_LIST=["world/overlays/noises/wowbeep"]



class Overlay:
	def __init__(self,output_index):
		self.output_index=output_index
	
	
	def select(self,engine):
		"""select the overlay for the engine"""
		engine.select_overlay(self.output_index)
	
	
	def compute(self,time,period,values,states,engine):
		"""proceed changes"""
		
		### take 3 secondes before completely= removing the hud transparency
		if time<3.0 :
			engine.set_overlay(self.output_index,blend_factor=time/3)
		
		### show icon if any key/button for rotation is pressed
		if states[2] is True :
			engine.add_overlay_icon_sprite(self.output_index,1,2,anchor=(0,0))
		else :
			engine.del_overlay_icon_sprite(self.output_index,1)
		
		### show icon and play sound if wrong key/button pressed
		if states[0] is True:
			engine.set_overlay_icon_signal(self.output_index,2,playout=True,volume=1)
			engine.add_overlay_icon_sprite(self.output_index,2,3,anchor=(0,0))
		else :
			engine.set_overlay_icon_signal(self.output_index,2,playout=False)
			engine.del_overlay_icon_sprite(self.output_index,2)



def load_hud(data_pathnames,output):
	"""add new hud overlay into the engine"""
	### load the requested shader
	output.load_shader(HUD_SHADER)
	### and add new hud in the engine
	overlay_index=output.add_overlay(HUD_SHADER)
	overlay=Overlay(overlay_index)
	
	### load all bitmaps in the engine
	for bitmap_path in BITMAPS_PATH_LIST :
		bmp_index=output.load_resource_bitmap(data_pathnames[bitmap_path])
	### load all noises in the engine
	for noise_path in NOISES_PATH_LIST :
		noise_index=output.load_resource_audio(data_pathnames[noise_path])
	
	### put icons in the engine and set bitmap noise to them
	### scope overlay
	icon_index=output.add_overlay_icon(overlay_index,None,position=(0,0,0.5),scale=(1,1))#
	output.add_overlay_icon_sprite(overlay_index,icon_index,0,anchor=(0.5,0.5),relative_position=True,relative_width=True,relative_height=True)
	### move icon
	icon_index=output.add_overlay_icon(overlay_index,None,position=(35,35,0.5),scale=(2,2),orientation=math.radians(180))#
	### alert icon
	icon_index=output.add_overlay_icon(overlay_index,None,position=(105,35,0.5),scale=(2,2),orientation=math.radians(0))#
	output.add_overlay_icon_signal(overlay_index,icon_index,0,volume=0.001,pitch=1,loop=False)
	### minimap
	icon_index=output.add_overlay_icon(overlay_index,None,position=(-1058*0.2*0.5,-1058*0.2*0.5,0.5),scale=(0.2,0.2))#
	output.add_overlay_icon_sprite(overlay_index,icon_index,4,anchor=(1,1),relative_position=False,relative_width=False,relative_height=False)
	
	### return the created local overlay
	return overlay

