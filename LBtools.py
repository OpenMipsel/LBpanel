# LBPanel -- Linux-Box Panel.                             
# Copyright (C) www.linux-box.es
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of   
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU gv; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
# 
# Author: lucifer
#         iqas
#
# Internet: www.linux-box.es
# Based on original source by epanel for openpli 
# Swap code based on original alibabu

from Screens.Screen import Screen
from Screens.Standby import TryQuitMainloop
from Screens.MessageBox import MessageBox
from Screens.InputBox import InputBox
from Components.Sources.StaticText import StaticText
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigClock, ConfigSelection, ConfigSubsection, ConfigYesNo,  config, configfile
from Components.ConfigList import ConfigListScreen
from Components.Harddisk import harddiskmanager
from Components.Pixmap import Pixmap
from Components.Sources.List import List
from Components.Input import Input
from Tools.LoadPixmap import LoadPixmap
from Screens.Console import Console
from Components.Label import Label
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Tools.Directories import fileExists
from Plugins.Plugin import PluginDescriptor
from Components.Language import language
from Components.ScrollLabel import ScrollLabel
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigSelection, ConfigSubsection, ConfigYesNo
from Components.ConfigList import ConfigListScreen
from time import *
from enigma import eEPGCache
from types import *
from enigma import *
import sys, traceback
import re
import new
import _enigma
import time
import datetime
from os import environ
import os
import gettext
import MountManager
import RestartNetwork

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("messages", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/LBpanel/locale/"))

def mountp():
	pathmp = []
	if fileExists("/proc/mounts"):
		for line in open("/proc/mounts"):
			if line.find("/dev/sd") > -1:
				pathmp.append(line.split()[1].replace('\\040', ' ') + "/")
	pathmp.append("/usr/share/enigma2/")
	return pathmp

def _(txt):
	t = gettext.dgettext("messages", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t
######################################################################################
config.plugins.epanel = ConfigSubsection()
config.plugins.epanel.scriptpath = ConfigSelection(default = "/usr/CamEmu/script/", choices = [
		("/usr/CamEmu/script/", _("/usr/CamEmu/script/")),
		("/media/hdd/script/", _("/media/hdd/script/")),
		("/media/usb/script/", _("/media/usb/script/")),
])
config.plugins.epanel.scriptpath1 = ConfigSelection(default = "/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/script/libmem/", choices = [
		("/usr/script/", _("/usr/script/")),
		("/media/hdd/script/", _("/media/hdd/script/")),
		("/media/usb/script/", _("/media/usb/script/")),
])
config.plugins.epanel.direct = ConfigSelection(default = "/media/hdd/", choices = [
		("/media/hdd/", _("/media/hdd/")),
		("/media/usb/", _("/media/usb/")),
		("/usr/share/enigma2/", _("/usr/share/enigma2/")),
		("/media/cf/", _("/media/cf/")),
])
config.plugins.epanel.auto = ConfigSelection(default = "no", choices = [
		("no", _("no")),
		("yes", _("yes")),
		])
config.plugins.epanel.lang = ConfigSelection(default = "es", choices = [
		("es", _("spain d+")),
		])
config.plugins.epanel.epgtime = ConfigClock(default = ((16*60) + 15) * 60) # 18:15
#config.plugins.epanel.weekday = ConfigSelection(default = "01", choices = [
#		("00", _("Mo")),
#		("01", _("Tu")),
#		("02", _("We")),
#		("03", _("Th")),
#		("04", _("Fr")),
#		("05", _("Sa")),
#		("06", _("Su")),
#		])
######################################################################
config.plugins.epanel.min = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("5", "5"),
		("10", "10"),
		("15", "15"),
		("20", "20"),
		("25", "25"),
		("30", "30"),
		("35", "35"),
		("40", "40"),
		("45", "45"),
		("50", "50"),
		("55", "55"),
		])
config.plugins.epanel.hour = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("0", "0"),
		("1", "1"),
		("2", "2"),
		("3", "3"),
		("4", "4"),
		("5", "5"),
		("6", "6"),
		("7", "7"),
		("8", "8"),
		("9", "9"),
		("10", "10"),
		("11", "11"),
		("12", "12"),
		("13", "13"),
		("14", "14"),
		("15", "15"),
		("16", "16"),
		("17", "17"),
		("18", "18"),
		("19", "19"),
		("20", "20"),
		("21", "21"),
		("22", "22"),
		("23", "23"),
		])
config.plugins.epanel.dayofmonth = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("1", "1"),
		("2", "2"),
		("3", "3"),
		("4", "4"),
		("5", "5"),
		("6", "6"),
		("7", "7"),
		("8", "8"),
		("9", "9"),
		("10", "10"),
		("11", "11"),
		("12", "12"),
		("13", "13"),
		("14", "14"),
		("15", "15"),
		("16", "16"),
		("17", "17"),
		("18", "18"),
		("19", "19"),
		("20", "20"),
		("21", "21"),
		("22", "22"),
		("23", "23"),
		("24", "24"),
		("25", "25"),
		("26", "26"),
		("27", "27"),
		("28", "28"),
		("29", "29"),
		("30", "30"),
		("31", "31"),
		])
config.plugins.epanel.month = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("1", _("Jan.")),
		("2", _("Feb.")),
		("3", _("Mar.")),
		("4", _("Apr.")),
		("5", _("May")),
		("6", _("Jun.")),
		("7", _("Jul")),
		("8", _("Aug.")),
		("9", _("Sep.")),
		("10", _("Oct.")),
		("11", _("Nov.")),
		("12", _("Dec.")),
		])
config.plugins.epanel.dayofweek = ConfigSelection(default = "*", choices = [
		("*", "*"),
		("0", _("Su")),
		("1", _("Mo")),
		("2", _("Tu")),
		("3", _("We")),
		("4", _("Th")),
		("5", _("Fr")),
		("6", _("Sa")),
		])
config.plugins.epanel.command = ConfigText(default="/usr/bin/", visible_width = 70, fixed_size = False)
config.plugins.epanel.every = ConfigSelection(default = "0", choices = [
		("0", _("No")),
		("1", _("Min")),
		("2", _("Hour")),
		("3", _("Day of month")),
		("4", _("Month")),
		("5", _("Day of week")),
		])
######################################################################################
config.plugins.epanel.manual = ConfigSelection(default = "0", choices = [
		("0", _("Auto")),
		("1", _("Manual")),
		])
