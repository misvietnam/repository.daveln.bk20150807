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

mysettings = xbmcaddon.Addon(id = 'plugin.video.netmedia')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
logos = xbmc.translatePath(os.path.join(home, 'logos\\'))
home_menu = xbmc.translatePath(os.path.join(home, 'menulist.xml'))
prog_menu = xbmc.translatePath(os.path.join(home, 'ProgMenu.xml'))
prog_link = 'https://raw.githubusercontent.com/daveln/repository.daveln/master/playlists/ProgMenu.xml'
home_link = 'https://raw.githubusercontent.com/daveln/repository.daveln/master/playlists/menulist.xml'
dict = {'&amp;':'&', '&quot;':'"', '.':' ', '&#39':'\'', '&#038;':'&', '&#039':'\'', '&#8211;':'-', '&#8220;':'"', '&#8221;':'"', '&#8230':'...'}

if not os.path.exists(home_menu):
	try:
		open(home_menu, 'w').close()
	except:
		pass  	
	
status = urllib.urlopen(home_link).getcode()
if status == 200:
	urllib.urlretrieve (home_link, home_menu)
else:
	pass
	
if not os.path.exists(prog_menu):
	try:
		open(prog_menu, 'w').close()
	except:
		pass  	
	
status = urllib.urlopen(prog_link).getcode()
if status == 200:
	urllib.urlretrieve (prog_link, prog_menu)
else:
	pass	

def menu_list():
	try:
		mainmenu = open(home_menu, 'r')  
		link = mainmenu.read()
		mainmenu.close()
		match = re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(link)
		return match
	except:
		pass	
		
def replace_all(text, dict):
	try:
		for a, b in dict.iteritems():
			text = text.replace(a, b)
		return text
	except:
		pass	
        
def make_request(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		response = urllib2.urlopen(req, timeout = 60)
		link = response.read()
		response.close()  
		return link
	except urllib2.URLError, e:
		print 'We failed to open "%s".' % url
		if hasattr(e, 'code'):
			print 'We failed with error code - %s.' % e.code	
		elif hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason
			
def home():
	add_dir('[COLOR cyan]. .[COLOR red]  ^  [COLOR cyan]. .[COLOR yellow]  Home  [COLOR cyan]. .[COLOR red]  ^  [COLOR cyan]. .[/COLOR]', '', None, icon)
		
def main():
	for title, url, thumb in menu_list():
		if 'Main Menu - ' in title:  
			add_dir(title.replace('Main Menu - ', ''), url, 2, logos + thumb)
		elif 'Main Menu Plus - ' in title:  
			add_dir(title.replace('Main Menu Plus - ', ''), url, 1, logos + thumb)	
		elif 'Main Menu learn_kodi - ' in title:  
			add_dir(title.replace('Main Menu learn_kodi - ', ''), url, 8, logos + thumb)			
		else:
			pass

def learn_kodi():
	home()
	myxml = open(prog_menu, 'r')  
	link = myxml.read()
	myxml.close()
	if '<channel>' in link:
		match = re.compile('<channel>\s*<name>(.+?)</name>').findall(link)
		for channel_name in match:
			add_dir(channel_name, 'progmenu', 9, iconimage)
	else:
		match = re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.*?)</thumbnail>").findall(link)
		for title, url, thumb in match:
			if len(thumb) > 0:
				add_link(title, url, 4, thumb) 
			else:	
				add_link(title, url, 4, iconimage) 		

def play_tutorial(name):
	home()
	myxml = open(prog_menu, 'r')  
	link = myxml.read()
	myxml.close()
	match = re.compile('<channel>\s*<name>' + name + '</name>((?s).+?)</channel>').findall(link)	
	for vlink in match:
		final_link = re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.*?)</thumbnail>").findall(vlink)
		for title, url, thumb in final_link:
			if len(thumb) <= 0:
				add_link(title, url, 4, iconimage)
			else:
				add_link(title, url, 4, thumb)	

def directory():
	home()
	add_dir('Tin Tức & TV Hải Ngoại', url, 2, logos + 'haingoai.png')
	add_dir('Tin Tức & TV Trong Nước', url, 2, logos + 'vietnam.png')
		
