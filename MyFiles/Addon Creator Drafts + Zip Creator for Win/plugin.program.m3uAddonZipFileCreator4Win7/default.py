# -*- coding: utf-8 -*-

'''
Copyright (C) 2014                                                     

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

mysettings = xbmcaddon.Addon(id = 'plugin.program.m3uAddonZipFileCreator4Win7')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
name_of_plugin_folder = mysettings.getSetting('name_of_plugin_folder')
name_of_addon = mysettings.getSetting('name_of_addon')
addon_version_number = mysettings.getSetting('addon_version_number')
provider_name = mysettings.getSetting('provider_name')
addon_icon = mysettings.getSetting('addon_icon')
addon_fanart = mysettings.getSetting('addon_fanart')
sum_mary = mysettings.getSetting('sum_mary')
desc = mysettings.getSetting('desc')
dst = mysettings.getSetting('dst')
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
	add_dir('[COLOR cyan]Create your own XBMC/Kodi add-on [COLOR red][B]zip file[/B] [COLOR yellow]from m3u playlist[/COLOR]', 'addoncreator', 1, icon, fanart)

def create_addon():
	if (len(m3u_file) > 0) and (len(name_of_plugin_folder) > 0) and (len(name_of_addon) > 0) and (len(addon_version_number) > 0) and (len(provider_name) > 0) and (len(addon_icon) > 0) and (len(addon_fanart) > 0) and (len(sum_mary) > 0) and (len(desc) > 0) and (len(dst) > 0):
		try:		
			# Define folders.
			addon_folders = xbmc.translatePath('special://home/addons/plugin.video.' + name_of_plugin_folder + '/plugin.video.' + name_of_plugin_folder)
			my_first_addon = (xbmc.translatePath('special://home/addons/plugin.video.' + name_of_plugin_folder))
			print 'Level 1: Done'
			# Delete old folder and zip file if exist and create new empty folder and sub-folder for add-on
			if os.path.exists(my_first_addon):
				shutil.rmtree(my_first_addon)
			else:
				pass
			if os.path.exists(my_first_addon + '.zip'):
				os.remove(my_first_addon + '.zip')			
			else:
				pass
			os.makedirs(addon_folders)
			print 'Level 2: Done'
			# Create default.py
			f = open(addon_folders + '/default.py', 'w')
			f.write('# -*- coding: utf-8 -*-' + '\n\n')
			f.write('import xbmc, xbmcgui, xbmcplugin, sys' + '\n\n')
			f.write('plugin_handle = int(sys.argv[1])' + '\n')
			f.write('xbmcplugin.setContent(plugin_handle, "movies")' + '\n')
			f.write('icon = xbmc.translatePath("special://home/addons/plugin.video.' + name_of_plugin_folder + '/icon.png")' + '\n')
			f.write('fanart = xbmc.translatePath("special://home/addons/plugin.video.' + name_of_plugin_folder + '/fanart.jpg")\n\n')	
			f.write('def add_item(url, infolabels, img = "", fanart = ""):' + '\n' + '    listitem = xbmcgui.ListItem(infolabels["title"], iconImage = img, thumbnailImage = img)' + '\n' + '    listitem.setInfo("video", infolabels)' + '\n' + '    listitem.setProperty("fanart_image", fanart)' + '\n' + '    listitem.setProperty("IsPlayable", "false")' + '\n' + '    xbmcplugin.addDirectoryItem(plugin_handle, url, listitem)' + '\n' + '    return' + '\n\n')			
			link = open_file(m3u_file)  
			match = re.compile(m3u_regex).findall(link) 
			for title, url in match:
				url = url.replace('"', ' ').strip()
				title = re.sub('\s+', ' ', title).replace('"', ' ').strip()
				f.write('add_item("' + url + '", {"title": "' + title + '"}, icon, fanart)\n')
			f.write('\n' + 'xbmcplugin.endOfDirectory(plugin_handle)' + '\n' + 'sys.exit(0)')				
			f.close()
			print 'Level 3: Done'
			# Create addon.xml
			f = open(addon_folders + '/addon.xml', 'w')			
			f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + '\n')
			f.write('<addon id="plugin.video.' + name_of_plugin_folder + '" name="' + name_of_addon.replace('\[', '[').replace('\]', ']') + '" version="' + addon_version_number + '" provider-name="' + provider_name.replace('\[', '[').replace('\]', ']') + '">' + '\n')			
			#f.write('    <requires>' + '\n' + '        <import addon="xbmc.python" version="2.1.0" optional="true" />' + '\n' + '    </requires>' + '\n')
			f.write('    <requires>' + '\n' + '    </requires>' + '\n') # Require nothing
			f.write('    <extension point="xbmc.python.pluginsource"' + '\n' + '               library="default.py">' + '\n' + '        <provides>video</provides>' + '\n' + '    </extension>' + '\n')
			f.write('    <extension point="xbmc.addon.metadata">' + '\n' + '        <platform>all</platform>' + '\n' + '        <summary>' + sum_mary.replace('\[', '[').replace('\]', ']') + '</summary>' + '\n' + '        <description>' + desc.replace('\[', '[').replace('\]', ']') + '</description>' + '\n' + '    </extension>' + '\n')
			f.write('</addon>')			
			f.close()
			print 'Level 4: Done'
			# Copy chosen icon and fanart to plugin folder
			shutil.copy(addon_icon, addon_folders)
			shutil.copy(addon_fanart, addon_folders)
			
			# Create zip file and delete add-on folder
			shutil.make_archive(my_first_addon, 'zip', my_first_addon)
			shutil.rmtree(my_first_addon)
			'''
			zf = zipfile.ZipFile(my_first_addon + ".zip", "w")
			for dirname, subdirs, files in os.walk(my_first_addon):
				zf.write(dirname)
				for filename in files:
					zf.write(os.path.join(dirname, filename))
			zf.close()
			'''
			# Delete old zip file if exist and move new add-on zip file to destination folder. 
			try:
				os.remove(xbmc.translatePath(os.path.join(dst, 'plugin.video.' + name_of_plugin_folder + '.zip')))
			except:
				pass
			shutil.move(my_first_addon + '.zip', dst)
			
			print 'Level 5: Done'
			# Conclusion
			xbmcgui.Dialog().ok('Add-on Zip File Creator', '[COLOR red][B]Go to destination folder to get add-on zip file.[/B][/COLOR]', '[B]Install it on any device running XBMC/Kodi.[/B]', 'Enjoy!')			
		except:	
			xbmcgui.Dialog().ok('Add-on Zip File Creator', '[COLOR red][B]Oops! Something has gone terribly wrong.[/B][/COLOR]', '[B]Double check ALL settings.[/B]', '[COLOR red][B]Make sure destination folder is writable.[/B][/COLOR]')
	else:	
		mysettings.openSettings()
				
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
	create_addon()
	sys.exit(0)

xbmcplugin.endOfDirectory(int(sys.argv[1]))