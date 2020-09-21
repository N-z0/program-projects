#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "This is the program centerpiece,can be imported or use by a starter."#information describing the purpose of this module
__status__ = "Prototype"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "3.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2016-02-25"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = ["Rob xxx", "Peter xxx", "Gavin xxxx",	"Matthew xxxx"]#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### import the required modules

import os
from os import path
import appdirs

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,GObject,Gdk


### for output messages to logs systems
from common import logger

### translation, internationalization, localization
from common import translator

import extra#



### The same log message can be used in many cases with different variables
### And here can be displayed a larger part of the complete lines.
LOG1='loading translation domain'
LOG2='translation domain not found'
LOG3='file found:{}'
LOG4='file not found:{}'
LOG11='test module function and class instance'
LOG12='template constante={}'
LOG13='template fonction result:{}'
	
#LANG_DIRECTORY="locale"
UI_DIRECTORY="ui"
ICON_DIRECTORY="logo"

#DEFAULT_DOMAIN="domain" # No program should use a domain with this name "messages", it can cause problems.
UI_FILE='gui.glade'
ICON_FILE='hicolor.svg'

MAIN_WINDOW='main_window'


class App(Gtk.Application):
	"""main software application as object"""
	def __init__(self,user_name,prog_name,cfg,dirs,env):
		"""initialization of the application"""
		Gtk.Application.__init__(self)

		### setup names
		self.prog_name=prog_name
		self.user_name=user_name
		
		### setup path
		self.working_dir=dirs['cwd']
		self.home_dir=dirs['home']
		self.cache_dir=dirs['cache']
		self.data_dir= dirs['data']
		
		### setup ui path
		self.ui_files= [path.join(dir,UI_DIRECTORY,UI_FILE) for dir in self.data_dir] 
		
		### setup icon path name
		self.icon_files=[path.join(dir,ICON_DIRECTORY,ICON_FILE) for dir in self.data_dir]
		
		### setup traduction dirs
		### define where can be find the specified domain.mo file
		#self.lang_dirs=[path.join(dir,LANG_DIRECTORY) for dir in self.data_dir]
		
		### settings for local mode
		local=cfg['SYSTEM']['local']
		if local :
			self.domain = None # DEFAULT_DOMAIN
			self.icon= None
		else :
			self.domain = prog_name
			self.icon = prog_name
			
			
		### because gtk gui builder cannot use paths for specific domain translation
		### in local mode translation is disabled
		if translator.check(self.domain) :
			logger.log_info(LOG1)
			translator.setup(self.domain)
		else :
			logger.log_warning(LOG2)
		#print(translator.get('MSG1'))
			
		
		self.cfg_display=cfg['DISPLAY']
		
		
		#Gtk.Application.set_app_menu()
		#Gtk.Application.set_menubar()
		
		#self.inhibit()
		#self.uninhibit(cookie)
		
		#add_accelerator(accelerator, action_name, parameter)
		#set_accels_for_action(detailed_action_name, accels)


		### test module function and class instance
		logger.log_debug(LOG11)
		self.b=extra.template_fonction()
		self.o=extra.Template_Class_Enfant(template_argument_enfant=12,template_argument_parent=1)

		
	### the function in C activate() becomes do_activate() in Python
	def do_activate(self):
		"""operates the software object"""
		xml = Gtk.Builder()
		### In GTK+ 3.0, resource files have been deprecated and replaced by CSS-like style sheets, which are understood by GtkCssProvider.
		
		### set translation domain
		### didn't found a way for translation from specific domain path
		### so this feature is disabled in local mode(making sense because no user language check is done)
		xml.set_translation_domain(self.domain) # will use an installed domain on platform, otherwise will not translate anything
		#print(xml.get_translation_domain()) # return none or any domain name even if it not existing
		
		### load ui file
		for ui_file in self.ui_files :
			if os.path.isfile(ui_file) :
				logger.log_info(LOG3.format(ui_file))
				break
			else :
				logger.log_warning(LOG4.format(ui_file))
		xml.add_from_file(ui_file) # returns a positive value on success or produce GLib.Error
		self.window = xml.get_object(MAIN_WINDOW)
				
		### icon
		self.window.set_icon_name(self.icon) # use system icon(no error if not existing)
		### Sets an icon to be used as fallback for windows that haven’t had 
		for icon_file in self.icon_files :
			if os.path.isfile(icon_file) :
				logger.log_info(LOG3.format(icon_file))
				break
			else :
				logger.log_warning(LOG4.format(icon_file))
		self.window.set_default_icon_from_file(icon_file)
		

		
		self.window.set_title(self.cfg_display['title'])
		
		position=self.cfg_display['position']
		self.window.move(position[0],position[1])
		
		size=self.cfg_display['size']
		#self.window.set_default_size(size[0],size[1]) # affect only if the window not been shown yet.
		self.window.resize(size[0],size[1]) #works whatever and is shorter
		
		if self.cfg_display['fullscreen'] :
			### with gtk not easy to put directly the window on the cfg chosen screen
			### but when the fullscreen mode is set a screen can be chosen
			monitor= self.cfg_display['screen']
			if monitor==0 : # no changes, window appear on the specified env[DISPLAY] 
				self.window.fullscreen()
			else :
				screen= self.window.get_screen()
				#print(screen,monitor)
				self.window.fullscreen_on_monitor(screen,monitor-1) # -1 because gtk screen index start at 0
		else :
			self.window.unfullscreen()
		
		if self.cfg_display['maximize'] :
			self.window.maximize()
		else :
			self.window.unmaximize()
		
		
		self.window.connect("key-release-event", self.on_key_release)
		self.window.connect('destroy',self.on_window_destroy)
		#self.window.connect("destroy", Gtk.main_quit)
		

		### test module function and class instance
		logger.log_debug(LOG12.format(extra.TEMPLATE_CONSTANTE))
		self.o.template_method_parent(3)
		extra.log_test()
		self.o.template_method_enfant(3)		
		logger.log_debug(LOG13.format(self.b))


		self.window.show_all()
		Gtk.main()


	def on_key_release(self, window, event):
		if event.keyval == Gdk.KEY_Escape:
			self.quit()
		elif event.keyval == Gdk.KEY_f:
			self.fullscreen_mode(window)


	def on_window_destroy(self, windo):
		Gtk.main_quit()
		#self.g_application_quit()