config.plugins.epanel.manualserver = ConfigText(default="ntp.ubuntu.com", visible_width = 70, fixed_size = False)
config.plugins.epanel.server = ConfigSelection(default = "es.pool.ntp.org", choices = [
		("ao.pool.ntp.org",_("Angola")),
		("mg.pool.ntp.org",_("Madagascar")),
		("za.pool.ntp.org",_("South Africa")),
		("tz.pool.ntp.org",_("Tanzania")),
		("bd.pool.ntp.org",_("Bangladesh")),
		("cn.pool.ntp.org",_("China")),
		("hk.pool.ntp.org",_("Hong Kong")),
		("in.pool.ntp.org",_("India")),
		("id.pool.ntp.org",_("Indonesia")),
		("ir.pool.ntp.org",_("Iran")),
		("jp.pool.ntp.org",_("Japan")),
		("kz.pool.ntp.org",_("Kazakhstan")),
		("kr.pool.ntp.org",_("Korea")),
		("my.pool.ntp.org",_("Malaysia")),
		("pk.pool.ntp.org",_("Pakistan")),
		("ph.pool.ntp.org",_("Philippines")),
		("sg.pool.ntp.org",_("Singapore")),
		("tw.pool.ntp.org",_("Taiwan")),
		("th.pool.ntp.org",_("Thailand")),
		("tr.pool.ntp.org",_("Turkey")),
		("ae.pool.ntp.org",_("United Arab Emirates")),
		("uz.pool.ntp.org",_("Uzbekistan")),
		("vn.pool.ntp.org",_("Vietnam")),
		("at.pool.ntp.org",_("Austria")),
		("by.pool.ntp.org",_("Belarus")),
		("be.pool.ntp.org",_("Belgium")),
		("bg.pool.ntp.org",_("Bulgaria")),
		("cz.pool.ntp.org",_("Czech Republic")),
		("dk.pool.ntp.org",_("Denmark")),
		("ee.pool.ntp.org",_("Estonia")),
		("fi.pool.ntp.org",_("Finland")),
		("fr.pool.ntp.org",_("France")),
		("de.pool.ntp.org",_("Germany")),
		("gr.pool.ntp.org",_("Greece")),
		("hu.pool.ntp.org",_("Hungary")),
		("ie.pool.ntp.org",_("Ireland")),
		("it.pool.ntp.org",_("Italy")),
		("lv.pool.ntp.org",_("Latvia")),
		("lt.pool.ntp.org",_("Lithuania")),
		("lu.pool.ntp.org",_("Luxembourg")),
		("mk.pool.ntp.org",_("Macedonia")),
		("md.pool.ntp.org",_("Moldova")),
		("nl.pool.ntp.org",_("Netherlands")),
		("no.pool.ntp.org",_("Norway")),
		("pl.pool.ntp.org",_("Poland")),
		("pt.pool.ntp.org",_("Portugal")),
		("ro.pool.ntp.org",_("Romania")),
		("ru.pool.ntp.org",_("Russian Federation")),
		("sk.pool.ntp.org",_("Slovakia")),
		("si.pool.ntp.org",_("Slovenia")),
		("es.pool.ntp.org",_("Spain")),
		("se.pool.ntp.org",_("Sweden")),
		("ch.pool.ntp.org",_("Switzerland")),
		("ua.pool.ntp.org",_("Ukraine")),
		("uk.pool.ntp.org",_("United Kingdom")),
		("bs.pool.ntp.org",_("Bahamas")),
		("ca.pool.ntp.org",_("Canada")),
		("gt.pool.ntp.org",_("Guatemala")),
		("mx.pool.ntp.org",_("Mexico")),
		("pa.pool.ntp.org",_("Panama")),
		("us.pool.ntp.org",_("United States")),
		("au.pool.ntp.org",_("Australia")),
		("nz.pool.ntp.org",_("New Zealand")),
		("ar.pool.ntp.org",_("Argentina")),
		("br.pool.ntp.org",_("Brazil")),
		("cl.pool.ntp.org",_("Chile")),
		])
config.plugins.epanel.onoff = ConfigSelection(default = "0", choices = [
		("0", _("No")),
		("1", _("Yes")),
		])
config.plugins.epanel.time = ConfigSelection(default = "30", choices = [
		("30", _("30 min")),
		("1", _("60 min")),
		("2", _("120 min")),
		("3", _("180 min")),
		("4", _("240 min")),
		])
config.plugins.epanel.TransponderTime = ConfigSelection(default = "0", choices = [
		("0", _("Off")),
		("1", _("On")),
		])
config.plugins.epanel.cold = ConfigSelection(default = "0", choices = [
		("0", _("No")),
		("1", _("Yes")),
		])
config.plugins.epanel.autosave = ConfigSelection(default = '0', choices = [
		('0', _("Off")),
		('29', _("30 min")),
		('59', _("60 min")),
		('119', _("120 min")),
		('179', _("180 min")),
		('239', _("240 min")),
		])
config.plugins.epanel.autobackup = ConfigYesNo(default = False)
######################################################################################
## lbscan section
config.plugins.epanel.checkauto = ConfigSelection(default = "no", choices = [
               ("yes", _("Yes")),
               ("no", _("No")), 
])
config.plugins.epanel.autocheck = ConfigSelection(default = "yes", choices = [
               ("yes", _("Yes")),   
               ("no", _("No")),    
 ])

config.plugins.epanel.checktype = ConfigSelection(default = "fast", choices = [
               ("fast", _("Fast")),   
               ("full", _("Full")),    
               ])
                              
config.plugins.epanel.checkhour = ConfigClock(default = ((18*60) + 30) * 60) # 20:30

config.plugins.epanel.checkoff = ConfigSelection(default = "yes", choices = [
               ("yes", _("Yes")),
               ("no", _("No")), 
])
config.plugins.epanel.lbemail = ConfigYesNo(default = False)
config.plugins.epanel.warnonlyemail = ConfigSelection(default = "yes", choices = [
               ("yes", _("Yes")),   
               ("no", _("No")), 
])                              
config.plugins.epanel.lbemailto = ConfigText(default = "correo@gmail.com",fixed_size = False, visible_width=30) 
config.plugins.epanel.smtpserver = ConfigText(default = "smtp.gmail.com:587",fixed_size = False, visible_width=30)
config.plugins.epanel.smtpuser = ConfigText(default = "yo@gmail.com",fixed_size = False, visible_width=30)
config.plugins.epanel.smtppass = ConfigPassword(default = "mailpass",fixed_size = False, visible_width=15)

#####################################################################################

class ToolsScreen(Screen):
	skin = """
		<screen name="ToolsScreen" position="70,35" size="1150,650" title="PANEL SERVICIOS">
		<ePixmap position="700,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo7.png" alphatest="blend" transparent="1" />
	<ePixmap position="705, 640" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="705, 610" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_green" render="Label" position="875, 610" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="885, 640" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />

	<widget source="menu" render="Listbox" position="15,10" size="660,630" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (200, 25), size = (600, 65), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (210, 75), size = (600, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (7, 7), size = (115, 115), png = 3), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 30),gFont("Regular", 16)],
	"itemHeight": 125
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("PANEL SERVICIOS"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"ok": self.keyOK,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.GreenKey,
		})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("HDD sleep"))
		self.list = []
		self["menu"] = List(self.list)
		self.mList()

	def mList(self):
		self.list = []
		onepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/crash.png"))
		twopng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/info2.png"))
		treepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/epg.png"))
		fivepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/script.png"))
		sixpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/ntp.png"))
		sevenpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/libmemoria.png"))
		dospng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/net1.png"))
		eightpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/scan.png"))
		self.list.append((_("Tools Crashlog"),"com_one", _("ver y borrar crashlog archivos"), onepng ))
		self.list.append((_("Info Sistema"),"com_two", _("Ver info sistema (free, dh -f)"), twopng ))
		self.list.append((_("EPG Descarga D+"),"com_tree", _("Descarga EPG D+"), treepng ))
		self.list.append((_("Scan Peer Security"),"com_scan", _("Check host security"), eightpng ))
		self.list.append((_("Sincronizacion NTP"),"com_six", _("Sincronizacion ntp 30 min,60 min,120 min, 240"), sixpng ))
		self.list.append((_("Scripts Usuario"),"com_five", _("Scripts Usuario"), fivepng ))
		self.list.append((_("Liberar memoria"),"com_seven", _("Lanzador liberar memoria"), sevenpng ))
		self.list.append((_("Network"),"com_dos", _("Reiniciar Red"), dospng ))
		self["menu"].setList(self.list)

	def exit(self):
		self.close()
		
	def GreenKey(self):
		ishdd = open("/proc/mounts", "r")
		for line in ishdd:
			if line.find("/media/hdd") > -1:
				mountpointname = line.split()
				os.system("hdparm -y %s" % (mountpointname[0]))
				self.mbox = self.session.open(MessageBox,_("HDD go sleep"), MessageBox.TYPE_INFO, timeout = 4 )

	def keyOK(self, returnValue = None):
		if returnValue == None:
			returnValue = self["menu"].getCurrent()[1]
			if returnValue is "com_one":
				self.session.openWithCallback(self.mList,CrashLogScreen)
			elif returnValue is "com_two":
				self.session.openWithCallback(self.mList,Info2Screen)
			elif returnValue is "com_tree":
				self.session.open(epgdn)
			elif returnValue is "com_five":
				self.session.openWithCallback(self.mList, ScriptScreen)
			elif returnValue is "com_six":
				self.session.openWithCallback(self.mList, NTPScreen)
			elif returnValue is "com_seven":
				self.session.openWithCallback(self.mList,Libermen)
			elif returnValue is "com_dos":
				self.session.open(RestartNetwork.RestartNetwork)
			elif returnValue is "com_scan":
                                self.session.open(scanhost)
			else:
				print "\n[BackupSuite] cancel\n"
				self.close(None)
###############################################################################
class SwapScreen2(Screen):
	skin = """
		<screen name="SwapScreen2" position="center,160" size="1150,500" title="SWAP MANAGER">
				  #<ePixmap position="700,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo17.png" alphatest="blend" transparent="1" />
	<ePixmap position="20,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="20,20" size="660,450" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("SWAP MANAGER"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"ok": self.Menu,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
		})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.Menu()
		
	def Menu(self):
		self.list = []
		minispng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/swapmini.png"))
		minisonpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/swapminion.png"))
		for line in mountp():
			if line not in "/usr/share/enigma2/":
				try:
					if self.swapiswork() in line:
						self.list.append((_("Manage Swap on %s") % line, _("Start, Stop, Create, Remove Swap file"), minisonpng, line))
					else:
						self.list.append((_("Manage Swap on %s") % line, _("Start, Stop, Create, Remove Swap file"), minispng, line))
				except:
					self.list.append((_("Manage Swap on %s") % line, _("Start, Stop, Create, Remove Swap file"), minispng, line))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.MenuDo, "cancel": self.close}, -1)
		
	def swapiswork(self):
		if fileExists("/proc/swaps"):
			for line in open("/proc/swaps"):
				if line.find("media") > -1:
					return line.split()[0][:-9]
		else:
			return " "
		
	def MenuDo(self):
		swppath = self["menu"].getCurrent()[3] + "swapfile"
		self.session.openWithCallback(self.Menu,SwapScreen, swppath)
	
	def exit(self):
		self.close()
