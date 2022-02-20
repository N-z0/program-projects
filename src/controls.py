#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "for the keyboards,mouse and others types of inputs handlers devices"#information describing the purpose of this module
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "2.1.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2013"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = [ ]#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### I KNOW !
### I MADE UGLY CODE HERE...
### I WISH TO FIND BETTER, BUT FOR NOW:::



### for output messages to logs systems
from commonz import logger
#import time
from gi.repository import Gdk as gdk



CONTROLS_POINTERS='POINTERS'
CONTROLS_SCROLLERS='SCROLLERS'
CONTROLS_BUTTONS='BUTTONS'
CONTROLS_KEYS='KEYS'

OPTIONS_SCALES='SCALES'
OPTIONS_OFFSETS='OFFSETS'
OPTIONS_SCROLLERS_EMULATORS='SCROLLERS_EMULATORS'
OPTIONS_POINTERS_EMULATORS='POINTERS_EMULATORS'

DEVICES_HANDLERS_SEPARATOR='/'

### same type of device get the same index
### i tried with 2 mouses connected to my computer
### the gtk/gdk events made with any of the 2 mouses get the same source index number
DEVICES={
	'MOUSE':gdk.InputSource.MOUSE,
	'KEYBOARD':gdk.InputSource.KEYBOARD,
	'CURSOR':gdk.InputSource.CURSOR,
	'ERASER':gdk.InputSource.ERASER,
	'PEN':gdk.InputSource.PEN,
	'TABLET_PAD':gdk.InputSource.TABLET_PAD,
	'TOUCHPAD':gdk.InputSource.TOUCHPAD,
	'TOUCHSCREEN':gdk.InputSource.TOUCHSCREEN,
	'TRACKPOINT':gdk.InputSource.TRACKPOINT,
	}

BUTTONS={
	'MIDDLE':gdk.BUTTON_MIDDLE,
	'PRIMARY':gdk.BUTTON_PRIMARY,
	'SECONDARY':gdk.BUTTON_SECONDARY
	}

SCROLLERS={
	'WHEEL':1# can also be: gdk.AxisUse.WHEEL i dont know exactly how to get it
	}

POINTERS={
	'X':0,
	'Y':1,
	'Z':3
	}



### CONTROLS

def get_controllers_map(controllers_settings,default_device,handlers_string_converter):
	"""get the devices controllers linked to the matching functions index"""
	controllers_map={}
	for function in controllers_settings :
		### function numbers are retrieved as strings so need to convert them
		function_index=int(function)
		### get the devices buttons keys and others handlers assigned to the function
		controllers=controllers_settings[function]
		controllers_list= controllers.split()
		while controllers_list:
			### get the combo of the device name + the handler name
			controller_combo= controllers_list.pop()
			if controller_combo in controllers_list :
				### ignore this controller_combo because many times in in the controllers_list
				logger.log_warning(57,[controller_combo])
			else :
				controller_names=controller_combo.split(DEVICES_HANDLERS_SEPARATOR,1)
				### get the handler name from the controller_combo
				### and if there is a device name in the controller_combo get the index of it
				### or get the default device index
				if len(controller_names)==2 :
					device_index=convert_device_string(controller_names[0])
					handler_name=controller_names[1]
				else :
					device_index=convert_device_string(default_device)
					handler_name=controller_names[0]
				### put the device in the controllers_map database if not already done
				if not device_index in controllers_map :
					controllers_map[device_index]={}
				### use the given string convert function for getting a list of handlers index to add
				for handler_index in handlers_string_converter(handler_name) :
					if not handler_index in controllers_map[device_index] :
						controllers_map[device_index][handler_index]= [function_index]
						logger.log_info(56,[controller_combo])
					else :
						### in this case no worry to have the same function index that append many times to the same controllers_map[device_index][handler_index]
						### because functions index should comes only once from the controls.ini file
						controllers_map[device_index][handler_index].append(function_index)
						logger.log_info(55,[controller_combo,len(controllers_map[device_index][handler_index])])
	return controllers_map


def convert_device_string(device_string):
	"""convert device string into device index"""
	if not device_string :
		return 0
	elif device_string in DEVICES  :
		return DEVICES[device_string].real
	elif device_string.startswith('DEVICE') :
		return int(device_string[6:])-1
	else :
		logger.log_error(54,[device_string])
		raise NameError(device_string)



