#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "provide a user interface for the main module."#information describing the purpose of this module
__status__ = "Prototype"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "7.0.0"# version number,date or about last modification made compared to the previous version
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
#from commonz import translator
#from commonz.constants import * 
from commonz.datafiles import ini

### import local modules
import controls # contents helpful function
import main # import the engine module



#LANG_PATH="locale/"
UI_PATH="ui/gtk/gui"
ICON_PATH="logo/hicolor"
CONTROLS_PATH="controls"

#DEFAULT_DOMAIN="domain" # No program should use a domain with this name "messages", it can cause problems.

MAIN_WINDOW="main_window"
GL_AREA="glcanva"
MENU_BAR="menu_bar"
TOOL_BAR="tool_bar"
STATUS_BAR="status_bar"
ABOUT_DIALOG="about_window"

FPS_LAPSE=1. # 1second



class Application(gtk.Application):
	"""software application program"""
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
		self.gl_area=None
		self.window=None
		self.about_dialog=None
		self.menu_bar=None
		self.tool_bar=None
		self.status_bar=None
		
		### default translation domain
		self.domain = None # DEFAULT_DOMAIN
		
		### set starting time and frame number
		self.start_time= 0
		self.old_time= 0
		self.fps_frame= 0
		self.fps_time= 0
		
		### if False app keep processing in loop
		self.stop=False
		
		### main module class instance
		self.main=main.Main(data_pathnames)
		
		### get controls file settings and init controls maps
		self.controls_file= ini.Parser(data_pathnames[CONTROLS_PATH])
		self.pointers_controls_map= {}
		self.scrollers_controls_map= {}
		self.buttons_controls_map= {}
		self.keys_controls_map= {}
		self.pressed_keys_list= []# because i dont know how to disable key-repeat for a widget
		self.pressed_buttons_list= []# prevent any buttons-repeat (just in case)
	
	
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
		self.gl_area = xml.get_object(GL_AREA)
		### the help dialog window
		self.about_dialog = xml.get_object(ABOUT_DIALOG)
		### get the bars
		self.menu_bar=xml.get_object(MENU_BAR)
		self.tool_bar=xml.get_object(TOOL_BAR)
		self.status_bar=xml.get_object(STATUS_BAR)
		
		### if some Event Callbacks are associated with some Widgets in the UI file
		### then the Event Callbacks in the UI file need to be associated with the right functions
		xml.connect_signals(self)# require positional argument
		### can set Mask Events in the UI file
		### (Mask Events are necessary for telling what event is received)
		### but apparently Mask Events from Glade UI files are not imported, 'bug?'
		### so i set the event mask here
		### /!\ POINTER_MOTION_HINT_MASK had been deprecated since GTK version 3.8 /!\
		### POINTER_MOTION_HINT_MASK is used to reduce the number of POINTER_MOTION_MASK events.
		### Normally a POINTER_MOTION_MASK event is received each time the mouse moves.
		### But if the application spends a lot of time processing the event it can lag behind the position of the mouse.
		### When using POINTER_MOTION_HINT_MASK fewer POINTER_MOTION_MASK events will be sent.
		### some of which are marked as a hint (the is_hint member is TRUE).
		### Then to receive more motion events after a motion hint event, the application will needs to asks for more by calling gdk_event_request_motions()
		motion_mask= gdk.EventMask.POINTER_MOTION_MASK # | POINTER_MOTION_HINT_MASK
		button_mask= gdk.EventMask.BUTTON_PRESS_MASK | gdk.EventMask.BUTTON_RELEASE_MASK
		keys_mask= gdk.EventMask.KEY_RELEASE_MASK | gdk.EventMask.KEY_PRESS_MASK
		focus_mask= gdk.EventMask.FOCUS_CHANGE_MASK
		scroll_mask= gdk.EventMask.SCROLL_MASK  | gdk.EventMask.SMOOTH_SCROLL_MASK
		enter_mask= gdk.EventMask.LEAVE_NOTIFY_MASK  | gdk.EventMask.ENTER_NOTIFY_MASK
		self.gl_area.set_events( motion_mask|button_mask|keys_mask|focus_mask|scroll_mask|enter_mask )
		#print("OpenGL area events mask:",self.gl_area.get_events())
		
		### Sets the required version of OpenGL to be used when creating the context for the widget.
		### This function must be called before the area has been realized and the context created
		### GL context versions less than 3.2 are not supported
		self.gl_area.set_required_version(4,3)#(3,2)
		
		### link controls with functions
		controls_settings= self.controls_file.get_dictionary()# get setting from file
		self.keys_controls_map=  controls.get_keys_controls(controls_settings)
		self.buttons_controls_map= controls.get_buttons_controls(controls_settings)
		self.pointers_controls_map= controls.get_pointers_controls(controls_settings)
		self.scrollers_controls_map= controls.get_scrollers_controls(controls_settings)
		### set main controls options
		for item in controls.get_scales_options(controls_settings).items() : self.main.set_scale_cfg(item[0],item[1])
		for item in controls.get_offsets_options(controls_settings).items() : self.main.set_offset_cfg(item[0],item[1])
		for item in controls.get_scrollers_emulators_options(controls_settings).items() : self.main.set_scroller_emulator_cfg(item[0],item[1])
		for item in controls.get_pointers_emulators_options(controls_settings).items() : self.main.set_pointer_emulator_cfg(item[0],item[1])
		
		### ask to show the main window and the all is contents
		self.window.show_all()
		
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
	
	
	def setup_gl_area(self,gl_area):
		"""setup the OpenGL area"""
		### this event happen after the call of activate() (do_activate() in Python)
		### and after the GLContext creation
		### the call is made by the gtk.Widget “realize“ signal
		### and its needed to initialize OpenGL state, e.g. buffer objects or shaders,
		logger.log_debug(17)
		
		### We need to make the context current if we want to call GL API
		gl_area.make_current()
		
		### Checks If some errors during the creation or initialization of the gdk.GLContext,
		### function will return a Gio.Error for you to catch
		### this function will return a Gio.Error for you to catch
		gl_area_error= gl_area.get_error()
		if gl_area_error :
			logger.log_error(18,gl_area_error)
		
		### Retrieves the required version for OpenGL
		logger.log_info(19,gl_area.get_required_version())
		
		### When realizing GDK will try to use the OpenGL 3.2 core profile
		### this profile removes all the OpenGL API that was deprecated prior to the 3.2 version
		### If its successful, this function will return False
		### If bot GDK will fall back to a pre-3.2 profile, and this function will return True
		### (The GdkGLContext must be realized before checking legacy)
		context = gl_area.get_context()
		logger.log_info(20,[gdk.GLContext.is_legacy(context)]) # does not allow None as context value
		
		### creates framebuffers for rendering onto.
		### If has_alpha is True the buffer allocated by the widget will have an alpha channel component
		### and when rendering to the window it will be composited over whatever is below the widget.
		### can choose to enable any buffers in the UI Glade file
		#gl_area.set_has_alpha(True)
		#gl_area.set_has_depth_buffer(True)
		#gl_area.set_has_stencil_buffer(False)
		### no need to set double_buffered True because its the default for all widgets
		# gl_area.set_double_buffered(True)
		### If has_alpha is FALSE there will be no alpha channel and thebuffer will fully replace anything below the widget.
		logger.log_info(21,[gl_area.get_has_alpha()])
		### If has_depth_buffer is True the widget will allocate and enable a depth buffer
		logger.log_info(22,[gl_area.get_has_depth_buffer()])
		### If has_stencil_buffer is True the widget will allocate and enable a stencil buffer
		logger.log_info(23,[gl_area.get_has_stencil_buffer()])
		
		### no need to set set_auto_render(True)
		### because in the mainloop we ask for a redraw when necessary
		### If auto_render is True the “render” signal will beemitted every time the widget draws. This is the default and isuseful if drawing the widget is faster. If auto_render is FALSE the data from previous rendering is keptaround and will be used for drawing the widget the next time,unless the window is resized. In order to force a renderingGtk.GLArea:queue_render() must be called. This mode is useful whenthe scene changes seldomly, but takes a long time to redraw.
		### can set it in the UI Glade file
		#gl_area.set_auto_render(False)
		
		### record the starting time
		### and request a callback for computing on time the main things
		### it will signal every time before openGL widget is ready to draw
		gl_area_clock= gl_area.get_frame_clock()
		self.start_time= gl_area_clock.get_frame_time()/1000000#(from microsecond to seconds)
		self.gl_area.add_tick_callback( self.on_frame_tick )
		
	
	def on_context(self, gl_area):
		"""makes the right context for OpenGL"""
		### the "context" call is made before the “realize“ signal
		### GLContext contains all of the information that will be used by the OpenGL system to render
		### each GLContext represent a separate viewable surface in window application
		### its not needed to custom GLContext except for special instances
		### or if you want to reuse an existing GLcontext
		### GtkGLArea setup is own GLContext and associate it with the widget drawing area,
		### keeping it updated when the size and position of the drawing area changes.
		logger.log_debug(24)
		context = gl_area.get_context()
		### need to return the new GLContext
		return context
	
	
	def on_about_dialog(self, *args):#
		"""help dialog window is requested"""
		### get reponse of the dialog window when it close
		logger.log_debug(25)
		response = self.about_dialog.run()
		### then hide the dialog window
		self.about_dialog.hide()
	
	
	def on_toggle_menubar(self, *args):
		"""toggle the visibility of the menu bar"""
		logger.log_debug(26)
		### To toggle the visibility of a widget use the show() and hide()
		### or map() and unmap() if don't want other widgets in window to move around.
		if self.menu_bar.is_visible():# if the widget and all its parents are marked asvisible
			self.menu_bar.hide()
		else :
			self.menu_bar.show()
	
	
	def on_toggle_toolbar(self, *args):
		"""toggle the visibility of the tool bar"""
		logger.log_debug(27)
		### To toggle the visibility of a widget use the show() and hide()
		### or map() and unmap() if don't want other widgets in window to move around.
		if self.tool_bar.is_visible():# if the widget and all its parents are marked asvisible
			self.tool_bar.hide()
		else :
			self.tool_bar.show()
	
	
	def on_toggle_statusbar(self, *args):
		"""toggle the visibility of the status bar"""
		logger.log_debug(28)
		### To toggle the visibility of a widget use the show() and hide()
		### or map() and unmap() if don't want other widgets in window to move around.
		if self.status_bar.is_visible():# if the widget and all its parents are marked asvisible
			self.status_bar.hide()
		else :
			self.status_bar.show()
	
	
	def on_enter(self, gl_area, *args):
		"""pointer entered the widget area"""
		logger.log_debug(29)
		### gives the focus to the widget,
		### focused widget will receive keyboards inputs events
		gl_area.grab_focus()
	
	
	def on_leave(self, gl_area, *args):
		"""pointer left the widget area"""
		logger.log_debug(30)
		### just unfocus (focus nothing) because dont know how to give the focus to another widget
		self.window.set_focus(None)
	
	
	def on_focus_in(self, gl_area, *args):
		"""The widget received the the focus"""
		logger.log_debug(31)
		self.main.focus_in()
	
	
	def on_focus_out(self, gl_area, *args):
		"""The widget lost the focus"""
		logger.log_debug(32)
		### signal the unfocus to the main part
		self.main.focus_out()
		### because i dont know how to disable key-repeat for a widget
		self.pressed_keys_list= []# remove all not released keys inside gl_area
		self.pressed_buttons_list= []# remove all not released buttons inside gl_area
	
	
	def on_render(self, gl_area, *args):
		"""render OpenGL scene into the window area"""
		logger.log_debug(33)
		
		### This function is automatically called before emitting the “render” signal
		### and doesn't normally need to be called by application code
		### GtkGLArea ensures that framebuffers is the default GL rendering target when rendering
		#widget.make_current()
		#widget.attach_buffers()
		
		self.main.display()
		
		### the draw commands will be flushed at the end of the signal emission chain
		### and the buffers will be drawn on the window
		### (i dont know why returning True but on the official exemple they do )
		return True
	
	
	def on_resize(self,gl_area,width,height):
		"""manage the new size of the window"""
		### no need to ask for a redraw after the resize
		### after resizing a redraw request is sent automatically
		logger.log_debug(34)
		
		### can also get the size with
		#w = gl_area.get_allocated_width()
		#h = gl_area.get_allocated_height()
		
		### set the opengl cameras ratio aspect
		self.main.resize((width,height))
	
	
	def on_mouse_move(self, gl_area, event):
		"""mouse movement event"""
		logger.log_debug(35)
		
		#print("is_hint",event.is_hint)# i dont know how to use it
		#print("send_event",event.send_event)# i dont know how to use it
		source=event.device.get_source()
		#name=source.value_name # ex: GDK_SOURCE_MOUSE
		#name=source.value_nick # ex: mouse
		#name=event.device.get_name() # ex: #Virtual core pointer # its not model or brand name, just a generic name
		device_index=source.real# dont know wich one is the good one
		#device_index=source.numerator# dont know wich one is the good one
		time=(event.time-self.start_time)/1000# when the event happened (from millisecond to seconds)
		#print("axes:",event.axes)# if device is not a mouse.(its a single valu)
		#state=event.state)#a bit-mask representing the state of the modifier keys
		position= (event.x,event.y)# position relative to gl_area , no event.z
		### can also get position by the gtk.gdk.Window get_pointer() method
		#x, y, mask = gl_area.get_pointer()
		### There is also gtk.Widget method get_pointer() which provides the same(without mask)
		
		if device_index in self.pointers_controls_map :
			for position_index in range(2) :# there is no Z
				if position_index in self.pointers_controls_map[device_index] :
					for function_index in self.pointers_controls_map[device_index][position_index] :
						self.main.set_pointer_value(function_index,position[position_index],time)
		
		###Reading the mouse position is easy
		### but we have to take care to put the cursor back to the center of the screen,
		### or it will soon go outside the window and you won’t be able to move anymore.
		#w = gl_area.get_allocated_width()
		#h = gl_area.get_allocated_height()
		#glfwSetMousePos(w/2, h/2)# Reset mouse position for next frame
		
		### the documentation says it should be used instead of gdk_window_get_pointer()
		### apparently it doesn't change things
		### certainty i dont know how to use it
		#gdk.event_request_motions(event)
	
	
	def on_mouse_scroll(self, gl_area,event):
		"""mouse scroll event"""
		### some mouses have wheels generating scroll events
		logger.log_debug(36)
		
		source=event.device.get_source()
		#name=source.value_name # ex: GDK_SOURCE_MOUSE
		#name=source.value_nick # ex: mouse
		#name=event.device.get_name() # ex: #Virtual core pointer # its not model or brand name, just a generic name
		device_index=source.real# dont know wich one is the good one
		#device_index=source.numerator# dont know wich one is the good one
		position= (event.x,event.y)# position relative to gl_area
		time=(event.time-self.start_time)/1000# when the event happened (from millisecond to seconds)
		
		### event.direction can be: GDK_SCROLL_UP GDK_SCROLL_DOWN GDK_SCROLL_LEFT GDK_SCROLL_RIGHT
		### or if event.direction is GDK_SCROLL_SMOOTH event.deltas can be obtained
		direction=event.direction
		delta=[0,0]# there is no Z
		if direction==gdk.ScrollDirection.SMOOTH :
			### with my computer device delta_x is always 0 and there is no delta_z
			### the delta at first call of Scroll with SMOOTH Direction is = 0,0
			delta[0]=event.delta_x
			delta[1]=event.delta_y
		elif direction==gdk.ScrollDirection.LEFT :
			delta[0]=-1
		elif direction==gdk.ScrollDirection.RIGHT :
			delta[0]=1
		elif direction==gdk.ScrollDirection.UP :
			delta[1]=1
		elif direction==gdk.ScrollDirection.DOWN :
			delta[1]=-1
		
		if device_index in self.scrollers_controls_map :
			for delta_index in range(2) :# there is no Z
				if delta_index in self.scrollers_controls_map[device_index] and delta[delta_index]!=0 :
					for function_index in self.scrollers_controls_map[device_index][delta_index] :
						self.main.set_scroller_value(function_index,delta[delta_index],position,time)
	
	
	def on_button_press(self, gl_area, event):
		"""mouse button pressed"""
		logger.log_debug(37)
		source=event.device.get_source()
		#name=source.value_name # ex: GDK_SOURCE_MOUSE
		#name=source.value_nick # ex: mouse
		#name=event.device.get_name() # ex: #Virtual core pointer # its not model or brand name, just a generic name
		device_index=source.real# dont know wich one is the good one
		#device_index=source.numerator# dont know wich one is the good one
		position= (event.x,event.y)# position relative to gl_area
		time=(event.time-self.start_time)/1000# when the event happened (from millisecond to seconds)
		button_code=event.button
		
		if device_index in self.buttons_controls_map :
			if button_code in self.buttons_controls_map[device_index] :
				### normally there is no repeat for buttons but just in case of gtk changes
				if not (device_index,button_code) in self.pressed_buttons_list :
					for function_index in self.buttons_controls_map[device_index][button_code] :
						self.main.set_button_press(function_index,position,time)
					### prevent future repeat of buttons
					self.pressed_buttons_list.append((device_index,button_code))
	
	
	def on_button_release(self, gl_area, event):
		"""mouse button released"""
		logger.log_debug(38)
		source=event.device.get_source()
		#name=source.value_name # ex: GDK_SOURCE_MOUSE
		#name=source.value_nick # ex: mouse
		#name=event.device.get_name() # ex: #Virtual core pointer # its not model or brand name, just a generic name
		device_index=source.real# dont know wich one is the good one
		#device_index=source.numerator# dont know wich one is the good one
		position= (event.x,event.y)# position relative to gl_area
		time=(event.time-self.start_time)/1000# when the event happened (from millisecond to seconds)
		button_code=event.button
		
		### normally there is no repeat for buttons but just in case of gtk changes
		combo=(device_index,button_code)
		if combo in self.pressed_buttons_list :
			for function_index in self.buttons_controls_map[device_index][button_code] :
				self.main.set_button_release(function_index,position,time)
			### remove pressed buttons allowing to press it again
			self.pressed_buttons_list.remove(combo)
	
	
	def on_key_press(self, gl_area, event):
		"""proceed press keys events"""
		### gl_area can send key-press-events only if focused
		logger.log_debug(39)
		source_device=event.get_source_device()
		source= source_device.get_source()
		device_index=source.real# dont know wich one is the good one
		#device_index=source.numerator# dont know wich one is the good one
		time=(event.time-self.start_time)/1000# when the event happened (from millisecond to seconds)
		#print('is_modifier',event.is_modifier)# always return 0
		### event.state contains the modifiers keys pressed at same time
		#mods=event.state.numerator
		#mods=event.state.real
		### groups are not used on standard US keyboards,
		### but are used in many other countries.
		### On a keyboard with groups, there can be 3 or 4 symbols printed on a single key.
		#print('group:',event.group)
		### level indicates which symbol on the key will be used in a vertical direction.
		### on a standard US keyboard for the key with 1 and ! the level indicates what symbol to use
		#print('level:',dir(event.level) # not available
		### string is nothing if the key is not a character
		string= event.string
		### length= 1 if the key is a character or 0 if its control key
		#length= event.length
		### each physical key of any keyboard has a unique identifier, this is the 'keycode'
		### ('keycode' is scancode in Windows) 
		keycode=event.hardware_keycode
		### each symbols keys have a unique identifier, this is the 'keyval'
		### for example z and Z have the same keycode but not the same keyval
		### The list of values and name for keyval can be found in the gdk/gdkkeysyms.h
		### ('keyval' is keysym in X)
		#keyval= event.keyval
		
		combo=(device_index,keycode)
		if device_index in self.keys_controls_map :
			if keycode in self.keys_controls_map[device_index] :
				### because i dont know how to disable key-repeat for a widget
				if not combo in self.pressed_keys_list :
					for function_index in self.keys_controls_map[device_index][keycode] :
						self.main.set_key_press(function_index,string,time)
					self.pressed_keys_list.append(combo)
		
		### return True prevent the lost of focus when arrows keys are pressed
		return True
	
	
	def on_key_release(self, gl_area, event):
		"""proceed release keys events"""
		### gl_area can send key-release-events only if focused
		logger.log_debug(40)
		source_device=event.get_source_device()
		source= source_device.get_source()
		device_index=source.real# dont know wich one is the good one
		#device_index=source.numerator# dont know wich one is the good one
		time=(event.time-self.start_time)/1000# when the event happened (from millisecond to seconds)
		#print('is_modifier',event.is_modifier)# always return 0
		### event.state contains the modifiers keys pressed at same time
		#mods=event.state.numerator
		#mods=event.state.real
		### groups are not used on standard US keyboards,
		### but are used in many other countries.
		### On a keyboard with groups, there can be 3 or 4 symbols printed on a single key.
		#print('group:',event.group)
		### level indicates which symbol on the key will be used in a vertical direction.
		### on a standard US keyboard for the key with 1 and ! the level indicates what symbol to use
		#print('level:',dir(event.level) # not available
		### string is nothing if the key is not a character
		string= event.string
		### length= 1 if the key is a character or 0 if its control key
		#length= event.length
		### each physical key of any keyboard has a unique identifier, this is the 'keycode'
		### ('keycode' is scancode in Windows) 
		keycode=event.hardware_keycode
		### each symbols keys have a unique identifier, this is the 'keyval'
		### for example z and Z have the same keycode but not the same keyval
		### The list of values and name for keyval can be found in the gdk/gdkkeysyms.h
		### ('keyval' is keysym in X)
		#keyval= event.keyval
		
		### need to prevent release of keys pressed outside gl_area
		combo=(device_index,keycode)
		if combo in self.pressed_keys_list :
			for function_index in self.keys_controls_map[device_index][keycode] :
					self.main.set_key_release(function_index,string,time)
			### because i dont know how to disable key-repeat for a widget
			self.pressed_keys_list.remove(combo)
	
	
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
		logger.log_debug(42)
		
		### request to stop the engines
		self.main.stop()
		
		### instructs main loop to terminate
		### the GTK mainloop is not use but just in case
		gtk.main_quit()
		### stop the custom main loop
		self.stop=True
		
		### It should return True if not want to close the window
		### If returns False then a destroy event will be sent.
		### Usually it is used to present an confirm dialog:(“Are you sure you want to quit ?”)
		return False
	
	
	def on_frame_tick(self,gl_area,clock):
		"""run the main loop every time"""
		### called before each frame
		### usually at the frame rate of the output device (60Hz 12ms)
		logger.log_debug(43)
		
		### Returns the counter of the oldest frame drawn available in history.
		### only when queue_render() is called a timer is kept in the history
		#frame_number = clock.get_history_start()
		#print("frame_number:",frame_number)
		### we use the given frame_number to identify and get the corresponding timer.
		#timer= clock.get_timings(frame_number)
		#print("last frame timer: ",timer.get_frame_time())
		
		### get FPS
		### not available for now
		### maybe my gtk version not match
		#print("fps:",clock.get_fps())
		
		### get a 64-bit counter that increments at each callback time
		### The frame counter does not advance during the frame is hiding,
		#print("frame counter:",clock.get_frame_counter())
		
		### gets the current time
		### timestamp is in microseconds
		### in the timescale of of g_get_monotonic_time()
		### The timestamp does not advance during the frame is hiding,
		### its a gint64 A signed integer guaranteed to be 64 bits on all platforms.
		### values can range from G_MININT64 (= -9,223,372,036,854,775,808) to G_MAXINT64 (= 9,223,372,036,854,775,807) 
		#print('frame time:',clock.get_frame_time())
		### same as calling get_frame_time() from the widget
		#print("frame_clock:", gl_area.get_frame_clock() )
		
		### Predicts the presentation time of the next frame, based on timers history
		### but i have no idea of what base_time valu must be
		#print('clock refresh info:',clock.get_refresh_info(base_time))
		
		### Asks the frame clock to run on particular phase.
		### seems to let choose at what moment the timer callback is sent
		### GDK_FRAME_CLOCK_PHASE_UPDATE GDK_FRAME_CLOCK_PHASE_PAINT
		### i think by default a call before each frame is ok so no need to change
		#clock.request_phase(phase)
		
		### can also get FrameClock
		### for the frame currently being processed,
		### or if no frame is being processed for the previous frame
		### or returns NULL if any frames have been processed yet
		#timer=clock.get_current_timings()
		
		### no need to check if the clock system reset
		### because the timestamp and frame counter use 64bits so they should "never" reset... i hope so...
		frame=clock.get_frame_counter()
		### frame_time is converted for matching others event timers
		time=(clock.get_frame_time()/1000000)-self.start_time # from microsecond to seconds
		laps=time-self.old_time
		self.old_time=time
		
		### FPS calculation
		if time-self.fps_time >= FPS_LAPSE :
			frame_quantum=frame-self.fps_frame
			self.set_statusbar("FPS:"+str(frame_quantum))
			self.fps_frame=frame
			self.fps_time=time
		
		### need it here or the Opengl will fail
		self.gl_area.make_current()
		if self.main.proceed(frame,time,laps) :
			### ask to redraw the gl_area if proceed returned True
			self.gl_area.queue_render()
		
		### Keep going by returning True
		### or stop receiving callback by calling gtk_widget_remove_tick_callback() or return False
		return True
		
		
	def hide_cursor(self):#
		"""hide the cursor pointer"""
		logger.log_debug(44)
		
		cursor = gdk.Cursor.new(gdk.CursorType.BLANK_CURSOR)
		
		### Sets the cursor to be shown when pointer devices point towards widget.
		### If the cursor is NULL, widget will use the cursor inherited from the parent widget.
		self.window.get_window().set_cursor(cursor)
	
	
	def set_statusbar(self,text_message):#
		"""set statusbar text"""
		### to display messages, the statusbar widget use Context Identifiers,
		### Context Identifiers allow different parts of an application to use the same statusbar
		### each Context Identifiers are used to identify different "users"
		logger.log_debug(45,[text_message])
		
		### A new Context Identifier is requested using a call to the following method
		### with a short textual description of the context
		context_id= self.status_bar.get_context_id("any_context_description")
		
		### add a specific message on top of the statusbar stack
		message_id= self.status_bar.push(context_id,text_message)
		
		### remove the last message from the top of the stack
		#self.status_bar.pop(self.context_id)
		
		### remove a specific message from a specific context
		#self.status_bar.remove(self.context_id,message_id)
	
	