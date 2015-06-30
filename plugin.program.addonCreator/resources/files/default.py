# -*- coding: utf-8 -*-

"""
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
"""

import xbmc, xbmcgui, xbmcplugin, sys, re

plugin_handle = int(sys.argv[1])
xbmcplugin.setContent(plugin_handle, "movies")
icon = xbmc.translatePath("special://home/addons/plugin.video.MyNewlyCreatedAddon/icon.png")
fanart = xbmc.translatePath("special://home/addons/plugin.video.MyNewlyCreatedAddon/fanart.jpg")
xml_playlist = xbmc.translatePath("special://home/addons/plugin.video.MyNewlyCreatedAddon/playlist.xml")
m3u_playlist = xbmc.translatePath("special://home/addons/plugin.video.MyNewlyCreatedAddon/playlist.m3u")
xml_regex = "<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>"
m3u_regex = "#.+,(.+?)\n(.+?)\n"

def read_file(file):
    try:
        f = open(file, "r")
        content = f.read()
        f.close()
        return content
    except:
        pass

def add_link(name, url, img = "", fanart = ""):
    liz = xbmcgui.ListItem(name, iconImage = img, thumbnailImage = img)
    liz.setInfo("video", infoLabels = {"Title": name})
    liz.setProperty("fanart_image", fanart)
    liz.setProperty("IsPlayable", "false")
    xbmcplugin.addDirectoryItem(plugin_handle, url, listitem = liz)
    return	
	
try:
    link = read_file(m3u_playlist)
    match = re.compile(m3u_regex).findall(link)
    for name, url in match:
        try:
            url = url.replace('"', ' ').replace('&amp;', '&').strip()
            name = re.sub('\s+', ' ', name).replace('"', ' ').strip()
            add_link(name, url, icon, fanart)
        except:
            pass
except:
    pass

try:
    link = read_file(xml_playlist)
    match = re.compile(xml_regex).findall(link)
    for name, url, thumb in match:
        try:
            url = url.replace('"', ' ').replace('&amp;', '&').strip()
            name = re.sub('\s+', ' ', name).replace('"', ' ').strip()
            if (len(thumb) > 0):
                add_link(name, url, thumb, thumb)
            else:
                add_link(name, url, icon, fanart)
        except:
            pass
except:
    pass

xbmcplugin.endOfDirectory(plugin_handle)
sys.exit(0)