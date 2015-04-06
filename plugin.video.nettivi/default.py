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

import urllib, urllib2, re, os, sys
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

mysettings = xbmcaddon.Addon(id = 'plugin.video.nettivi')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
logos = xbmc.translatePath(os.path.join(home, 'resources', 'logos\\'))
MainDirTV = xbmc.translatePath(os.path.join(home, 'resources', 'playlists', 'MainDirTV.xml'))
localm3u = mysettings.getSetting('local_m3u')
onlinem3u = mysettings.getSetting('online_m3u')
localxml = mysettings.getSetting('local_xml')
onlinexml = mysettings.getSetting('online_xml')
localizedString = mysettings.getLocalizedString
m3u_regex = '#.+,(.+?)\n(.+?)\n'
xml_channel_name = '<channel>\s*<name>(.+?)</name>'
xml_regex = '<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>'
xml_regex_reg_1S = '<title>(.*?)</title>(?s).*?<page>(.*?)</page>(?s).*?<thumbnail>(.*?)</thumbnail>'
xml_regex_reg_2L = '<title>(.*?)</title>\s*<link>.*?</link>\s*<regex>\s*<name>.*?</name>\s*<expres>.*?</expres>\s*<page>(.*?)</page>\s*<referer>.*?</referer>\s*</regex>\s*<thumbnail>(.*?)</thumbnail>'
my_dict = {'&#7893;':'ổ', '&#7907;':'ợ', '&#7885;':'ọ', '&#7909;':'ụ', '&#7875;':'ể', '&#7843;':'ả', '&#7871;':'ế', '&#7897;':'ộ', '&#7889;':'ố', '&#7873;':'ề', '&#7883;':'ị', '&#7855;':'ắ'}
my_repo = 'https://raw.githubusercontent.com/daveln/repository.daveln/'
hplus = 'http://hplus.com.vn/vi/categories/live-tv'
anluongtv = 'http://tv.anluong.info/'
tvreplay = 'http://103.31.126.20/tvcatchup/'
tvviet = 'http://tv.vnn.vn/'
u_tube = 'http://www.youtube.com'

tv_mode = mysettings.getSetting('tv_mode')
if len(tv_mode) <= 0:
	xbmcgui.Dialog().ok(localizedString(10001), localizedString(10002), localizedString(10003), localizedString(10004))
	mysettings.openSettings() 

def get_cookie():
	from urllib2 import Request, build_opener, HTTPCookieProcessor, HTTPHandler
	import cookielib
	cj = cookielib.CookieJar()
	opener = build_opener(HTTPCookieProcessor(cj), HTTPHandler())
	req = Request(tvviet)
	f = opener.open(req)
	for cookie in cj:
		return "%s=%s" % (cookie.name, cookie.value)      

def replaceAll(text, my_dict):
	try:
		for a, b in my_dict.iteritems():
			text = text.replace(a, b)
		return text
	except:
		pass	

def open_file(file):
	try:
		f = open(file, 'r')
		content = f.read()
		f.close()
		return content	
	except:
		pass 