### POINTERS

def get_pointers_controls(controls_settings):
	"""get the pointers controllers linked to the matching functions"""
	return get_controllers_map(controls_settings[CONTROLS_POINTERS],'MOUSE',convert_pointer_string)


def  convert_pointer_string(pointer_string):
	"""convert pointer string into pointer index"""
	if not pointer_string :
		return [0]
	elif pointer_string in POINTERS :
		return [POINTERS[pointer_string].real]
	elif pointer_string.startswith('POINTER') :
		return [int(pointer_string[7:])-1]
	else :
		logger.log_error(53,[pointer_string])
		raise NameError(pointer_string)



### SCROLLERS

def get_scrollers_controls(controls_settings):
	"""get the scrollers controllers linked to the matching functions"""
	return get_controllers_map(controls_settings[CONTROLS_SCROLLERS],'MOUSE',convert_scroller_string)


def convert_scroller_string(scroller_string):
	"""convert scroller string into scroller index"""
	if not scroller_string :
		return [0]
	elif scroller_string in SCROLLERS :
		return [SCROLLERS[scroller_string].real]
	elif scroller_string.startswith('SCROLLER') :
		return [int(scroller_string[8:])-1]
	else :
		logger.log_error(52,[scroller_string])
		raise NameError(scroller_string)



### BUTTONS

def get_buttons_controls(controls_settings):
	"""get the buttons controllers linked to the matching functions"""
	return get_controllers_map(controls_settings[CONTROLS_BUTTONS],'MOUSE',convert_button_string)


def convert_button_string(button_string):
	"""convert button string into button index"""
	if not button_string :
		return [0]
	elif button_string in BUTTONS :
		return [BUTTONS[button_string].real]
	elif button_string.startswith('BUTTON') :
		return [int(button_string[6:])-1]
	else :
		logger.log_error(51,[button_string])
		raise NameError(button_string)



### KEYS

def get_keys_controls(controls_settings):
	"""get the keys controllers linked to the matching functions"""
	return get_controllers_map(controls_settings[CONTROLS_KEYS],'KEYBOARD',convert_key_string)


def convert_key_string(key_name):
	"""convert key string into key index"""
	if not key_name :
		return 0
	elif key_name.startswith('KEY') :
		return int(key_name[3:])
	else:
		### from the 'key name' we get the 'keyval'
		keyval= gdk.keyval_from_name(key_name)
		### from GDK api we need the current display keymap
		### the keymap given by gdk is used for converting 'keyval' into 'keycode'
		display= gdk.Display.get_default()
		keymap= gdk.Keymap.get_for_display(display)
		### each physical key of any keyboard has a unique identifier, this is the 'keycode'
		### ('keycode' is scancode in Windows)
		### each symbols keys have a unique identifier, this is the 'keyval'
		### for example z and Z have the same keycode' but not the same 'keyval'
		### The list of values and name for keyval can be found in the gdk/gdkkeysyms.h
		### ('keyval' is keysym in X)
		entries = gdk.Keymap.get_entries_for_keyval(keymap,keyval)
		if entries[0] : # True if the 'keyval' been found in gdk.Keymap
			keycodes_list=[]
			for entry in entries[1] :
				keycodes_list.append(entry.keycode)
			return keycodes_list
		else :
			logger.log_error(50,[key_name])
			raise NameError(key_name)



### TUNE MODS

def get_options_map(options_settings,convert_function):
	"""get the options settings"""
	new_options_settings={}
	for item in options_settings.items() :
		index=int(item[0])
		data=convert_function(item[1])
		new_options_settings[index]=data
	return new_options_settings


def get_scales_options(controls_settings):
	"""get the scales options settings"""
	return get_options_map(controls_settings[OPTIONS_SCALES],float)


def get_offsets_options(controls_settings):
	"""get the offsets options settings"""
	return get_options_map(controls_settings[OPTIONS_OFFSETS],float)


def get_scrollers_emulators_options(controls_settings):
	"""get the scrollers emulators options settings"""
	return get_options_map(controls_settings[OPTIONS_SCROLLERS_EMULATORS],bool)


def get_pointers_emulators_options(controls_settings):
	"""get the pointers emulators options settings"""
	return get_options_map(controls_settings[OPTIONS_POINTERS_EMULATORS],bool)