####################################################################
class SwapScreen(Screen):
	skin = """
		<screen name="SwapScreen" position="center,160" size="1150,500" title="SWAP MANAGER">
		  #<ePixmap position="700,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo17.png" alphatest="blend" transparent="1" />
	<ePixmap position="20,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="20,20" size="660,450" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 3), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session, swapdirect):
		self.swapfile = swapdirect
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("SWAP MANAGER"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"ok": self.CfgMenuDo,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
		})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()

	def isSwapPossible(self):
		for line in open("/proc/mounts"):
			fields= line.rstrip('\n').split()
			if fields[1] == "%s" % self.swapfile[:-9]:
				if fields[2] == 'ext2' or fields[2] == 'ext3' or fields[2] == 'ext4' or fields[2] == 'vfat':
					return 1
				else:
					return 0
		return 0
		
	def isSwapRun(self):
		try:
			for line in open('/proc/swaps'):
				if line.find(self.swapfile) > -1:
					return 1
			return 0
		except:
			pass
			
	def isSwapSize(self):
		try:
			swapsize = os.path.getsize(self.swapfile) / 1048576
			return ("%sMb" % swapsize)
		except:
			pass
			
	def makeSwapFile(self, size):
		try:
			os.system("dd if=/dev/zero of=%s bs=1024 count=%s" % (self.swapfile, size))
			os.system("mkswap %s" % (self.swapfile))
			self.mbox = self.session.open(MessageBox,_("Swap file created"), MessageBox.TYPE_INFO, timeout = 4 )
			self.CfgMenu()
		except:
			pass
	
	def CfgMenu(self):
		self.list = []
		minispng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/swapmini.png"))
		minisonpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/swapminion.png"))
		if self.isSwapPossible():
			if os.path.exists(self.swapfile):
				if self.isSwapRun() == 1:
					self.list.append((_("Swap off"),"5", (_("Swap on %s off (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minisonpng))
				else:
					self.list.append((_("Swap on"),"4", (_("Swap on %s on (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minispng))
					self.list.append((_("Remove swap"),"7",( _("Remove swap on %s (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minispng))
			else:
				self.list.append((_("Make swap"),"11", _("Make swap on %s (128MB)") % self.swapfile[7:10].upper(), minispng))
				self.list.append((_("Make swap"),"12", _("Make swap on %s (256MB)") % self.swapfile[7:10].upper(), minispng))
				self.list.append((_("Make swap"),"13", _("Make swap on %s (512MB)") % self.swapfile[7:10].upper(), minispng))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.CfgMenuDo, "cancel": self.close}, -1)
			
	def CfgMenuDo(self):
		m_choice = self["menu"].getCurrent()[1]
		if m_choice is "4":
			try:
				for line in open("/proc/swaps"):
					if  line.find("swapfile") > -1:
						os.system("swapoff %s" % (line.split()[0]))
			except:
				pass
			os.system("swapon %s" % (self.swapfile))
			os.system("sed -i '/swap/d' /etc/fstab")
			os.system("echo -e '%s/swapfile swap swap defaults 0 0' >> /etc/fstab" % self.swapfile[:10])
			self.mbox = self.session.open(MessageBox,_("Swap file started"), MessageBox.TYPE_INFO, timeout = 4 )
			self.CfgMenu()
		elif m_choice is "5":
			os.system("swapoff %s" % (self.swapfile))
			os.system("sed -i '/swap/d' /etc/fstab")
			self.mbox = self.session.open(MessageBox,_("Swap file stoped"), MessageBox.TYPE_INFO, timeout = 4 )
			self.CfgMenu()
		elif m_choice is "11":
			self.makeSwapFile("131072")

		elif m_choice is "12":
			self.makeSwapFile("262144")

		elif m_choice is "13":
			self.makeSwapFile("524288")

		elif m_choice is "7":
			os.system("rm %s" % (self.swapfile))
			self.mbox = self.session.open(MessageBox,_("Swap file removed"), MessageBox.TYPE_INFO, timeout = 4 )
			self.CfgMenu()
			
	def exit(self):
		self.close()
####################################################################
class UsbScreen(Screen):
	skin = """