def category(url):
	home()
	for title, url, thumb in menu_list():
		if 'Tôn Giáo' in name and 'Religion - ' in title:
			add_dir(title.replace('Religion - ', ''), url, 3, logos + thumb)
		elif "thanh51's collection" in name and 'thanh51 - ' in title:
			add_dir(title.replace('thanh51 - ', ''), url, 3, logos + thumb)		
		if 'Tin Tức & TV Hải Ngoại' in name and 'OverseaNews - ' in title:	
			add_dir(title.replace('OverseaNews - ', ''), url, 3, logos + thumb)
		elif 'Tin Tức & TV Trong Nước' in name and 'NewsInVN - ' in title:	
			add_dir(title.replace('NewsInVN - ', ''), url, 3, logos + thumb)      
		elif 'Thiếu Nhi' in name and 'Children - ' in title:	
			add_dir(title.replace('Children - ', ''), url, 3, logos + thumb)
		elif 'Ca Nhạc' in name and 'Music - ' in title:	
			add_dir(title.replace('Music - ', ''), url, 3, logos + thumb)
		elif 'Hát Karaoke' in name and 'Karaoke - ' in title:	
			add_dir(title.replace('Karaoke - ', ''), url, 3, logos + thumb)
		elif 'Cải Lương' in name:
			if 'CailuongTV - ' in title:
				add_link(title.replace('CailuongTV - ', ''), url, 4, logos + thumb)
			elif 'Cailuong - ' in title:	
				add_dir(title.replace('Cailuong - ', ''), url, 3, logos + thumb)      
		elif 'Hài Kịch' in name and 'Sitcom - ' in title:	
			add_dir(title.replace('Sitcom - ', ''), url, 3, logos + thumb)
		elif 'Talk Shows' in name and 'TalkShows - ' in title:	
			add_dir(title.replace('TalkShows - ', ''), url, 3, logos + thumb)      
		elif 'TV Shows' in name and 'TiviShows - ' in title:	
			add_dir(title.replace('TiviShows - ', ''), url, 3, logos + thumb)
		elif 'Thể Thao' in name and 'Sports - ' in title:	
			add_dir(title.replace('Sports - ', ''), url ,3, logos + thumb)
		elif 'Du Lịch' in name and 'Travel - ' in title:	
			add_dir(title.replace('Travel - ', ''), url, 3, logos + thumb)
		elif 'Y Khoa' in name:
			if 'Medical - ' in title:	
				add_dir(title.replace('Medical - ', ''), url, 3, logos + thumb)
			elif 'Y Tế NguoiVietTV - ' in title:
				add_dir(title.replace('Y Tế NguoiVietTV - ', ''), url, 5, logos + thumb)         
			elif 'Y Tế Đồng Nai' in title:
				add_dir(title.replace('Y Tế Đồng Nai - ', ''), url, 5, logos + thumb)        
		elif 'Ẩm Thực Tình Yêu' in name and 'Cooking - ' in title:	
			add_dir(title.replace('Cooking - ', ''), url, 3, logos + thumb)     
		elif 'Trang Điểm' in name and 'MakeUp - ' in title:	
			add_dir(title.replace('MakeUp - ', ''), url, 3, logos + thumb)	
		elif 'Đọc Truyện' in name and 'AudioBook - ' in title:	
			add_dir(title.replace('AudioBook - ', ''), url, 3, logos + thumb)
		elif 'Di trú và Nhập Tịch Hoa Kỳ' in name and 'Immigration - ' in title:	
			add_dir(title.replace('Immigration - ', ''), url, 3, logos + thumb)
		elif 'America\'s Funniest Videos' in name and 'AFV - ' in title:	
			add_dir(title.replace('AFV - ', ''), url, 3, logos + thumb)
		elif 'Dicovery Channels & Animal Planet' in name and 'DCAP - ' in title:	
			add_dir(title.replace('DCAP - ', ''), url, 3, logos + thumb)    
		elif 'Những Mục Khác' in name and 'Other - ' in title:	
			add_dir(title.replace('Other - ', ''), url, 3, logos + thumb)  

