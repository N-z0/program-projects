#!/usr/bin/env python3
#coding: utf-8
### 1st line allows to execute this script by typing only its name in terminal, with no need to precede it with the python command
### 2nd line declaring source code charset should be not necessary but for exemple pydoc request it



__doc__ = "provide multilingual translation, internationalization, localization for text messages."#information describing the purpose of this modul
__status__ = "Development"#should be one of 'Prototype' 'Development' 'Production' 'Deprecated' 'Release'
__version__ = "v1.0.0"# version number,date or about last modification made compared to the previous version
__license__ = "public domain"# ref to an official existing License
__date__ = "2020-06-18"#started creation date / year month day
__author__ = "N-zo syslog@laposte.net"#the creator origin of this prog,
__maintainer__ = "Nzo"#person who curently makes improvements, replacing the author
__credits__ = []#passed mainteners and any other helpers
__contact__ = "syslog@laposte.net"# current contact adress for more info about this file



###  import concerned modules

#import babel # specialized in localization, format dates according to each country, [available in Debian repo]

#import locale #(builtin module) opens access to the POSIX locale database and functionality. allows to deal with certain cultural issues in an application,

import gettext #(builtin module) provides internationalization and localization, (with the use of po/mo traductions files)
### i dont like to use _() shortcut, i prefer the more explicite gettext()


#import os 


def check(domain,directory=None):
	### shows the environment variables used to select the translation language
	#print(os.environ["LANGUAGE"],os.environ["LANG"])#
	#print(os.environ["LC_ALL"],os.environ["LC_MESSAGES"]) # not present in my env variables
		
	### search .mo file that can be use
	### If languages is not given, then search is made for the following environment variables :
	###	LANGUAGE, LC_ALL, LC_MESSAGES, LANG
	### (The first one find will be use)
	### directory is the place where to search for specified domain 
	### if directory=None then default '/usr/share/locale' will be use on linux
	if gettext.find(domain=domain,localedir=directory) : # return None or the pathname where domain is found
		return True
	else :
		return False
	
def setup(domain,directory=None):
	"""define at once the translation system for all program modules."""
	
	### The bindtextdomain function can be used several times. 
	### if the domainname argument is different the previously bound domains will not be overwritten.
	### if directory=None then default '/usr/share/locale' will be use on linux
	gettext.bindtextdomain(domain=domain,localedir=directory)
	
	### select the domain.mo file to use for the next translations
	gettext.textdomain(domain)



def get(text):
	return gettext.gettext(text)
	
def nget(singular, plural, quantum):
	return gettext.ngettext(singular, plural, quantum)