<screen name="UsbScreen" position="center,160" size="1150,500" title="Unmount manager">
  #<ePixmap position="700,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo18.png" alphatest="blend" transparent="1" />
	<ePixmap position="20,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_green" render="Label" position="190,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_yellow" render="Label" position="360,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
	<ePixmap position="360,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
	<widget source="menu" render="Listbox" position="20,20" size="660,450" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (100, 60), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 70
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("Unmount manager"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.Ok,
			"yellow": self.CfgMenu,
			})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("UnMount"))
		self["key_yellow"] = StaticText(_("reFresh"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def CfgMenu(self):
		self.list = []
		minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/usbico.png"))
		hddlist = harddiskmanager.HDDList()
		hddinfo = ""
		if hddlist:
			for count in range(len(hddlist)):
				hdd = hddlist[count][1]
				devpnt = self.devpoint(hdd.mountDevice())
				if hdd.mountDevice() != '/media/hdd':
					if devpnt != None:
						if int(hdd.free()) > 1024:
							self.list.append(("%s" % hdd.model(),"%s  %s  %s (%d.%03d GB free)" % (devpnt, self.filesystem(hdd.mountDevice()),hdd.capacity(), hdd.free()/1024 , hdd.free()%1024 ), minipng, devpnt))
						else:
							self.list.append(("%s" % hdd.model(),"%s  %s  %s (%03d MB free)" % (devpnt, self.filesystem(hdd.mountDevice()), hdd.capacity(),hdd.free()), minipng, devpnt))
		else:
			hddinfo = _("none")
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], { "cancel": self.close}, -1)
		
	def Ok(self):
		try:
			item = self["menu"].getCurrent()[3]
			os.system("umount -f %s" % item)
			self.mbox = self.session.open(MessageBox,_("Unmounted %s" % item), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			pass
		self.CfgMenu()
		
	def filesystem(self, mountpoint):
		try:
			for line in open("/proc/mounts"):
				if line.find(mountpoint)  > -1:
					return "%s  %s" % (line.split()[2], line.split()[3].split(',')[0])
		except:
			pass
			
	def devpoint(self, mountpoint):
		try:
			for line in open("/proc/mounts"):
				if line.find(mountpoint)  > -1:
					return line.split()[0]
		except:
			pass
			
	def exit(self):
		self.close()
		
####################################################################
class ScriptScreen(Screen):
	skin = """
	<screen name="ScriptScreen" position="center,160" size="1150,500" title="Script Usuario" >
	    <ePixmap position="710,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo11.png" alphatest="blend" transparent="1" />
		<widget name="list" position="20,10" size="660,450" scrollbarMode="showOnDemand" />
		<ePixmap position="20,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
		<widget source="key_red" render="Label" position="20,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="190,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
		<widget source="key_green" render="Label" position="190,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.setTitle(_("Script Usuario"))
		self.scrpit_menu()
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Config"))
		self["actions"] = ActionMap(["OkCancelActions","ColorActions"], {"ok": self.run, "red": self.exit, "green": self.config_path, "cancel": self.close}, -1)
		
	def scrpit_menu(self):
		list = []
		try:
			list = os.listdir("%s" % config.plugins.epanel.scriptpath.value[:-1])
			list = [x[:-3] for x in list if x.endswith('.sh')]
		except:
			list = []
		list.sort()
		self["list"] = MenuList(list)
		
	def run(self):
		script = self["list"].getCurrent()
		if script is not None:
			name = ("%s%s.sh" % (config.plugins.epanel.scriptpath.value, script))
			os.chmod(name, 0755)
			self.session.open(Console, script.replace("_", " "), cmdlist=[name])
			
	def config_path(self):
		self.session.open(ConfigScript)

	def exit(self):
		self.close()
########################################################################
class ConfigScript(ConfigListScreen, Screen):
	skin = """
<screen name="ConfigScript" position="center,160" size="750,370" title="Config script Executer">
		<widget position="15,10" size="720,300" name="config" scrollbarMode="showOnDemand" />
		<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
		<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
		<widget source="key_green" render="Label" position="190,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("Config script Executer"))
		self.list = []
		self.list.append(getConfigListEntry(_("Set script path"), config.plugins.epanel.scriptpath))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"ok": self.save
		}, -2)
		
	def cancel(self):
		self.close()
		
	def save(self):
		if not os.path.exists(config.plugins.epanel.scriptpath.value):
			try:
				os.system("mkdir %s" % config.plugins.epanel.scriptpath.value)
			except:
				pass
		config.plugins.epanel.scriptpath.save()
		configfile.save()
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )
########################################################################
class NTPScreen(ConfigListScreen, Screen):
	skin = """
<screen name="NTPScreen" position="center,160" size="1150,500" title="SINCRONIZACION NTP">
    #<ePixmap position="720,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo14.png" alphatest="blend" transparent="1" />
		<widget position="15,10" size="690,450" name="config" scrollbarMode="showOnDemand" />
		<ePixmap position="10,488" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
		<widget source="key_red" render="Label" position="10,458" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="175,488" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
		<widget source="key_green" render="Label" position="175,458" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="340,488" zPosition="1" size="195,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
		<widget source="key_yellow" render="Label" position="340,458" zPosition="2" size="195,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="535,488" zPosition="1" size="195,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/blue.png" alphatest="blend" />
		<widget source="key_blue" render="Label" position="535,458" zPosition="2" size="195,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("SINCRONIZACION NTP"))
		self.cfgMenu()
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText(_("Update Now"))
		self["key_blue"] = StaticText(_("Manual"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "EPGSelectActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"yellow": self.UpdateNow,
			"blue": self.Manual,
			"ok": self.save
		}, -2)
		
	def cfgMenu(self):
		self.list = []
		self.list.append(getConfigListEntry(_("Actualizar NTP"), config.plugins.epanel.onoff))
		self.list.append(getConfigListEntry(_("Ajustar Hora Actualizacion"), config.plugins.epanel.time))
		self.list.append(getConfigListEntry(_("Ajustar Hora Transpondedor"), config.plugins.epanel.TransponderTime))
		self.list.append(getConfigListEntry(_("Sincronizacion en arranque"), config.plugins.epanel.cold))
		self.list.append(getConfigListEntry(_("Modo Servidor"), config.plugins.epanel.manual))
		self.list.append(getConfigListEntry(_("Seleccionar zona horaria"), config.plugins.epanel.server))
		self.list.append(getConfigListEntry(_("Elejir Servidor ntp"), config.plugins.epanel.manualserver))
		ConfigListScreen.__init__(self, self.list)
		
	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close()
		
	def Manual(self):
		ManualSetTime(self.session)
	
	def save(self):
		path = "/etc/cron/crontabs/root"
		if config.plugins.epanel.onoff.value == "0":
			if fileExists(path):
				os.system("sed -i '/ntp./d' %s" % path)
		if config.plugins.epanel.onoff.value == "1":
			if fileExists(path):
				os.system("sed -i '/ntp./d' %s" % path)
			if config.plugins.epanel.manual.value == "0":
				if config.plugins.epanel.time.value == "30":
					os.system("echo -e '/%s * * * * /usr/bin/ntpdate -s -u %s' >> %s" % (config.plugins.epanel.time.value, config.plugins.epanel.server.value, path))
				else:
					os.system("echo -e '* /%s * * * /usr/bin/ntpdate -s -u %s' >> %s" % (config.plugins.epanel.time.value, config.plugins.epanel.server.value, path))
			else:
				if config.plugins.epanel.time.value == "30":
					os.system("echo -e '/%s * * * * /usr/bin/ntpdate -s -u %s' >> %s" % (config.plugins.epanel.time.value, config.plugins.epanel.manualserver.value, path))
				else:
					os.system("echo -e '* /%s * * * /usr/bin/ntpdate -s -u %s' >> %s" % (config.plugins.epanel.time.value, config.plugins.epanel.manualserver.value, path))
		os.system("echo -e 'root' >> /etc/cron/crontabs/cron.update")
		if fileExists(path):
			os.chmod("%s" % path, 0644)
		if config.plugins.epanel.TransponderTime.value == "0": 
			config.misc.useTransponderTime.value = False
			config.misc.useTransponderTime.save()
		else:
			config.misc.useTransponderTime.value = True
			config.misc.useTransponderTime.save()
		if config.plugins.epanel.cold.value == "0":
			if fileExists("/etc/rcS.d/S42ntpdate.sh"):
				os.unlink("/etc/rcS.d/S42ntpdate.sh")
		else:
			os.system("tar -C/ -xzpvf /usr/lib/enigma2/python/Plugins/Extensions/LBpanel/ntpdate.tar.gz")
			if fileExists("/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/ntpdate.sh"):
				if config.plugins.epanel.manual.value == "0":
					os.system("sed -i 's/ntp_server/%s/g' /usr/lib/enigma2/python/Plugins/Extensions/LBpanel/ntpdate.sh" % config.plugins.epanel.server.value)
				else:
					os.system("sed -i 's/ntp_server/%s/g' /usr/lib/enigma2/python/Plugins/Extensions/LBpanel/ntpdate.sh" % config.plugins.epanel.manualserver.value)
			if not fileExists("/etc/rcS.d/S42ntpdate.sh"):
				os.symlink("/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/ntpdate.sh", "/etc/rcS.d/S42ntpdate.sh")
				os.chmod("/etc/rcS.d/S42ntpdate.sh", 0777)
		for i in self["config"].list:
			i[1].save()
		configfile.save()
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )
			
	def UpdateNow(self):
		list =""
		synkinfo = os.popen("/usr/bin/ntpdate -v -u pool.ntp.org")
		for line in synkinfo:
			list += line
		self.mbox = self.session.open(MessageBox,list, MessageBox.TYPE_INFO, timeout = 6 )
####################################################################
class ManualSetTime(Screen):
	def __init__(self, session):
		self.session = session
		self.currentime = strftime("%d:%m:%Y %H:%M",localtime())
		self.session.openWithCallback(self.newTime,InputBox, text="%s" % (self.currentime), maxSize=16, type=Input.NUMBER)

	def newTime(self,what):
		try:
			lenstr=len(what)
		except:
			lengstr = 0
		if what is None:
			self.breakSetTime(_("new time not available"))
		elif ((what.count(" ") < 1) or (what.count(":") < 3) or (lenstr != 16)):
			self.breakSetTime(_("bad format"))
		else:
			newdate = what.split(" ",1)[0]
			newtime = what.split(" ",1)[1]
			newday = newdate.split(":",2)[0]
			newmonth = newdate.split(":",2)[1]
			newyear = newdate.split(":",2)[2]
			newhour = newtime.split(":",1)[0]
			newmin = newtime.split(":",1)[1]
			maxmonth = 31
			if (int(newmonth) == 4) or (int(newmonth) == 6) or (int(newmonth) == 9) or (int(newmonth) == 11):
				maxmonth=30
			elif (int(newmonth) == 2):
				if ((4*int(int(newyear)/4)) == int(newyear)):
					maxmonth=28
				else:
					maxmonth=27
			if (int(newyear) < 2007) or (int(newyear) > 2027)  or (len(newyear) < 4):
				self.breakSetTime(_("bad year %s") %newyear)
			elif (int(newmonth) < 0) or (int(newmonth) >12) or (len(newmonth) < 2):
				self.breakSetTime(_("bad month %s") %newmonth)
			elif (int(newday) < 1) or (int(newday) > maxmonth) or (len(newday) < 2):
				self.breakSetTime(_("bad day %s") %newday)
			elif (int(newhour) < 0) or (int(newhour) > 23) or (len(newhour) < 2):
				self.breakSetTime(_("bad hour %s") %newhour)
			elif (int(newmin) < 0) or (int(newmin) > 59) or (len(newmin) < 2):
				self.breakSetTime(_("bad minute %s") %newmin)
			else:
				self.newtime = "%s%s%s%s%s" %(newmonth,newday,newhour,newmin,newyear)
				self.session.openWithCallback(self.ChangeTime,MessageBox,_("Apply the new System time?"), MessageBox.TYPE_YESNO)

	def ChangeTime(self,what):
		if what is True:
			os.system("date %s" % (self.newtime))
		else:
			self.breakSetTime(_("not confirmed"))

	def breakSetTime(self,reason):
		self.session.open(MessageBox,(_("Change system time was canceled, because %s") % reason), MessageBox.TYPE_WARNING)

####################################################################
class SystemScreen(Screen):
	skin = """
		<screen name="SystemScreen" position="70,35" size="1150,650" title="Panel Sistema">
	<ePixmap position="700,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo13.png" alphatest="blend" transparent="1" />
	<ePixmap position="705, 640" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="705, 610" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="15,10" size="660,630" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (200, 25), size = (600, 65), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (210, 75), size = (600, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (7, 7), size = (115, 115), png = 3), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 30),gFont("Regular", 16)],
	"itemHeight": 125
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("Panel Sistema"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"ok": self.keyOK,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
		})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.mList()

	def mList(self):
		self.list = []
		onepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/kernel.png"))
		fourpng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/swap.png"))
		fivepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/cron.png"))
		seispng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/disco.png"))
		treepng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/unusb.png"))
		self.list.append((_("Manager Kernel Modulo"),"1", _("load & unload Modulos Kernel"), onepng))
		self.list.append((_("Cron Manager"),"5", _("Activar tareas programadas"), fivepng))
		self.list.append((_("Mount Manager"),"6", _("Manager Disco Duro"), seispng))
		self.list.append((_("Swap Manager"),"4", _("Start, Stop, Create, Remove archivos Swap"), fourpng ))
		self.list.append((_("UnMount USB"),"3", _("Unmount usb devices"), treepng ))
		self["menu"].setList(self.list)

	def exit(self):
		self.close()

	def keyOK(self, returnValue = None):
		if returnValue == None:
			returnValue = self["menu"].getCurrent()[1]
			if returnValue is "1":
				self.session.openWithCallback(self.mList,KernelScreen)
			elif returnValue is "3":
				self.session.openWithCallback(self.mList,UsbScreen)
			elif returnValue is "4":
				self.session.openWithCallback(self.mList,SwapScreen2)
			elif returnValue is "5":
				self.session.openWithCallback(self.mList,CrontabMan)
			elif returnValue is "6":
				self.session.open(MountManager.HddMount)
			else:
				print "\n[BackupSuite] cancel\n"
				self.close(None)