def medical_site(url):
	home()
	content = make_request(url)
	if 'www.dnrtv.org.vn' in url:
		match = re.compile("img src=\"([^\"]+)\" \/><\/a>\s*<a href=\"([^\"]*)\" class=\"title\">(.+?)<").findall(content)
		for thumb, url, name in match:	
			add_link(name, url, 4, thumb)
		match = re.compile('class=\'paging_normal\' href=\'([^\']*)\'>Trang đầu<').findall(content)
		for url in match:	
			add_dir('[COLOR violet]Trang đầu[/COLOR]', url, 5, logos + 'dongnai.png')    
		match = re.compile('class=\'paging_normal\' href=\'([^\']+)\'>(\d+)<').findall(content)
		for url, name in match:	
			add_dir('[COLOR lime]Trang ' + name + '[/COLOR]', url, 5, logos + 'dongnai.png')	
		match = re.compile('class=\'paging_normal\' href=\'([^\']*)\'>Trang cuối<').findall(content)
		for url in match:	
			add_dir('[COLOR red]Trang cuối[/COLOR]', url, 5, logos + 'dongnai.png')	
	elif 'nguoiviettv' in url:
		match = re.compile('title="([^"]*)" href="([^"]+)">\s*<span class="clip">\s*<img src="(.+?)"').findall(content)[15:-6]
		for name, url, thumb in match:
			name = replace_all(name, dict)  
			add_link(name, url, 4, thumb)   
		match = re.compile("href='([^']*)' class='.+?'>(\d+)<").findall(content)
		for url, name in match:	
			add_dir('[COLOR yellow]Trang ' + name + '[/COLOR]', url.replace('&#038;','&'), 5, logos + 'bacsi.png')
      
