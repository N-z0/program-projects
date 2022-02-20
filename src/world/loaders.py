#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "help to load scene and models files"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "5.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2021"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### built-in modules
import math# for degrees to radians

### commonz moduls
from commonz import logger
from commonz.constants import *
from commonz.ds import array
from commonz.datafiles import yml

### local moduls
from . import scenes



class Loader :
	"""scene file parser"""
	def __init__(self,data_pathnames,engine):
		"""
		data_pathnames must contents necessary data files path
		engine (zvs) will be use as output
		"""
		self.data_pathnames=data_pathnames
		self.engine=engine
	
	
	def load_scene_file(self,scene_file):
		"""
		scene_file need to be the path of wml file
		"""
		### retrieve all data from the file
		data=yml.get_data(self.data_pathnames[scene_file])
		
		### get the scene data
		shader_index=data['SHADER']['index']
		background=data['BACKGROUND']
		background_color=background['color']
		background_fog=background['fog']
		blend=data['BLEND']
		blend_factor=blend['factor']
		
		### load the requested shader
		self.engine.load_shader(shader_index)
		### and add new scene in the engine
		self.scene_index=self.engine.add_scene(shader_index,background_color,background_fog,blend_factor)
		### also create a local new scene
		self.scene=scenes.Scene(self.scene_index,shader_index,background_color,background_fog,blend_factor)
		
		### for all units found in the scene file
		for unit_data in data['UNITS'] :
			self.extract_items(unit_data)
		
		### return the local new scene
		return self.scene
	
	
	def extract_items(self,item_data,parent_index=None,models_lib=None,sounds_lib=None,position=None,orientation=None,scale=None,activ=None,attribs=None):
		"""get data from the elements of scene"""
		class_item=item_data.get('class')
		position= position or item_data.get('position')
		orientation= orientation or item_data.get('orientation')
		scale= scale or item_data.get('scale')
		activ= activ or item_data.get('active')
		attributes= item_data.get('attributes',{})
		#print('attributes=',attributes,attribs,attribs is not None)
		attributes.update( attribs or {} )
		
		### get elements data from another file if requested
		if class_item=='file' :
			### get and remove the path attributes
			### because we dont want to overwrite the one imported from file
			path=attributes.pop('path')
			self.load_items_file(path,parent_index,position,orientation,scale,activ,attributes)
			### given children are ignored because it will make conflicts with the imported children
			if item_data.get('children') :
				logger.log_warning(71,[path])
		else:
			item_index=self.add_item(class_item,parent_index,position,orientation,scale,activ,attributes,models_lib,sounds_lib)
			
			### do same process for any children
			for child_data in item_data.get('children',[]) :
				self.extract_items(child_data,item_index,models_lib,sounds_lib)
	
	
	def load_items_file(self,path,parent_index,position,orientation,scale,activ,attribs):
		"""get data from items file"""
		### retrieve all data from the file
		data=yml.get_data(self.data_pathnames[path])
		
		### get the sound models data if any
		models_lib= self.extract_models( data['MODELS'] )
		sounds_lib= self.extract_sounds( data['SOUNDS'] )
		
		### process all items found in file
		for item_data in data['OBJECT'] :
			self.extract_items(item_data,parent_index,models_lib,sounds_lib,position,orientation,scale,activ,attribs)
	
	
	def add_item(self,class_item,parent_index,position,orientation,scale,activ,attribs,models_lib,sounds_lib):
		"""output a new item"""
		### use given or default values
		position= position or (0,0,0)
		orientation= orientation or (0,0,0)
		scale= scale or (1,1,1)
		activ= activ or True
		
		### convert orientation angles in to one quaternion
		euler_rotation=(math.radians(orientation[X]),math.radians(orientation[Y]),math.radians(orientation[Z]))
		#euler_quaternion=tuple( array.quaternion_from_euler(euler_rotation[X],euler_rotation[Y],euler_rotation[Z]) )
		xq= array.quaternion_from_pitch(euler_rotation[X])
		yq= array.quaternion_from_yaw(euler_rotation[Y])
		zq= array.quaternion_from_roll(euler_rotation[Z])
		quaternion= tuple(array.multiply_quaternions( array.multiply_quaternions(zq,yq) ,xq))
		
		### adapt the process for each type of object
		if class_item=='object' :
			item_index=self.add_object(parent_index,position,quaternion,scale,activ,attribs,models_lib,sounds_lib)
		elif class_item=='eye' :
			item_index=self.add_eye(parent_index,position,quaternion,scale,activ,attribs)
		elif class_item=='ear' :
			item_index=self.add_ear(parent_index,position,quaternion,scale,activ,attribs)
		elif class_item=='light' :
			item_index=self.add_light(parent_index,position,quaternion,scale,activ,attribs)
		else :
			item_index=None
			logger.log_error(72,[class_item])
			raise NameError(class_item)
		
		return item_index
	
	
	def extract_sounds(self,sounds_data):
		"""retrieve sound data and load in engine"""
		sounds_lib={}
		if sounds_data :
			for sound_data in sounds_data :
				### use name as identifier
				name=sound_data['name']
				volumes=sound_data['volumes']
				pitch=sound_data['pitch']
				loop=sound_data['loop']
				spreading=sound_data['spreading']
				angles= (math.radians(sound_data['angles'][0]),math.radians(sound_data['angles'][1]))
				source_index= self.engine.load_resource_sound(self.data_pathnames[sound_data['source']])
				sounds_lib[name]={'volumes':volumes,'pitch':pitch,'loop':loop,'angles':angles,'spreading':spreading,'index':source_index}
		
		return sounds_lib
	
	
	def extract_models(self,models_data):
		"""retrieve model data and load in engine"""
		models_lib={}
		if models_data :
			for model_data in models_data :
				### use name as identifier
				name=model_data['name']
				
				### mesh
				mesh=model_data['mesh']
				mesh_lib={}
				mesh_lib['index']=self.engine.load_resource_mesh(self.data_pathnames[mesh['path']])
				mesh_lib['part']=mesh.get('part','')
				mesh_lib['groups']=mesh.get('groups',[])
				
				### textures
				textures=model_data['textures']
				textures_lib={}
				textures_lib['emit_index']= self.engine.load_resource_texture_emissive(self.data_pathnames[textures['emit']])
				textures_lib['ao_index']= self.engine.load_resource_texture_ao(self.data_pathnames[textures['ao']])
				textures_lib['albedo_index']= self.engine.load_resource_texture_albedo(self.data_pathnames[textures['albedo']])
				textures_lib['smoothness_index']= self.engine.load_resource_texture_smoothness(self.data_pathnames[textures['smoothness']])
				textures_lib['metallic_index']= self.engine.load_resource_texture_metallic(self.data_pathnames[textures['metallic']])
				textures_lib['normal_index']= self.engine.load_resource_texture_normal(self.data_pathnames[textures['normal']])
				
				### materials
				materials_lib={}
				for material in model_data['materials'] :
					material_index=self.engine.load_resource_material(self.data_pathnames[material['path']])
					material_name=material['name']
					materials_lib[material_name]=material_index
				
				models_lib[name]={'mesh':mesh_lib,'textures':textures_lib,'materials':materials_lib}
		
		return models_lib
	
	
	def add_object(self,parent_index,position,quaternion,scale,activ,attribs,models_lib,sounds_lib):
		"""retrieve object data and load it in engine"""
		### getting index by loading object in the engine
		item_index=self.engine.add_scene_item(self.scene_index,parent_index,activ,position,quaternion,scale)
		
		### set the models if there some for this object
		obj_models_lib={}
		if 'model' in attribs :
			models_list= attribs['model']
			if not type(models_list)==list :# no tuples in .yml files
				models_list=[models_list]
			for model_name in models_list :
				obj_models_lib[model_name]= models_lib.get(model_name,None)
			if models_list[0] in obj_models_lib :
				model_name=models_list[0]
				self.set_model(item_index,obj_models_lib[model_name])
		
		### set the sounds if there some for this object
		obj_sounds_lib={}
		if 'sound' in attribs :
			sounds_list= attribs['sound']
			if not type(sounds_list)==list :# no tuples in .yml files
				sounds_list=[sounds_list]
			for sound_name in sounds_list :
				obj_sounds_lib[sound_name]= sounds_lib.get(sound_name,None)
			if sounds_list[0] in obj_sounds_lib :
				sound_name=sounds_list[0]
				self.set_sound(item_index,obj_sounds_lib[sound_name])
		
		### add the new object into the local scene
		self.scene.add_object(parent_index,item_index,attribs,obj_models_lib,obj_sounds_lib)
		
		return item_index
	
	
	def add_eye(self,parent_index,position,quaternion,scale,activ,attribs):
		"""retrieve eye data and load it in engine"""
		frame_position=attribs['frame']['position']
		frame_size=attribs['frame']['size']
		size=attribs['size']
		scope=attribs['scope']
		focal=math.radians(attribs['focal_normal'])
		### getting index by loading eye in the engine
		item_index=self.engine.add_scene_eye(self.scene_index,parent_index,frame_position,frame_size,size,scope,focal,activ,position,quaternion,scale)
		### add the new eye into the local scene
		self.scene.add_eye(parent_index,item_index,attribs)
		return item_index
	
	
	def add_ear(self,parent_index,position,quaternion,scale,activ,attribs):
		"""retrieve ear data and load it in engine"""
		volume=attribs['volume']
		### getting index by loading ear in the engine
		item_index=self.engine.add_scene_ear(self.scene_index,parent_index,volume,activ,position,quaternion,scale)
		### add the new ear into the local scene
		self.scene.add_ear(parent_index,item_index,attribs)
		return item_index
	
	
	def add_light(self,parent_index,position,quaternion,scale,activ,attribs):
		"""retrieve light data and load it in engine"""
		ambient=attribs['ambient']
		diffuse=attribs['diffuse']
		### getting index by loading light in the engine
		item_index=self.engine.add_scene_light(self.scene_index,parent_index,ambient,diffuse,activ,position,quaternion,scale)
		### add the new light into the local scene
		self.scene.add_light(parent_index,item_index,attribs)
		return item_index
	
	
	def set_model(self,item_index,model):
		"""associate the given model to an object in the engine"""
		### mesh
		mesh=model['mesh']
		mesh_name= mesh['part']
		mesh_index=mesh['index']
		### textures
		textures= model['textures']
		t_emit=textures['emit_index']
		t_ao=textures['ao_index']
		t_albedo=textures['albedo_index']
		t_smooth=textures['smoothness_index']
		t_metal=textures['metallic_index']
		t_normal=textures['normal_index']
		### materials
		materials=model['materials']
		
		self.engine.add_scene_item_model(self.scene_index,item_index,mesh_index,mesh_name,t_emit,t_ao,t_albedo,t_smooth,t_metal,t_normal,materials)
	
	
	def set_sound(self,item_index,sound):
		"""associate the given sound to an object in the engine"""
		sound_index=sound['index']
		volumes=sound['volumes']
		pitch=sound['pitch']
		loop=sound['loop']
		angles=sound['angles']
		spreading=sound['spreading']
		
		self.engine.add_scene_item_noise(self.scene_index,item_index,sound_index,volumes,pitch,loop,angles,spreading)