###############################################################################
class KernelScreen(Screen):
	skin = """
<screen name="KernelScreen" position="center,100" size="1150,500" title="Kernel Modules Manager">
  #<ePixmap position="710,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo15.png" alphatest="blend" transparent="1" />
	<ePixmap position="20,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_green" render="Label" position="185,458" zPosition="2" size="210,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,488" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
	<ePixmap position="390,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" transparent="1" alphatest="on" />
	<widget source="key_yellow" render="Label" position="390,458" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="key_blue" render="Label" position="560,458" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<ePixmap position="560,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/blue.png" transparent="1" alphatest="on" />
	<widget source="menu" render="Listbox" position="20,10" size="660,450" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (51, 40), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("Manager Kernel Modulo"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.Ok,
			"yellow": self.YellowKey,
			"blue": self.BlueKey,
		})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Load/UnLoad"))
		self["key_yellow"] = StaticText(_("LsMod"))
		self["key_blue"] = StaticText(_("Reboot"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def BlueKey(self):
		os.system("reboot")
		
	def YellowKey(self):
		self.session.openWithCallback(self.CfgMenu,lsmodScreen)
		
	def IsRunnigModDig(self, what):
		modrun = os.popen ("lsmod | grep %s" % (what[:-4]))
		for line in modrun:
			if line.find(what[:-4]) > -1:
				return 1
				break
		return 0
		
	def CfgMenu(self):
		self.list = []
		DvrName = os.popen("modprobe -l -t drivers")
		for line in DvrName:
			kernDrv = line.split("/")
			if self.IsRunnigModDig(kernDrv[-1]) == 1:
				minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/kernelminimem.png"))
				self.list.append((kernDrv[-1],line,minipng, "1"))
			else:
				minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/kernelmini.png"))
				self.list.append((kernDrv[-1],line,minipng, "0"))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.Ok, "cancel": self.close}, -1)

	def Ok(self):
		item = self["menu"].getCurrent()
		isrunning = item[3]
		nlist = item[0]
		if item[3] == "0":
			os.system(("modprobe %s" % (nlist[:-4])))
			os.system(("echo %s>/etc/modutils/%s" % (nlist[:-4],nlist[:-4])))
			os.chmod(("/etc/modutils/%s" % (nlist[:-4])), 0644)
			os.system("update-modules")
			self.mbox = self.session.open(MessageBox,(_("Loaded %s") % (nlist)), MessageBox.TYPE_INFO, timeout = 4 )
		else:
			os.system(("rmmod%s" % (" " + nlist[:-4])))
			os.system(("rm /etc/modutils/%s" % (nlist[:-4])))
			os.system("update-modules")
			self.mbox = self.session.open(MessageBox,(_("UnLoaded %s") % (nlist)), MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def exit(self):
		self.close()
####################################################################
class lsmodScreen(Screen):
	skin = """
