#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "provide a user interface for the main module."#information describing the purpose of this module
__status__ = "Prototype"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "6.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
#__copyright__ = "Copyright 2000, The X Project"
__date__ = "2016-02-25"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = ["Rob xxx", "Peter xxx", "Gavin xxxx",	"Matthew xxxx"]#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



### gi provides bindings for GObject based libraries such as GTK, GStreamer, WebKitGTK, GLib, GIO and many more.
import gi
### GTK is a GUI toolkit
### it provides buttons and text entry boxes
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
### GDK is an library use by GTK to abstract the details of the display
### it to actually create the windows in a way that the X server, or your Apple box, or your Windows box understands.
from gi.repository import Gdk as gdk
### GObject for threading with idle_add timeout_add callbacks 
from gi.repository import GObject as go
### as soon as possible enable threading in the PyGTK app.
go.threads_init()

### import the required commonz modules
from commonz import logger
from commonz import translator

### import the engine module
import main



#LANG_PATH="locale/"
UI_PATH="ui/gtk/gui"
ICON_PATH="logo/hicolor"

#DEFAULT_DOMAIN="domain" # No program should use a domain with this name "messages", it can cause problems.

MAIN_WINDOW="main_window"
MENU_BAR="menu_bar"
TOOL_BAR="tool_bar"
STATUS_BAR="status_bar"
ABOUT_DIALOG="about_window"