def make_request(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		req.add_header('Cookie', get_cookie())
		response = urllib2.urlopen(req, timeout = 60)	  
		link = response.read()
		response.close()  
		return link
	except urllib2.URLError, e:
		print 'We failed to open "%s".' % url
		if hasattr(e, 'code'):
			print 'We failed with error code - %s.' % e.code	
		if hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason

def main():
	content = open_file(MainDirTV)
	match = re.compile(xml_regex + '\s*<mode>(.*?)</mode>').findall(content)
	for name, url, thumb, add_dir_mode in match:
		add_dir(name, url, add_dir_mode, logos + thumb) 

def direct_link(): 
	content = make_request(my_repo + 'master/playlists/direct_link.m3u')
	match = re.compile(m3u_regex).findall(content)
	for name, url in match:
		if 'hplus' in url or 'htvonline' in url or 'giniko' in url or 'tv.vnn.vn' in url:
			add_link(name, url, 202, logos + 'directlink.png')
		else:	
			add_link(name, url, 201, logos + 'directlink.png')

def my_tv_directory(url, iconimage): 
	content = make_request(url) 
	match = re.compile(xml_channel_name).findall(content)
	for channel_name in match:
		if 'UPDATED ON' in channel_name or 'CẬP NHẬT' in channel_name:
			add_link(channel_name, u_tube, 201, iconimage)
		else:
			if 'Tôn Giáo TV' in channel_name:
				add_dir(channel_name, url, 2, logos + 'myreligion.png')	  
			elif 'Âm Nhạc TV' in channel_name:
				add_dir(channel_name, url, 2, logos + 'mymusic.png')	  
			elif 'Radio Tổng Hợp' in channel_name:
				add_dir(channel_name, url, 2, logos + 'myradio.png')	  
			else:
				add_dir(channel_name, url, 2, iconimage) 

def my_tv_index(name, url, iconimage):	
	content = make_request(url) 
	match = re.compile('<channel>\s*<name>' + name + '</name>((?s).+?)</channel>').findall(content)
	for vlink in match:
		final_link = re.compile(xml_regex).findall(vlink)
		for title, url, thumb in final_link:
			if 'www.giniko.com' in url:
				add_link(title, url, 202, thumb)
			else:
				if len(thumb) <= 0:
					add_link(title, url, 201, iconimage) 
				else:	
					add_link(title, url, 201, thumb)  

def my_tv_scraper(url, iconimage):
	content = make_request(url)
	if 'hplus' in url:
		match = re.compile('href="http://hplus.com.vn/vi/genre/index(.+?)">(.+?)<').findall(content)
		for url, name in match:
			if 'Xem tất cả' in name: 
				pass 
			else: 
				add_dir(name, 'http://hplus.com.vn/vi/genre/index' + url, 101, 'http://static.hplus.com.vn/themes/front/images/logo.png')
	elif 'anluong' in url: 
		match = re.compile('href="(.+?)"><img title="(.+?)".+?\s*src="(.+?)"').findall(content)
		for url, name, thumb in match:	  
			if 'SCTV' in name or 'SAO TV HD' in name or 'NHẠC CÁCH MẠNG' in name:
				pass
			else: 
				add_dir(name.replace('SOPPING', 'SHOPPING'), anluongtv + url, 111, iconimage)
				for url, name, thumb in match:
					if 'SCTV' in name or 'SAO TV HD' in name:
						add_dir(name, anluongtv + url, 111, iconimage)
					else:
						pass 		
		match = re.compile('href="(.+?)"><img class="images-kenh1" src="(.+?)"').findall(content)
		for url, thumb in match:
			name = url.replace('?tab=sctv&xem=', '').upper()
			add_dir(name.replace('SCTV', 'SCTV '), anluongtv + url, 111, iconimage)		  
	elif 'tvcatchup' in url:
		match = re.compile('href="(\d+)/">(\d+)/<').findall(content)
		for url, name in match:
			add_dir(name, tvreplay + url, 121, iconimage)
	elif 'tv.vnn.vn' in url:
		match = re.compile('href="\/(.+?)">\s*<img src="\/(.+?)".+?\/>\s*(.+?)\n').findall(content)
		for url, thumb, title in match:
			title = replaceAll(title, my_dict)	
			add_link(title, tvviet + url, 202, (tvviet + thumb).replace(' ', '%20'))  	  

def tvtonghop_anluong(name, url, iconimage):
	content = make_request(url)
	match = re.compile('onclick="configurator\(this\)" name="(.+?)">(.+?)<').findall(content)
	for url, channel_name in match:  
		if 'f4m' in url:
			url = url.split('=')[-1]
			url = 'plugin://plugin.video.f4mTester/?url=' + url
			add_link(name + '[COLOR magenta] - [/COLOR]' + channel_name.replace(' sever', 'Link') + ' [COLOR yellow](f4m)[/COLOR]', url, 201, iconimage)
		else:
			add_link(name + '[COLOR magenta] - [/COLOR]' + channel_name.replace(' sever', 'Link'), url, 203, iconimage)  

def tvreplay_link(url, iconimage):
	content = make_request(url)
	match = re.compile('href="(.+?)">(.+?)\.mp4</a></td><td align="right">.+?</td><td align="right">(.+?)<').findall(content)
	for href, name, video_size in match:
		name = name.split('_')
		name = name[0] + '_' + name[-1]
		add_link(name + '   [COLOR yellow]' + video_size + '[/COLOR]', url + '/' + href, 201, iconimage)

def my_playlist_directories(name, iconimage):
	if 'XML' in name:
		add_dir('[COLOR cyan]Online XML Playlist Của Tui[/COLOR]', 'onlinexml', 32, iconimage)
		add_dir('[COLOR orange]Local XML Playlist Của Tui[/COLOR]', 'localxml', 32, iconimage)  
	else:
		add_dir('[COLOR yellow]My Online M3U Playlist[/COLOR]', 'onlinem3u', 32, iconimage)
		add_dir('[COLOR lime]My Local M3U Playlist[/COLOR]', 'localm3u', 32, iconimage)

def my_playlist_links(name, iconimage):
	if 'Local M3U' in name:
		if len(localm3u) <= 0:
			mysettings.openSettings()
		else:  
			try:
				mym3u = open(localm3u, 'r')  
				link = mym3u.read()
				mym3u.close()
				match = re.compile(m3u_regex).findall(link)
				for title, url in match:
					add_link(title, url, 201, iconimage)
			except:
				pass 
	elif 'Online M3U' in name:
		if len(onlinem3u) > 0: 
			content = make_request(onlinem3u)
			match = re.compile(m3u_regex).findall(content)
			for title, url in match:
				add_link(title, url, 201, iconimage)
		else:		
			mysettings.openSettings()			
	elif 'Local XML' in name:
		if len(localxml) <= 0:
			mysettings.openSettings() 
		else:	  
			myxml = open(localxml, 'r')  
			link = myxml.read()
			myxml.close()
			if '<channel>' in link:
				match = re.compile(xml_channel_name).findall(link)
				for channel_name in match:
					if 'UPDATED ON' in channel_name or 'CẬP NHẬT' in channel_name:
						add_link(channel_name, u_tube, 201, iconimage)
					else:
						add_dir(channel_name, 'xmlfile', 33, iconimage)
			else:
				match = re.compile(xml_regex).findall(link)
				for title, url, thumb in match:
					if len(thumb) > 0:
						add_link(title, url, 201, thumb) 
					else:	
						add_link(title, url, 201, iconimage)  
	elif 'Online XML' in name:
		if len(onlinexml) > 0: 
			link = make_request(onlinexml)
			if '<channel>' in link:
				match = re.compile(xml_channel_name).findall(link)
				for channel_name in match:
					if 'UPDATED ON' in channel_name or 'CẬP NHẬT' in channel_name:
						add_link(channel_name, u_tube, 201, iconimage)
					else:		
						add_dir(channel_name, onlinexml, 33, iconimage)
			else:
				match = re.compile(xml_regex).findall(link)
				for title, url, thumb in match:
					if len(thumb) > 0:
						add_link(title, url, 201, thumb) 
					else:	
						add_link(title, url, 201, iconimage)  		  
		else:		  
			mysettings.openSettings()	

def playlist_channel(url, name, iconimage):
	name = name.replace('[', '\[').replace(']', '\]')
	if url == onlinexml:
		link = make_request(onlinexml)
	else:
		myxml = open(localxml, 'r')  
		link = myxml.read()
		myxml.close()
	match = re.compile('<channel>\s*<name>' + name + '</name>((?s).+?)</channel>').findall(link)	
	for vlink in match:
		final_link = re.compile(xml_regex).findall(vlink)
		for title, url, thumb in final_link:
			if len(thumb) <= 0:
				add_link(title, url, 201, iconimage)
			else:
				add_link(title, url, 201, thumb)	
				
def thanh51_xml_m3u_directory(iconimage):
	add_dir("[COLOR lime]thanh51's XML playlist[/COLOR]", my_repo + 'master/playlists/thanh51.xml', 12, iconimage)  
	add_dir("[COLOR blue]thanh51's M3U playlist[/COLOR]", my_repo + 'master/playlists/thanh51.m3u', 12, iconimage)  

def thanh51_xml_m3u_channel(url, iconimage):	
	content = make_request(url)
	if 'thanh51.xml' in url:
		if '<channel>' in content:
			match = re.compile(xml_channel_name).findall(content)
			for channel_name in match:
				if 'UPDATED ON' in channel_name or 'CẬP NHẬT' in channel_name:
					add_link(channel_name, u_tube, 201, iconimage)
				else:
					add_dir(channel_name, url, 13, iconimage)  	
		else:
			match = re.compile(xml_regex).findall(content)
			for title, url, thumb in match:
				if len(thumb) > 0:
					add_link(title, url, 201, thumb) 
				else:	
					add_link(title, url, 201, iconimage) 
	else:  
		if '<CHANNEL>' in content:
			match = re.compile('<NAME>(.+?)</NAME>').findall(content)
			for channel_name in match:
				if 'UPDATED ON' in channel_name or 'CẬP NHẬT' in channel_name:
					add_link(channel_name, u_tube, 201, iconimage)
				else:	
					add_dir(channel_name, url, 13, iconimage)  
		else:
			match = re.compile(m3u_regex).findall(content)
			for title, url in match: 
				if 'UPDATED ON' in title or 'CẬP NHẬT' in title:
					add_link(title, u_tube, 201, iconimage)
				else:
					add_link(title, url, 201, iconimage)

def thanh51_xml_m3u_index(url, name, iconimage):
	name = name.replace('[', '\[').replace(']', '\]')
	content = make_request(url)
	if 'thanh51.xml' in url:  
		match = re.compile('<channel>\s*<name>' + name + '</name>((?s).+?)</channel>').findall(content)	
		for vlink in match:
			if '<page>' in vlink:
				#final_link = re.compile(xml_regex_reg_1S).findall(vlink)
				final_link = re.compile(xml_regex_reg_2L).findall(vlink)
				for name, url, thumb in final_link:
					if len(thumb) <= 0:
						add_link(name, url, 202, iconimage)		
					else:
						add_link(name, url, 202, thumb) 
			else:		
				final_link = re.compile(xml_regex).findall(vlink)
				for title, url, thumb in final_link:
					if len(thumb) <= 0:
						add_link(title, url, 201, iconimage) 
					else:	
						add_link(title, url, 201, thumb)  
	else: 
		match = re.compile('#<CHANNEL>\s*#<NAME>' + name + '</NAME>((?s).*?)#</CHANNEL>').findall(content)
		vlink = re.compile(m3u_regex).findall(match[0])
		for title, ahref in vlink:	
			add_link(title, ahref, 201, iconimage) 

def atf01_m3u(url, iconimage):
	content = make_request(url)
	match = re.compile(m3u_regex).findall(content)
	for title, url in match:
		if 'UPDATED ON' in title or 'CẬP NHẬT' in title:
			add_link(title, u_tube, 201, iconimage)
		else:
			add_link(title, url, 201, iconimage)

def index(url, iconimage):
	content = make_request(url)
	if 'tv.anluong.info' in url:		
		match = re.compile('href="\?tab=kenhhd&xem=(.+?)"><img title="([^"]+)" class="images-kenh".+?src="([^"]*)"').findall(content)
		for url, name, thumb in match:	
			add_dir('SCTV HD - ' + name.replace('HD', '').replace('SCTV ', ''), anluongtv + '?tab=kenhhd&xem=' + url, 5, anluongtv + thumb)
		match = re.compile('href="(.+?)"><img class="images-kenh1"  src="(.+?)"').findall(content)
		for url, thumb in match:
			name = url.replace('?tab=sctv&xem=', '').upper()
			add_dir(name.replace('SCTV', 'SCTV '), anluongtv + url, 5, anluongtv + thumb) 
	elif 'htvonline' in url:
		match = re.compile("<a class=\"mh-grids5-img\".*?href=\"([^\"]*)\" title=\"(.+?)\">\s.*?\s*<img src=\"(.*?)\"").findall(content)
		for url, name, thumb in match:
			add_Link(name, url, thumb) 	  
	elif 'hplus' in url:
		match = re.compile('href="(.+?)" style.+?url\(\'(.+?)\'\)" data-content-tooltips="<div class.+?><h3 class.+?>(.+?)<').findall(content)
		for url, thumb, name in match:
			name = re.sub(' HD', ' [COLOR magenta]* [COLOR yellow]HD[/COLOR]', name)
			add_link(name, 'http://hplus.com.vn/' + url, 202, thumb + '?.png') 
			
def play_my_playlists(url):
	mediaUrl = url.replace('&amp;', '&')
	item = xbmcgui.ListItem(path = mediaUrl)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return

def resolve_url(url):	
	content = make_request(url)
	if 'htvonline' in url:   
		mediaUrl = re.compile("file: \"([^\"]*)\"").findall(content)[0] 
	elif 'hplus' in url:
		mediaUrl = re.compile('var iosUrl = "(.+?)"').findall(content)[0]	
	elif 'giniko' in url: 
		mediaUrl = re.compile('file: "(.+?)"').findall(content)[0]
	else:
		mediaUrl = re.compile("file: '(.+?)'").findall(content)[0]  
	item = xbmcgui.ListItem(path = mediaUrl)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)	  
	return