<screen name="lsmodScreen" position="center,100" size="750,570" title="Kernel Drivers in Memory">
	<ePixmap position="20,558" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,528" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="20,10" size="710,500" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (51, 40), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("Kernel Drivers en Memoria"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def CfgMenu(self):
		self.list = []
		DvrName = os.popen("lsmod")
		minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/kernelminimem.png"))
		for line in DvrName:
			item = line.split(" ")
			size = line[:28].split(" ")
			minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/kernelminimem.png"))
			if line.find("Module") != 0:
				self.list.append((item[0],( _("size: %s  %s") % (size[-1], item[-1])), minipng))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], { "cancel": self.close}, -1)

	def exit(self):
		self.close()
####################################################################
class CrashLogScreen(Screen):
	skin = """
<screen name="CrashLogScreen" position="center,160" size="1150,500" title="Ver archivos crashlog">
    <ePixmap position="715,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo8.png" alphatest="blend" transparent="1" />
	<ePixmap position="20,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<widget source="key_green" render="Label" position="190,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
	<ePixmap position="360,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" transparent="1" alphatest="on" />
	<widget source="key_yellow" render="Label" position="360,458" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="key_blue" render="Label" position="530,458" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<ePixmap position="530,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/blue.png" transparent="1" alphatest="on" />
	<widget source="menu" render="Listbox" position="20,10" size="690,347" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (51, 40), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("Ver archivos Crashlog"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.Ok,
			"yellow": self.YellowKey,
			"blue": self.BlueKey,
			})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("View"))
		self["key_yellow"] = StaticText(_("Remove"))
		self["key_blue"] = StaticText(_("Remove All"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def CfgMenu(self):
		self.list = []
		minipng = LoadPixmap(cached=True, path=resolveFilename(SCOPE_PLUGINS, "Extensions/LBpanel/images/crashmini.png"))
		try:
			crashfiles = os.listdir("/media/hdd")
			for line in crashfiles:
				if line.find("enigma2_crash") > -1:
					self.list.append((line,"%s" % time.ctime(os.path.getctime("/media/hdd/" + line)), minipng))
		except:
			pass
		self.list.sort()
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], { "cancel": self.close}, -1)
		
	def Ok(self):
		try:
			item = "/media/hdd/" + self["menu"].getCurrent()[0]
			self.session.openWithCallback(self.CfgMenu,LogScreen, item)
		except:
			pass
	
	def YellowKey(self):
		item = "/media/hdd/" +  self["menu"].getCurrent()[0]
		try:
			os.system("rm %s"%(item))
			self.mbox = self.session.open(MessageBox,(_("Removed %s") % (item)), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox,(_("Failed remove")), MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def BlueKey(self):
		try:
			os.system("rm /media/hdd/enigma2_crash*.log")
			self.mbox = self.session.open(MessageBox,(_("Removed All Crashlog Files") ), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox,(_("Failed remove")), MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def exit(self):
		self.close()
####################################################################
class LogScreen(Screen):
	skin = """
<screen name="LogScreen" position="center,80" size="1170,600" title="View Crashlog file">
	<ePixmap position="20,590" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,560" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,590" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
	<widget source="key_green" render="Label" position="190,560" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="390,590" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
	<widget source="key_yellow" render="Label" position="390,560" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget name="text" position="10,10" size="1150,542" font="Console;22" />
</screen>"""

	def __init__(self, session, what):
		self.session = session
		Screen.__init__(self, session)
		self.crashfile = what
		self.setTitle(_("View Crashlog file"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.GreenKey,
			"yellow": self.YellowKey,
			})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Restart GUI"))
		self["key_yellow"] = StaticText(_("Save"))
		self["text"] = ScrollLabel("")
		self.listcrah()
		
	def exit(self):
		self.close()
	
	def GreenKey(self):
		self.session.open(TryQuitMainloop, 3)
		
	def YellowKey(self):
		os.system("gzip %s" % (self.crashfile))
		os.system("mv %s.gz /tmp" % (self.crashfile))
		self.mbox = self.session.open(MessageBox,_("%s.gz created in /tmp") % self.crashfile, MessageBox.TYPE_INFO, timeout = 4)
		
	def listcrah(self):
		list = " "
		files = open(self.crashfile, "r")
		for line in files:
			if line.find("Traceback (most recent call last):") != -1:
				for line in files:
					list += line
					if line.find("]]>") != -1:
						break
		self["text"].setText(list)
		files.close()
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions"], { "cancel": self.close, "up": self["text"].pageUp, "left": self["text"].pageUp, "down": self["text"].pageDown, "right": self["text"].pageDown,}, -1)
######################################################################################
class epgdn(ConfigListScreen, Screen):
	skin = """
