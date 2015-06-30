# -*- coding: utf-8 -*-

'''
Copyright (C) 2015                                                     

This program is free software: you can redistribute it and/or modify   
it under the terms of the GNU General Public License as published by   
the Free Software Foundation, either version 3 of the License, or      
(at your option) any later version.                                    

This program is distributed in the hope that it will be useful,        
but WITHOUT ANY WARRANTY; without even the implied warranty of         
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          
GNU General Public License for more details.                           

You should have received a copy of the GNU General Public License      
along with this program. If not, see <http://www.gnu.org/licenses/>  
'''                                                                           

import urllib, urllib2, re, os, sys, shutil
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

mysettings = xbmcaddon.Addon(id = 'plugin.program.addonCreator')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
logos = xbmc.translatePath(os.path.join(home, 'resources/logos/'))

license_txt = xbmc.translatePath(os.path.join(home, 'LICENSE.txt'))
default_file = xbmc.translatePath(os.path.join(home, 'resources/files/default.py'))
addon_file = xbmc.translatePath(os.path.join(home, 'resources/files/addon.xml'))

name_of_plugin_folder = mysettings.getSetting('name_of_plugin_folder')
my_first_addon = xbmc.translatePath('special://home/addons/plugin.video.' + name_of_plugin_folder)
name_of_addon = mysettings.getSetting('name_of_addon')
addon_version_number = mysettings.getSetting('addon_version_number')
provider_name = mysettings.getSetting('provider-name')
addon_icon = mysettings.getSetting('addon_icon')
addon_fanart = mysettings.getSetting('addon_fanart')
sum_mary = mysettings.getSetting('sum_mary')
desc = mysettings.getSetting('desc')
xml_file = mysettings.getSetting('xml_file')
xml_regex = '<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>'
m3u_file = mysettings.getSetting('m3u_file')
m3u_regex = '#.+,(.+?)\n(.+?)\n'

def open_file(file):
	try:
		f = open(file, 'r')
		content = f.read()
		f.close()
		return content	
	except:
		pass 
		
def home():
	add_dir(
				'[COLOR white]Create[COLOR cyan] XBMC/Kodi addons[COLOR white] with [COLOR yellow]M3U and/or XML[COLOR red][B] NO REGEX[/B][/COLOR]', 
				'AddonCreator', 1, logos + 'kodi_xbmc.png', fanart
			)

def check_settings(): 
	if (	
			len(name_of_plugin_folder) > 0 and len(name_of_addon) > 0 and len(addon_version_number) > 0 and 
			len(provider_name) > 0 and len(addon_icon) > 0 and len(addon_fanart) > 0 and len(sum_mary) > 0 and len(desc) > 0
		):
			create_addon()
	else:	
		mysettings.openSettings()

def completion_note():
	xbmcgui.Dialog().ok(
							'Add-on Creator', '[COLOR red][B]Please manually reboot XBMC - KODI[/B][/COLOR]', 
							'Look for your new add-on in [B]VIDEOS >> Add-ons[/B]', 'Done. Enjoy!'
						)			

def error_warning():
	xbmcgui.Dialog().ok(
							'Add-on Creator', '[COLOR red][B]Oops! Something has gone terribly wrong.[/B][/COLOR]', 
							'[B]Double check [COLOR red]ALL[/COLOR] settings.[/B]', 'Then try again.'
						)

def copy_files():
	# Delete the same old plug-in folder if exists and create new empty one.
	try:
		shutil.rmtree(my_first_addon)
	except:
		pass				
	os.mkdir(my_first_addon)	
	
	# Copy license.txt, icon.png, and fanart.jpg
	shutil.copy(license_txt, my_first_addon)			
	shutil.copy(addon_icon, my_first_addon)
	shutil.copy(addon_fanart, my_first_addon)
	
	# Copy default.py and replace the target string.
	shutil.copy(default_file, my_first_addon)
	d_file = xbmc.translatePath(os.path.join(my_first_addon, 'default.py'))
	""" Read in the default.py file """
	default_py = None
	with open(d_file, 'r') as f :
		default_py = f.read()
		f.close()
	""" Replace the target string """
	default_py = default_py.replace('MyNewlyCreatedAddon', name_of_plugin_folder)
	""" Write the default.py file out again """
	with open(d_file, 'w') as f:
		f.write(default_py)	
		f.close()
		
	# Copy addon.xml and replace the target strings.		
	shutil.copy(addon_file, my_first_addon)
	a_file = xbmc.translatePath(os.path.join(my_first_addon, 'addon.xml'))
	addon_xml = None
	with open(a_file, 'r') as f :
		addon_xml = f.read()
		f.close()
	addon_xml = addon_xml.replace(
									'<addon id="" name="" version="" provider-name="">', '<addon id="' + 
									name_of_plugin_folder + '" name="' + name_of_addon + '" version="' + 
									addon_version_number + '" provider-name="' + provider_name + '">'
								  )
	addon_xml = addon_xml.replace('<summary>', '<summary>' + sum_mary).replace('<description>', '<description>' + desc).replace('\[', '[').replace('\]', ']')
	with open(a_file, 'w') as f:
		f.write(addon_xml)
		f.close()		
	
def create_addon():
	if len(m3u_file) < 1 and len(xml_file) < 1: 
		mysettings.openSettings()

	elif len(m3u_file) > 0 and len(xml_file) > 0:
		try:
			copy_files(); m3u_playlist(); xml_playlist(); completion_note()								
		except:	
			error_warning()
		
	elif len(m3u_file) > 0 and len(xml_file) < 1:
		try:
			copy_files(); m3u_playlist(); completion_note()								
		except:	
			error_warning()		

	elif len(m3u_file) < 1 and len(xml_file) > 0:
		try:
			copy_files(); xml_playlist(); completion_note()								
		except:	
			error_warning()	

def m3u_playlist():
	m3uPlaylist = open_file(m3u_file)
	f = open(my_first_addon + '/playlist.m3u', 'w')
	f.write(m3uPlaylist)
	f.close()
	
def xml_playlist():
	xmlPlaylist = open_file(xml_file)
	f = open(my_first_addon + '/playlist.xml', 'w')
	f.write(xmlPlaylist)
	f.close()
			
def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring)>= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]
	return param

def add_dir(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

params = get_params()
url = None
name = None
mode = None
iconimage = None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode = int(params["mode"])
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass  
 
print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
print "iconimage: " + str(iconimage)

if mode == None or url == None or len(url)<1:
	home()

elif mode == 1:
	check_settings()
	sys.exit(0)

xbmcplugin.endOfDirectory(int(sys.argv[1]))