def play_tvtonghop(url):
	if 'm3u8' in url:
		mediaUrl = url.split('=')[-1]
	elif 'rtsp' in url:
		mediaUrl = url  
	else:
		content = make_request(url)
		try:  
			mediaUrl = re.compile('file: "(.+?)",').findall(content)[0]
		except:
			try:
				mediaUrl = re.compile('<param name="flashvars" value="src=(.+?)\?').findall(content)[0]  
			except:
				mediaUrl = re.compile("'streamer': '(.+?)',").findall(content)[0]+' playpath=' + re.compile("'file': '(.+?)',").findall(content)[0]			
				#mediaUrl = re.compile("'streamer': '(.+?)',").findall(content)[0] + '/' + re.compile("'file': '(.+?)',").findall(content)[0]	  
	item = xbmcgui.ListItem(path = mediaUrl)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	return

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

def add_dir(name, url, mode, iconimage):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

def add_link(name, url, mode, iconimage):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&iconimage=" + urllib.quote_plus(iconimage)	
	liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('IsPlayable', 'true')  
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz)  

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

if mode == None or url == None or len(url) < 1:
	if '1' in tv_mode:
		main()
	if '2' in tv_mode:
		direct_link()  	

elif mode == 1:
	my_tv_directory(url, iconimage)

elif mode == 2:  
	my_tv_index(name, url, iconimage)

elif mode == 3:
	my_tv_scraper(url, iconimage)  

elif mode == 11:  
	thanh51_xml_m3u_directory(iconimage)

elif mode == 12:
	thanh51_xml_m3u_channel(url, iconimage)

elif mode == 13:
	thanh51_xml_m3u_index(url ,name, iconimage)

elif mode == 21:  
	atf01_m3u(url, iconimage)  

elif mode == 31:
	my_playlist_directories(name, iconimage)

elif mode == 32:
	my_playlist_links(name, iconimage)  

elif mode == 33:  
	playlist_channel(url, name, iconimage)  

elif mode == 101:
	index(url, iconimage) 

elif mode == 111:
	tvtonghop_anluong(name, url, iconimage) 

elif mode == 121: 
	tvreplay_link(url, iconimage)  

elif mode == 201:  
	play_my_playlists(url)

elif mode == 202:
	resolve_url(url)  

elif mode == 203:  
	play_tvtonghop(url) 

xbmcplugin.endOfDirectory(int(sys.argv[1]))