<screen name="epgdn" position="center,160" size="1150,500" title="EPG D+ LINUX-BOX.ES">
    <ePixmap position="715,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo9.png" alphatest="blend" transparent="1" />
  <widget position="15,10" size="690,450" name="config" scrollbarMode="showOnDemand" />
   <ePixmap position="10,488" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,458" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,488" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,458" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="340,488" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="340,458" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="540,488" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/blue.png" alphatest="blend" />
  <widget source="key_blue" render="Label" position="540,458" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("EPG D+ LINUX-BOX.ES"))
		self.list = []
		self.list.append(getConfigListEntry(_("Seleccione donde guardar epg.dat"), config.plugins.epanel.direct))
		self.list.append(getConfigListEntry(_("Seleccion D+ epg"), config.plugins.epanel.lang))
		self.list.append(getConfigListEntry(_("Activar Autodescarga epg.dat"), config.plugins.epanel.auto))
		self.list.append(getConfigListEntry(_("Hora de autodescarga"), config.plugins.epanel.epgtime))
		self.list.append(getConfigListEntry(_("Guardar y carga EPG automatica"), config.plugins.epanel.autosave))
		self.list.append(getConfigListEntry(_("Guardar copia en ../epgtmp.gz"), config.plugins.epanel.autobackup))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText(_("Descarga EPG"))
		self["key_blue"] = StaticText(_("Manual"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"yellow": self.downepg,
			"blue": self.manual,
			"ok": self.save
		}, -2)
		
	def downepg(self):
		try:
			os.system("wget -q http://www.linux-box.es/epg/epg.dat.gz -O %sepg.dat.gz" % (config.plugins.epanel.direct.value))
			if fileExists("%sepg.dat" % config.plugins.epanel.direct.value):
				os.unlink("%sepg.dat" % config.plugins.epanel.direct.value)
				os.system("rm -f %sepg.dat" % config.plugins.epanel.direct.value)
			if not os.path.exists("%sepgtmp" % config.plugins.epanel.direct.value):
				os.system("mkdir -p %sepgtmp" % config.plugins.epanel.direct.value)
			os.system("cp -f %sepg.dat.gz %sepgtmp" % (config.plugins.epanel.direct.value, config.plugins.epanel.direct.value))
			os.system("gzip -df %sepg.dat.gz" % config.plugins.epanel.direct.value)
			os.chmod("%sepg.dat" % config.plugins.epanel.direct.value, 0644)
			self.mbox = self.session.open(MessageBox,(_("EPG downloaded")), MessageBox.TYPE_INFO, timeout = 4 )
			epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
			epgcache = eEPGCache.getInstance().load()
		except:
			self.mbox = self.session.open(MessageBox,(_("Sorry, the EPG download error")), MessageBox.TYPE_INFO, timeout = 4 )

	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close(False)
	
	def save(self):
		config.misc.epgcache_filename.value = ("%sepg.dat" % config.plugins.epanel.direct.value)
		config.misc.epgcache_filename.save()
		config.plugins.epanel.epgtime.save()
		config.plugins.epanel.lang.save()
		config.plugins.epanel.direct.save()
		config.plugins.epanel.auto.save()
		config.plugins.epanel.autosave.save()
		config.plugins.epanel.autobackup.save()
		configfile.save()
		self.mbox = self.session.open(MessageBox,(_("configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )
################################################################################################################
	def manual(self):
		self.session.open(epgdmanual)
################################################################################################################
	def restart(self):
		self.session.open(TryQuitMainloop, 3)
#####################################################
################################################################################################################
class epgdmanual(Screen):
	skin = """
<screen name="epgdmanual" position="center,260" size="850,50" title="EPG D+ de LINUX-BOX.ES">
  <ePixmap position="10,40" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,10" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,40" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,10" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="375,40" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="375,10" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="574,40" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/blue.png" alphatest="blend" />
  <widget source="key_blue" render="Label" position="574,10" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
</screen>"""
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("EPG D+ de LinuxBox"))
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Guardar epg.dat"))
		self["key_yellow"] = StaticText(_("Restaurar epg.dat"))
		self["key_blue"] = StaticText(_("Releer epg.dat"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.savepg,
			"yellow": self.restepg,
			"blue": self.reload,
		}, -2)
################################################################################################################
	def reload(self):
		try:
			if fileExists("%sepgtmp/epg.dat.gz" % config.plugins.epanel.direct.value):
				os.system("cp -f %sepgtmp/epg.dat.gz %s" % (config.plugins.epanel.direct.value, config.plugins.epanel.direct.value))
				os.system("gzip -df %sepg.dat.gz" % config.plugins.epanel.direct.value)
				os.chmod("%sepg.dat" % config.plugins.epanel.direct.value, 0644)
			epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
			epgcache = eEPGCache.getInstance().load()
			self.mbox = self.session.open(MessageBox,(_("epg.dat reloaded")), MessageBox.TYPE_INFO, timeout = 4 )
		except:
			self.mbox = self.session.open(MessageBox,(_("reload epg.dat failed")), MessageBox.TYPE_INFO, timeout = 4 )
################################################################################################################
	def savepg(self):
		epgcache = new.instancemethod(_enigma.eEPGCache_save,None,eEPGCache)
		epgcache = eEPGCache.getInstance().save()
		self.mbox = self.session.open(MessageBox,(_("epg.dat saved")), MessageBox.TYPE_INFO, timeout = 4 )
		
	def restepg(self):
		epgcache = new.instancemethod(_enigma.eEPGCache_load,None,eEPGCache)
		epgcache = eEPGCache.getInstance().load()
		self.mbox = self.session.open(MessageBox,(_("epg.dat restored")), MessageBox.TYPE_INFO, timeout = 4 )
		
	def cancel(self):
		self.close(False)
##############################################################################
class CrontabMan(Screen):
	skin = """
<screen name="CrontabMan" position="center,160" size="1150,500" title="CRON MANAGER">
  #<ePixmap position="700,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo16.png" alphatest="blend" transparent="1" />
	<ePixmap position="20,488" zPosition="1" size="175,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,458" zPosition="2" size="175,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_green" render="Label" position="195,458" zPosition="2" size="175,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="195,488" zPosition="1" size="175,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
	<widget source="key_yellow" render="Label" position="370,458" zPosition="2" size="175,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="370,488" zPosition="1" size="175,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
	<widget source="menu" render="Listbox" position="15,15" size="660,450" scrollbarMode="showOnDemand">
		<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (10, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 29
	}
			</convert>
		</widget>
</screen>"""
	
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("CRON MANAGER"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],

		{
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.GreenKey,
			"yellow": self.YellowKey,
		})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Add tabs"))
		self["key_yellow"] = StaticText(_("Remove tabs"))
		self.list = []
		self["menu"] = List(self.list)
		self.cMenu()

	def cMenu(self):
		self.list = []
		count = 0
		if fileExists("/etc/cron/crontabs/root"):
			cron = open("/etc/cron/crontabs/root", "r")
			for line in cron:
				count = count + 1
				self.list.append((line, count))
			cron.close()
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.Ok, "cancel": self.close}, -1)

	def Ok(self):
		self.close()
		
	def GreenKey(self):
		self.session.openWithCallback(self.cMenu,CrontabManAdd)

	
	def YellowKey(self):
		try:
			os.system("sed -i %sd /etc/cron/crontabs/root" % str(self["menu"].getCurrent()[1]))
			os.system("echo -e 'root' >> /etc/cron/crontabs/cron.update")
		except:
			pass
		self.cMenu()
		
	def exit(self):
		self.close()
####################################################################
class CrontabManAdd(ConfigListScreen, Screen):
	skin = """
<screen name="CrontabManAdd" position="center,160" size="750,370" title="add tabs" >
		<widget position="15,10" size="720,300" name="config" scrollbarMode="showOnDemand" />
		<ePixmap position="10,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
		<widget source="key_red" render="Label" position="10,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<ePixmap position="175,358" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
		<widget source="key_green" render="Label" position="175,328" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />

</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("add tabs"))
		self.list = []
		self.list.append(getConfigListEntry(_("Min"), config.plugins.epanel.min))
		self.list.append(getConfigListEntry(_("Hour"), config.plugins.epanel.hour))
		self.list.append(getConfigListEntry(_("Day of month"), config.plugins.epanel.dayofmonth))
		self.list.append(getConfigListEntry(_("Month"), config.plugins.epanel.month))
		self.list.append(getConfigListEntry(_("Day of week"), config.plugins.epanel.dayofweek))
		self.list.append(getConfigListEntry(_("Command"), config.plugins.epanel.command))
		self.list.append(getConfigListEntry(_("Every"), config.plugins.epanel.every))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Add"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.ok,
			"ok": self.ok
		}, -2)
		
	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close()
		
	
	def ok(self):
		everymin = ""
		everyhour = ""
		everydayofmonth = ""
		everymonth = ""
		everydayofweek = ""
		if config.plugins.epanel.min.value != '*' and config.plugins.epanel.every.value == '1':
			everymin = '/'
		elif config.plugins.epanel.hour.value != '*' and config.plugins.epanel.every.value == '2':
			everyhour = '/'
		elif config.plugins.epanel.dayofmonth.value != '*' and config.plugins.epanel.every.value == '3':
			everydayofmonth = '/'
		elif config.plugins.epanel.month.value != '*' and config.plugins.epanel.every.value == '4':
			everymonth = '/'
		elif config.plugins.epanel.dayofweek.value != '*' and config.plugins.epanel.every.value == '5':
			everydayofweek = '/'
			
		if config.plugins.epanel.min.value == '*' and config.plugins.epanel.hour.value == '*' and config.plugins.epanel.dayofmonth.value == '*' and config.plugins.epanel.month.value == '*' and  config.plugins.epanel.dayofweek.value == '*':
			print ("error")
		else:
			os.system("echo -e '%s%s %s%s %s%s %s%s %s%s    %s' >> /etc/cron/crontabs/root" % (everymin, config.plugins.epanel.min.value,
																				everyhour, config.plugins.epanel.hour.value, 
																				everydayofmonth, config.plugins.epanel.dayofmonth.value,
																				everymonth, config.plugins.epanel.month.value,
																				everydayofweek, config.plugins.epanel.dayofweek.value,
																				config.plugins.epanel.command.value))
		os.system("echo -e 'root' >> /etc/cron/crontabs/cron.update")
		for i in self["config"].list:
			i[1].cancel()
		self.close()
###############################################################################
class Info2Screen(Screen):
	skin = """