class Application(gtk.Application):
	"""software application as object"""
	def __init__(self,prog_name,cfg,dirs,data_pathnames,env):
		"""initialization of the application"""
		gtk.Application.__init__(self)
		
		### setup names
		self.prog_name=prog_name
		
		### user paths
		self.working_dir=dirs['cwd']
		self.home_dir=dirs['home']
		self.cache_dir=dirs['cache']
		
		### get settings from env variables
		self.host_name=env.get('HOSTNAME') # name of the computer
		self.host_type=env.get('HOSTTYPE')# eg: x86_64
		self.ifs=env.get('IFS') # eg:  \t\n
		self.user= env.get('USERNAME') or env.get('LOGNAME') or env.get('USER') # current user name
		self.desktop= env.get('XDG_CURRENT_DESKTOP') or env.get('XDG_SESSION_DESKTOP') or env.get('DESKTOP_SESSION') #eg: xfce
		self.seat=env.get('XDG_SEAT') # eg: seat0
		self.monitor=env.get('DISPLAY') # the display used by X. This variable is usually set to :0.0, which means the first display on the current computer
		self.mails_path=env.get('MAIL') #the location of the user’s mail spool. Usually /var/spool/mail/USER
		self.time_zone=env.get('TZ') #the time zone
		self.lang=env.get('LANG') or env.get('LANGUAGE') #eg: en_US.UTF-8
		self.lc_address=env.get('LC_ALL') or env.get('LC_ADDRESS')
		self.lc_name=env.get('LC_ALL') or env.get('LC_NAME')
		self.lc_monetary=env.get('LC_ALL') or env.get('LC_MONETARY')
		self.lc_measurement=env.get('LC_ALL') or env.get('LC_MEASUREMENT')
		self.lc_time=env.get('LC_ALL') or env.get('LC_TIME')
		self.lc_numeric=env.get('LC_ALL') or env.get('LC_NUMERIC')
		
		### get settings from cfg
		cfg_system=cfg['SYSTEM']
		self.local=cfg_system['local']
		cfg_display=cfg['DISPLAY']
		self.title=cfg_display['title']
		self.position=cfg_display['position']
		self.size=cfg_display['size']
		self.fullscreen=cfg_display['fullscreen']
		self.monitor= cfg_display['screen']# or self.monitor # if this env variable is set the window will be automatically placed at the right place
		self.maximize=cfg_display['maximize']
		
		### data pathnames
		self.data_pathnames= data_pathnames
		
		### later those widget will be set
		self.window=None
		self.about_dialog=None
		self.menu_bar=None
		self.tool_bar=None
		self.status_bar=None
		
		### default translation domain
		self.domain = None # DEFAULT_DOMAIN
		
		### if True app keep processing in loop 
		self.proced=True
	
		### main module class instance
		self.main=main.Advanced_Main(adv_main_template_argument=3,main_template_argument=1)
	
	
	def do_activate(self):
		"""load and set the UI interface"""
		### will be exectuded when starter module will call a.run()
		### (the function in C activate() becomes do_activate() in Python)
		logger.log_debug(6)
		
		### In GTK+ 3.0, resource files have been deprecated and replaced by CSS-like style sheets, which are understood by GtkCssProvider.
		xml = gtk.Builder()
		
		### setup translation
		### find the domain.mo file
		#lang_file=self.data_pathnames[LANG_PATH]
		### in local mode translation is disabled
		### because i didn't found how to use a specific domain.mo file
		if not self.local :
			self.domain = self.prog_name
			### with gtk the translation is not done by the translator module
			#if translator.check(self.domain) :
			#	logger.log_debug(7)
			#	translator.setup(self.domain)
			#	#print(translator.get('MSG1'))
			#else :
			#	logger.log_warning(8)
			### apparently gtk gui builder cannot use a specific domain translation file as-well
			xml.set_translation_domain(self.domain) # will use an installed domain on platform, otherwise will not translate anything
			### check if translation system is effective
			#xml.get_translation_domain() : # return none or any domain name even if it not existing
			logger.log_debug(7)
			
		### load ui file
		ui_file=self.data_pathnames[UI_PATH]
		logger.log_info(9,[ui_file])
		xml.add_from_file(ui_file) # returns a positive value on success or produce GLib.Error
		
		### retrieve from the ui file some important widgets
		### for later be able to interacts with them
		self.window = xml.get_object(MAIN_WINDOW)
		### the help dialog window
		self.about_dialog = xml.get_object(ABOUT_DIALOG)
		### get the bars
		self.menu_bar=xml.get_object(MENU_BAR)
		self.tool_bar=xml.get_object(TOOL_BAR)
		self.status_bar=xml.get_object(STATUS_BAR)
		
		### if some Event Callbacks are associated with some Widgets in the UI file
		### then the Event Callbacks in the UI file need to be associated with the right functions
		xml.connect_signals(self)# require positional argument
		
		
		### ask to show the main window and the all is contents
		self.window.show_all()
		
		### there is many ways for idle processing
		### but not all have the same efficience
		### The gobject.idle_add() function adds a function to be called whenever there are no higher priority events pending to the default main loop.
		#go.idle_add(priority=go.PRIORITY_DEFAULT_IDLE,function=self.on_idle)
		### The gobject.timeout_add() function sets a function to be called at regular intervals, with the default priority
		#go.timeout_add(50, self.on_timer)# Add a 20fps (50ms) timer
		### Or we can start up the main loop just after application initialization.
		go.timeout_add(100,self.mainloop)# 100ms delay is just for let the application finish settings first
		
		### start GTK loop and sending events
		gtk.main()
	
	
	def setup_main_window(self,window):
		"""set the main window graphic interface"""
		### this event happen after the call of activate() (do_activate() in Python)
		### its call by the gtk.Widget “realize“ signal
		logger.log_debug(10)
		
		### the icon can be specified in the ui file.
		### but the name of the icon must be the name of program,
		### i dont want makes the ui file program dependent.
		if not self.local : # settings for local mode
			window.set_icon_name(self.prog_name) # use system icon(no error if not existing)
		### Sets an icon file to be used as fallback for windows that haven’t had
		icon_file=self.data_pathnames[ICON_PATH]
		logger.log_info(11,[icon_file])
		window.set_default_icon_from_file(icon_file)
		
		### because i dont want makes ui file dependent on the program.
		### window title is set here
		window.set_title(self.title)
		
		window.move(self.position[0],self.position[1])
		logger.log_info(12,self.position)
		#window.set_default_size(self.size[0],self.size[1]) # affect only if the window not been shown yet.
		window.resize(self.size[0],self.size[1]) #works whatever and is shorter
		logger.log_info(13,self.size)
		
		if self.fullscreen :
			### with gtk not easy to put directly the window on the cfg chosen screen
			### but when the fullscreen mode is set a screen can be chosen
			logger.log_debug(14)
			if self.monitor==0 : # no changes requested, window will appear on the specified env[DISPLAY]
				window.fullscreen()
			else :
				screen= window.get_screen()
				window.fullscreen_on_monitor(screen,self.monitor-1) # -1 because gtk screen index start at 0
				logger.log_info(15,[screen,self.monitor])
		else :
			window.unfullscreen()
		
		if self.maximize :
			window.maximize()
			logger.log_debug(16)
		else :
			window.unmaximize()
		
		### Inform the session manager that certain types of actions should be inhibited.
		### This is not guaranteed to work on all platforms and for all types of actions.
		### Applications should invoke this method when they begin an operation that should not be interrupted, such as creating a CD or DVD.
		### The types of actions that may be blocked are specified by the flags parameter.
		#reason= "A short, human-readable string that explains why these operations are inhibited."
		#flags= gtk.ApplicationInhibitFlags.LOGOUT|gtk.ApplicationInhibitFlags.SWITCH|gtk.ApplicationInhibitFlags.SUSPEND|gtk.ApplicationInhibitFlags.IDLE
		#self.inhibitor=self.inhibit(window,flags,reason)
		### When the application completes the operation it should remove the inhibitor.
		### Note that an application can have multiple inhibitors, and all of them must be individually removed.
		### (Inhibitors are also cleared when the application exits.)
		#self.uninhibit(self.inhibitor)
	
	def on_about_dialog(self, *args):#
		"""help dialog window is requested"""
		### get reponse of the dialog window when it close
		logger.log_debug(17)
		response = self.about_dialog.run()
		### then hide the dialog window
		self.about_dialog.hide()
	
	
	def on_toggle_menubar(self, *args):
		"""toggle the visibility of the menu bar"""
		logger.log_debug(18)
		### To toggle the visibility of a widget use the show() and hide()
		### or map() and unmap() if don't want other widgets in window to move around.
		if self.menu_bar.is_visible():# if the widget and all its parents are marked asvisible
			self.menu_bar.hide()
		else :
			self.menu_bar.show()
	
	
	def on_toggle_toolbar(self, *args):
		"""toggle the visibility of the tool bar"""
		logger.log_debug(19)
		### To toggle the visibility of a widget use the show() and hide()
		### or map() and unmap() if don't want other widgets in window to move around.
		if self.tool_bar.is_visible():# if the widget and all its parents are marked asvisible
			self.tool_bar.hide()
		else :
			self.tool_bar.show()
	
	
	def on_toggle_statusbar(self, *args):
		"""toggle the visibility of the status bar"""
		logger.log_debug(20)
		### To toggle the visibility of a widget use the show() and hide()
		### or map() and unmap() if don't want other widgets in window to move around.
		if self.status_bar.is_visible():# if the widget and all its parents are marked asvisible
			self.status_bar.hide()
		else :
			self.status_bar.show()
	
	
	def on_unrealize(self,widget):#
		"""uninitialize the app before exit"""
		### this event happen after DELETE and before DESTROY
		### call from the gtk.Widget “unrealize“ signal
		logger.log_debug(21)
	
	
	def on_exit(self, *args):
		"""exit the application"""
		### usually activate by choosing to close program by the menubar or shortcut
		### then close the window and a delete_event will be sent automatically
		self.window.close()
	
	
	def on_delete(self, window, *args):#
		"""delete application window"""
		### this event happen when delete-event signal is received
		### usually when try to close the window a delete_event event is sent.
		### it can be used to interact with the user before the sent of destroy-event.
		logger.log_debug(22)
		
		### instructs main loop to terminate
		### the GTK mainloop is not use but just in case
		gtk.main_quit()
		### stop the custom main loop
		self.proced=False
		
		### It should return True if not want to close the window
		### If returns False then a destroy event will be sent.
		### Usually it is used to present an confirm dialog:(“Are you sure you want to quit ?”)
		return False
	
	
	def on_idle(self):
		"""to run code whenever there is nothing else to do"""
		### The downside is that other events (like mouse movement) take priority over idle event, or vice versa,
		### which leads to animation stuttering when lots of external events happen,
		### or else delays in processing external events while animation is running.
		logger.log_debug(23)
		
		### place for doing things
		### test module function and class instance
		logger.log_debug(28,[main.TEMPLATE_CONSTANTE])
		self.main.template_method(3)
		self.main.adv_template_method(3)
		
		### if return True the function will be requeued for the next idle time.
		if self.proced :
			return True
	
	
	def on_timer(self):
		"""to run code at time intervals """
		### One problem with timer events is that the timer only starts counting again after the function returns.
		### So, if the timer is set to 30ms and your function takes 20ms to execute, it will be called 50ms after it was first called.
		### A second problem is that if the millisecond count not enough for all other events to be processed between timer events,
		### you can starve the event queue in such a way that other events will never happen.
		logger.log_debug(24)
		
		### place for doing things
		### test module function and class instance
		logger.log_debug(28,[main.TEMPLATE_CONSTANTE])
		self.main.template_method(3)
		self.main.adv_template_method(3)
		
		return True
	
	
	def mainloop(self):
		"""to run code in a main loop"""
		#logger.log_debug(25)
		while self.proced :
			
			### Process all pending events.
			while gtk.events_pending():
				gtk.main_iteration()
			
			### place for doing things
			### test module function and class instance
			logger.log_debug(28,[main.TEMPLATE_CONSTANTE])
			self.main.template_method(3)
			self.main.adv_template_method(3)
	
	
	def set_statusbar(self,text_message):#
		"""set statusbar text"""
		### to display messages, the statusbar widget use Context Identifiers,
		### Context Identifiers allow different parts of an application to use the same statusbar
		### each Context Identifiers are used to identify different "users"
		logger.log_debug(26,[text_message])
		
		### A new Context Identifier is requested using a call to the following method
		### with a short textual description of the context
		context_id= self.status_bar.get_context_id("any_context_description")
		
		### add a specific message on top of the statusbar stack
		message_id= self.status_bar.push(context_id,text_message)
		
		### remove the last message from the top of the stack
		#self.status_bar.pop(self.context_id)
		
		### remove a specific message from a specific context
		#self.status_bar.remove(self.context_id,message_id)
	
	