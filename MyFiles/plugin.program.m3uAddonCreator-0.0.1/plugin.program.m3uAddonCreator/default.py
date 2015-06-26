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

import urllib, urllib2, re, os, sys, shutil, zipfile
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

mysettings = xbmcaddon.Addon(id = 'plugin.program.m3uAddonCreator')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
m3u_file = mysettings.getSetting('m3u_file')
name_of_addon = mysettings.getSetting('name_of_addon')
provider_name = mysettings.getSetting('provider_name')
addon_icon = mysettings.getSetting('addon_icon')
addon_fanart = mysettings.getSetting('addon_fanart')
dst_folder =  mysettings.getSetting('dst_folder')
m3u_regex = '#.+,(.+?)\n(.+?)\n'

def open_file(file):
	try:
		f = open(file, 'r')
		content = f.read()
		f.close()
		return content	
	except:
		pass 

def main():
	if (len(m3u_file) > 0) and (len(name_of_addon) > 0) and (len(provider_name) > 0) and (len(addon_icon) > 0) and (len(addon_fanart) > 0) and (len(dst_folder) > 0):
		try:		
			# Create default.py
			os.makedirs (xbmc.translatePath(os.path.join(home, 'plugin.video.' + name_of_addon + '/plugin.video.' + name_of_addon)))
			temp_plugin_folder = xbmc.translatePath(os.path.join(home, 'plugin.video.' + name_of_addon + '/plugin.video.' + name_of_addon))
			f = open(temp_plugin_folder + '/default.py', 'w')
			f.write('# -*- coding: utf-8 -*-' + '\n\n')
			f.write('import xbmc, xbmcgui, xbmcplugin, sys' + '\n\n')
			f.write('plugin_handle = int(sys.argv[1])' + '\n')
			f.write('xbmcplugin.setContent(plugin_handle, "movies")' + '\n')
			f.write('icon = xbmc.translatePath("special://home/addons/plugin.video.' + name_of_addon + '/icon.png")' + '\n')
			f.write('fanart = xbmc.translatePath("special://home/addons/plugin.video.' + name_of_addon + '/fanart.jpg")\n\n')	
			f.write('def add_item(url, infolabels, img = "", fanart = ""):' + '\n' + '    listitem = xbmcgui.ListItem(infolabels["title"], iconImage=img, thumbnailImage=img)' + '\n' + '    listitem.setInfo("video", infolabels)' + '\n' + '    listitem.setProperty("fanart_image", fanart)' + '\n' + '    listitem.setProperty("IsPlayable", "false")' + '\n' + '    xbmcplugin.addDirectoryItem(plugin_handle, url, listitem)' + '\n' + '    return' + '\n\n')			
			link = open_file(m3u_file)  
			match = re.compile(m3u_regex).findall(link) 
			for title, url in match:
				url = url.replace('"', ' ').strip()
				title = re.sub('\s+', ' ', title).replace('"', ' ').strip()
				f.write('add_item("' + url + '", {"title": "' + title + '"}, icon, fanart)\n')
			f.write('\n' + 'xbmcplugin.endOfDirectory(plugin_handle)' + '\n' + 'sys.exit(0)')				
			f.close()
			
			# Create addon.xml
			f = open(temp_plugin_folder + '/addon.xml', 'w')			
			f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' + '\n')
			f.write('<addon id="plugin.video.' + name_of_addon + '" name="' + name_of_addon + '" version="1.0.0" provider-name="' + provider_name + '">' + '\n')			
			f.write('    <requires>' + '\n' + '        <import addon="xbmc.python" version="2.1.0" />' + '\n' + '    </requires>' + '\n')
			f.write('    <extension point="xbmc.python.pluginsource"' + '\n' + '               library="default.py">' + '\n' + '        <provides>video</provides>' + '\n' + '    </extension>' + '\n')
			f.write('    <extension point="xbmc.addon.metadata">' + '\n' + '        <platform>all</platform>' + '\n' + '        <summary>My first addon</summary>' + '\n' + '        <description>Play video and audio</description>' + '\n' + '    </extension>' + '\n')
			f.write('</addon>')			
			f.close()
			
			# Copy chosen icon and fanar to temp plugin folder
			shutil.copy(addon_icon, temp_plugin_folder)
			shutil.copy(addon_fanart, temp_plugin_folder)
			
			# Create temp plugin zip file
			my_first_addon = xbmc.translatePath(os.path.join(home, 'plugin.video.' + name_of_addon))
			shutil.make_archive(my_first_addon, 'zip', my_first_addon)	
			
			# Delete temp plugin folder			
			if os.path.exists(my_first_addon):
				shutil.rmtree(my_first_addon)
			else: 
				pass
			
			# Delete old plugin zip file if exist and move temp plugin zip file to final destination.			
			try:	
				os.remove(dst_folder + 'plugin.video.' + name_of_addon + '.zip')
			except: 
				pass			
			shutil.move(my_first_addon + '.zip', dst_folder)
			
			# Conclusion
			xbmcgui.Dialog().ok('Addon Creator', 'Done.', '', 'Enjoy!')			
		except:	
			xbmcgui.Dialog().ok('Addon Creator', 'Oops! Something is terribly wrong.', '', 'Try again.')
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
	main()
	sys.exit(0)

xbmcplugin.endOfDirectory(int(sys.argv[1]))