<screen name="Info2Screen" position="center,100" size="890,560" title="System Info">
	<ePixmap position="20,548" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,518" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget name="text" position="15,10" size="860,500" font="Console;20" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("System Info"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"ok": self.exit,
			})
		self["key_red"] = StaticText(_("Close"))
		self["text"] = ScrollLabel("")
		self.meminfoall()
		
	def exit(self):
		self.close()
		
	def meminfoall(self):
		list = " "
		try:
			os.system("free>/tmp/mem && echo>>/tmp/mem && df -h>>/tmp/mem")
			meminfo = open("/tmp/mem", "r")
			for line in meminfo:
				list += line
			self["text"].setText(list)
			meminfo.close()
			os.system("rm /tmp/mem")
		except:
			list = " "
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions"], { "cancel": self.close, "up": self["text"].pageUp, "left": self["text"].pageUp, "down": self["text"].pageDown, "right": self["text"].pageDown,}, -1)
######################################################################################
class Libermen(Screen):
	skin = """
	<screen name="ScriptScreen" position="center,160" size="1150,500" title="Liberar Memoria" >
	    <ePixmap position="715,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo12.png" alphatest="blend" transparent="1" />
			<widget name="list" position="20,10" size="660,450" scrollbarMode="showOnDemand" />
		<ePixmap position="20,488" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
		<widget source="key_red" render="Label" position="20,458" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		</screen>"""

	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.setTitle(_("Liberar Memoria"))
		self.scrpit_menu()
		self["key_red"] = StaticText(_("Close"))
		self["actions"] = ActionMap(["OkCancelActions","ColorActions"], {"ok": self.run, "red": self.exit, "cancel": self.close}, -1)
		
	def scrpit_menu(self):
		list = []
		try:
			list = os.listdir("%s" % config.plugins.epanel.scriptpath1.value[:-1])
			list = [x[:-3] for x in list if x.endswith('.sh')]
		except:
			list = []
		list.sort()
		self["list"] = MenuList(list)
		
	def run(self):
		script = self["list"].getCurrent()
		if script is not None:
			name = ("%s%s.sh" % (config.plugins.epanel.scriptpath1.value, script))
			os.chmod(name, 0755)
			self.session.open(Console, script.replace("_", " "), cmdlist=[name])
			
	def config_path(self):
		self.session.open(ConfigScript)

	def exit(self):
		self.close()

######################################################################################
class scanhost(ConfigListScreen, Screen):
	skin = """
<screen name="scanhost" position="center,160" size="1150,500" title="Check Host LINUX-BOX.ES">
    <ePixmap position="715,10" zPosition="1" size="450,700" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/fondo100.png" alphatest="blend" transparent="1" />
  <widget position="15,10" size="690,450" name="config" scrollbarMode="showOnDemand" />
   <ePixmap position="10,488" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
  <widget source="key_red" render="Label" position="10,458" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="175,488" zPosition="1" size="165,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/green.png" alphatest="blend" />
  <widget source="key_green" render="Label" position="175,458" zPosition="2" size="165,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <ePixmap position="340,488" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/yellow.png" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="340,458" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="540,488" zPosition="1" size="200,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/blue.png" alphatest="blend" />
  <widget source="key_blue" render="Label" position="540,458" zPosition="2" size="200,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
  <widget name="LabelStatus" position="10,400" zPosition="2" size="400,40"  font="Regular;20"/>
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("SCAN PEER LINUX-BOX.ES"))
		self.list = []
		self.list.append(getConfigListEntry(_("Test diario automatico"), config.plugins.epanel.checkauto))
		self.list.append(getConfigListEntry(_("Hora test"), config.plugins.epanel.checkhour))
		self.list.append(getConfigListEntry(_("Desactivar lineas con fallos"), config.plugins.epanel.checkoff))
		self.list.append(getConfigListEntry(_("Tipo de scan"), config.plugins.epanel.checktype))
		self.list.append(getConfigListEntry(_("Auto scan localhost"), config.plugins.epanel.autocheck))
		self.list.append(getConfigListEntry(_("Enviar email con resultados"), config.plugins.epanel.lbemail))
		self.list.append(getConfigListEntry(_("Email solo si hay peligros"), config.plugins.epanel.warnonlyemail))
		self.list.append(getConfigListEntry(_("Enviar el reporte a: (email)"), config.plugins.epanel.lbemailto))
		self.list.append(getConfigListEntry(_("Servidor smtp"), config.plugins.epanel.smtpserver))
		self.list.append(getConfigListEntry(_("Usuario smtp"), config.plugins.epanel.smtpuser))
		self.list.append(getConfigListEntry(_("Password smtp"), config.plugins.epanel.smtppass))
		ConfigListScreen.__init__(self, self.list)
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Save"))
		self["key_yellow"] = StaticText(_("View"))
		self["key_blue"] = StaticText(_("Run"))
		self["setupActions"] = ActionMap(["SetupActions", "ColorActions"],
		{
			"red": self.cancel,
			"cancel": self.cancel,
			"green": self.save,
			"yellow": self.viewscanlog,
			"blue": self.checkt,
			"ok": self.save
		}, -2)
		self["LabelStatus"] = Label(_("Configure and press blue key to check"))
		
        def check(self):
	        try:   
			self["LabelStatus"].setText("Scan init")                     
        		os.system("/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/lbscan.py %s %s %s %s" % (config.plugins.epanel.checktype.value, config.plugins.epanel.autocheck.value, config.plugins.epanel.checkoff.value, config.plugins.epanel.warnonlyemail.value))
        		self["LabelStatus"].setText("Scan end")
        		self.session.open(showScan)
                except IOError:
                      	self.mbox = self.session.open(MessageBox,(_("Sorry, I can not find lbscan.py")), MessageBox.TYPE_INFO, timeout = 4 )
		
        def checkt(self):
	        try:   
	        	self["LabelStatus"].setText("Scan init")
        		self.session.open(Console,_("Scan peer"),["/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/lbscan.py " + config.plugins.epanel.checktype.value + " " + config.plugins.epanel.autocheck.value + " " + config.plugins.epanel.checkoff.value + " " + config.plugins.epanel.warnonlyemail.value])
        		self["LabelStatus"].setText("Scan end")
        		# Send email with result by cron
        		
#        		self.session.open(showScan)
                except:
                      	self.mbox = self.session.open(MessageBox,(_("Sorry, I can not find lbscan.py")), MessageBox.TYPE_INFO, timeout = 4 )
	def viewscanlog(self):
		if (os.path.exists("/tmp/.lbscan.log")):
			 self.session.open(showScan)
		else:
			 self.mbox = self.session.open(MessageBox,(_("Sorry, I can not find scan data, scan first")), MessageBox.TYPE_INFO, timeout = 4 )
		
	def cancel(self):
		for i in self["config"].list:
			i[1].cancel()
		self.close(False)
	
	def save(self):
		config.plugins.epanel.checkauto.save()
		config.plugins.epanel.checkhour.save()
		config.plugins.epanel.checkoff.save()
		config.plugins.epanel.checktype.save()
		config.plugins.epanel.autocheck.save()
		config.plugins.epanel.lbemail.save()
		config.plugins.epanel.warnonlyemail.save()
		config.plugins.epanel.lbemailto.save()
		config.plugins.epanel.smtpserver.save()
		config.plugins.epanel.smtpuser.save()
		config.plugins.epanel.smtppass.save()
		configfile.save()
		self.mbox = self.session.open(MessageBox,(_("Configuration is saved")), MessageBox.TYPE_INFO, timeout = 4 )

	def messagebox(self):
		self.mbox = self.session.open(MessageBox,(_("Scaning hosts, please wait")), MessageBox.TYPE_INFO, timeout = 4 )
	
	
################################################################################################################
class showScan(Screen):
	skin = """
<screen name="Show Scan" position="center,100" size="890,560" title="Show Scan Results">
	<ePixmap position="20,548" zPosition="1" size="170,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/LBpanel/images/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,518" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget name="text" position="15,10" size="860,500" font="Console;20" />
</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("Scan Results"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"ok": self.exit,
			})
		self["key_red"] = StaticText(_("Close"))
		self["text"] = ScrollLabel("")
		self.meminfoall()
		
	def exit(self):
		self.close()
		
	def meminfoall(self):
		list = " "
		try:
			scaninfo = open("/tmp/.lbscan.log", "r")
			for line in scaninfo:
				list += line
			self["text"].setText(list)
			scaninfo.close()
		except:
			list = " "
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions"], { "cancel": self.close, "up": self["text"].pageUp, "left": self["text"].pageUp, "down": self["text"].pageDown, "right": self["text"].pageDown,}, -1)