def media_list(url):
	home()
	if 'youtube' in url:
		try:
			url1 = url.split('?')[0].replace('/uploads', '/playlists')
			content1 = make_request(url1)
			match1 = re.compile("<title type='text'>(?!Playlists of)(.+?)</title>.+?href='http://www\.youtube\.com/playlist\?list=.+?'").findall(content1)[0]
			for name in match1[0]:		
				if name > 0:
					add_dir('[COLOR magenta]+ + + +[COLOR cyan]  Playlists  [COLOR magenta]+ + + +[/COLOR]', url1 + '?start-index=1&max-results=25', 6, iconimage)		
		except:
			pass			
		content = make_request(url)
		match = re.compile("player url='(.+?)\&.+?><media.+?url='(.+?)' height=.+?'plain'>(.+?)<\/media").findall(content)
		for url, thumb, name in match:
			name = replace_all(name, dict)
			url = url.replace('http://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/play/?video_id=') #new
			#url = url.replace('http://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/?action=play_video&videoid=')  #old
			#url = url.replace('http://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=') #old     
			add_link(name, url, 4, thumb)
		match = re.compile("<link rel='next' type='application\/atom\+xml' href='(.+?)'").findall(content)
		for url in match:	      
			add_dir('[COLOR cyan]Trang kế  [COLOR cyan]>[COLOR magenta]>[COLOR orange]>[COLOR yellow]>[/COLOR]', url.replace('&amp;', '&'), 3, icon)		  
	elif 'dailymotion' in url:
		try:
			url1 = url.replace('/rss/', '/playlists/')
			content1 = make_request(url1)
			match1 = re.compile('href=".+?" class="link" title="(.+?)"').findall(content1)[0]
			for name in match1[0]:		
				if name > 0 and '/1' in url:
					add_dir('[COLOR magenta]+ + + +[COLOR lime]  Playlists  [COLOR magenta]+ + + +[/COLOR]', url1, 6, iconimage)	
		except:
			pass
		content = make_request(url)		
		match = re.compile('<title>(.+?)<\/title>\s*<link>(.+?)_.+?<\/link>\s*<description>.+?src="(.+?)"').findall(content)
		for name, url, thumb in match:
			name = replace_all(name, dict)    
			url = url.replace('http://www.dailymotion.com/video/', 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=')	  
			add_link(name, url, 4, thumb)
		match = re.compile('<dm:link rel="next" href="(.+?)"').findall(content)
		for url in match:  
			add_dir('[COLOR lime]Trang kế  [COLOR cyan]>[COLOR magenta]>[COLOR orange]>[COLOR yellow]>[/COLOR]', url, 3, icon)	

def TubeMotion_playlist(url):
	home()
	content = make_request(url)
	if 'youtube' in url:
		try:
			content = content.encode('utf-8')
		except: 
			pass
		content = ''.join(content.splitlines()).replace('\t','')	
		match = re.compile("<title type='text'>(?!Playlists of)(.+?)</title>.+?href='http://www\.youtube\.com/playlist\?list=(.+?)'").findall(content)
		for name, url in match:
			name = replace_all(name, dict)
			add_dir(name, 'http://gdata.youtube.com/feeds/api/playlists/' + url + '?max-results=50&start-index=1', 7, iconimage)
		match = re.compile("<link rel='next' type='application\/atom\+xml' href='(.+?)'").findall(content)
		for url in match:	      
			add_dir('[COLOR cyan]Next playlist  [COLOR cyan]>[COLOR magenta]>[COLOR orange]>[COLOR yellow]>[/COLOR]', url.replace('&amp;', '&'), 6, icon)		  			
	elif 'dailymotion' in url:
		match = re.compile('href="(.+?)" class="link" title="(.+?)"').findall(content)
		for url, name in match:
			name = replace_all(name, dict)
			add_dir(name, 'http://www.dailymotion.com/rss' + url, 7, iconimage)
		for url, name in match:  
			add_dir("[COLOR lime]Playlists  [COLOR cyan]>[COLOR magenta]>[COLOR orange]>[COLOR yellow]>  [COLOR lime]Page " + name + "[/COLOR]" , "http://www.dailymotion.com" + url, 6, icon)

def TubeMotion_playlist_medialist(url):
	home()
	content = make_request(url)
	if 'youtube' in url:
		match = re.compile("player url='(.+?)\&.+?><media.+?url='(.+?)' height=.+?'plain'>(.+?)<\/media").findall(content)
		for url, thumb, name in match:
			name = replace_all(name, dict)
			url = url.replace('http://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/play/?video_id=')
			add_link(name, url, 4, thumb)
		match = re.compile("<link rel='next' type='application\/atom\+xml' href='(.+?)'").findall(content)
		for url in match:	      
			add_dir('[COLOR cyan]Playlists  [COLOR cyan]>[COLOR magenta]>[COLOR orange]>[COLOR yellow]>  [COLOR cyan]Next page[/COLOR]', url.replace('&amp;', '&'), 7, icon)		  
	elif 'dailymotion' in url:
		match = re.compile('<title>(.+?)<\/title>\s*<link>(.+?)_.+?<\/link>\s*<description>.+?src="(.+?)"').findall(content)
		for name, url, thumb in match:
			name = replace_all(name, dict)    
			url = url.replace('http://www.dailymotion.com/video/', 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=')	  
			add_link(name, url, 4, thumb)
		match = re.compile('<dm:link rel="next" href="(.+?)"').findall(content)
		for url in match:  
			add_dir('[COLOR lime]Playlists  [COLOR cyan]>[COLOR magenta]>[COLOR orange]>[COLOR yellow]>  [COLOR lime]Next page[/COLOR]', url, 7, icon)	
		
def resolve_url(url):
	content = make_request(url)
	if 'www.dnrtv.org.vn' in url:		
		mediaUrl = re.compile("url: '(.+?)mp4'").findall(content)[0] + 'mp4'
	elif 'nguoiviettv' in url:
		mediaUrl = 'plugin://plugin.video.youtube/play/?video_id=' + re.compile('src="http://www\.youtube\.com/embed/(.+?)\?').findall(content)[0]        
	else:  
		mediaUrl = url	
	item = xbmcgui.ListItem(name, path = mediaUrl)
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
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)	
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
	main()
  
elif mode == 1: 
	directory()  
  
elif mode == 2:
	category(url)  

elif mode == 3:
	media_list(url)
   
elif mode == 4:
	resolve_url(url)

elif mode == 5:
	medical_site(url)  

elif mode == 6:	
	TubeMotion_playlist(url)
	
elif mode == 7:
	TubeMotion_playlist_medialist(url)
	
elif mode == 8:	
	learn_kodi()

elif mode == 9:	
	play_tutorial(name)
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))

