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

mysettings = xbmcaddon.Addon(id = 'plugin.video.netmovie')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
logos = xbmc.translatePath(os.path.join(home, 'resources', 'logos\\'))
anhtrang = 'http://phim.anhtrang.org/'
m_anhtrang = 'http://m.anhtrang.org/'
dangcapmovie = 'http://dangcapmovie.com/'
dchd = 'http://dangcaphd.com/'
phim3s = 'http://phim3s.net/'
megaboxvn = 'http://megabox.vn/'
phimb = 'http://www.phimb.net'
phim14 = 'http://phim14.net/'
phim7 = 'http://phim7.com'

def make_request(url):
	if 'phimb' in url:
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
			if hasattr(e, 'reason'):
				print 'We failed to reach a server.'
				print 'Reason: ', e.reason	
	else:
		try:
			req = urllib2.Request(url)
			req.add_header('User-Agent', 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
			req.add_header ('Cookie', 'window.location.href') 
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

def home():
	add_dir('[COLOR cyan]. .[COLOR red]  ^  [COLOR cyan]. .[COLOR yellow]  Home  [COLOR cyan]. .[COLOR red]  ^  [COLOR cyan]. .[/COLOR]', '', None, icon, fanart)
				
def main():
	add_dir('[COLOR yellow]phim3s.net[/COLOR]', phim3s, 2, logos + 'phim3s.png', fanart) 
	add_dir('[COLOR magenta]phim14.net[/COLOR]', phim14, 2, logos + 'phim14.png', fanart)   
	add_dir('[COLOR lime]phim7.com[/COLOR]', phim7, 2, logos + 'phim7.png', fanart)
	add_dir('[COLOR cyan]phimb.net[/COLOR]', phimb, 2, logos + 'phimb.png', fanart)    
	add_dir('[COLOR orange]anhtrang.org[/COLOR]', anhtrang, 2, logos + 'anhtrang.png', fanart)  
	add_dir('[COLOR violet]megabox.vn[/COLOR]', megaboxvn, 2, logos + 'megabox.png', fanart)  
	add_dir('[COLOR lime]dangcaphd.com[/COLOR]', dchd, 2, logos + 'dchd.png', fanart) 
	add_dir('[COLOR blue]dangcapmovie.com[/COLOR]', dangcapmovie, 2, logos + 'dcm.png', fanart)  

def search():
	try:
		keyb = xbmc.Keyboard('', '[COLOR yellow]Enter search text[/COLOR]')
		keyb.doModal()
		if (keyb.isConfirmed()):
			searchText = urllib.quote_plus(keyb.getText())
		if 'phim3s' in name:  
			url = phim3s + 'search?keyword=' + searchText
			media_list(url)
		elif 'dangcaphd' in name:
			url = dchd + 'movie/search.html?key=' + searchText + '&search_movie=0'
			media_list(url)
		elif 'anhtrang' in name:		
			url = anhtrang + 'tim-kiem=' + searchText + '.html'  
			media_list(url)
		elif 'megabox' in name:	
			url = megaboxvn + 'home/search/index/key/' + searchText.replace('+', '%20')	
			megabox_list_eps(url)
			other_megabox_list(url)
		elif 'dangcapmovie' in name:      
			url = dangcapmovie + 'movie/search.html?key=' + searchText
			search_result(url)
		elif 'phim7' in name:      
			url = phim7 + '/tim-kiem/tat-ca/' + searchText.replace('+', '-') + '.html'
			media_list(url)
		elif 'phimb' in name: 
			url = phimb + '/tim-kiem/' + searchText
			media_list(url)	
		elif 'phim14' in name: 
			url = phim14 + 'search/' + searchText.replace('+', '-') + '.html'
			media_list(url)	
	except: 
		pass

def search_result(url):
	content = make_request(url)
	if 'dangcapmovie' in url:
		match = re.compile('href="(.+?)" title="(.+?)" data-tooltip=".+?">\s*<img src="(.+?)"').findall(content)
		for url, name, thumb in match:
			url = url.replace('/movie-', '/watch-')
			add_dir('[COLOR lime]' + name  + '[/COLOR]', url.replace('/movie-', '/watch-'), 5, thumb, fanart)
 		
def category(url):
	home()
	content = make_request(url)
	if 'phim3s' in url:
		add_dir('[COLOR yellow]phim3s[B]   [COLOR lime]>[COLOR orange]>[COLOR blue]>[COLOR magenta]>   [/B][COLOR yellow]Tìm Phim[/COLOR]', phim3s, 1, logos + 'phim3s.png', fanart)
		match = re.compile("<a href=\"the-loai([^\"]*)\" title=\"([^\"]+)\">.+?<\/a>").findall(content) 
		for url, name in match:
			add_dir('[COLOR cyan]' + name + '[/COLOR]', ('%sthe-loai%s' % (phim3s, url)), 3, logos + 'phim3s.png', fanart)					
		match = re.compile("<a href=\"quoc-gia([^\"]*)\" title=\"([^\"]+)\">.+?<\/a>").findall(content) 
		for url, name in match:
			add_dir('[COLOR lime]' + name + '[/COLOR]', ('%squoc-gia%s' % (phim3s, url)), 3, logos + 'phim3s.png', fanart)					
		match = re.compile("<a href=\"danh-sach([^\"]*)\" title=\"([^\"]+)\">.+?<\/a>").findall(content) 
		for url, name in match:
			add_dir('[COLOR lightblue]' + name + '[/COLOR]', ('%sdanh-sach%s' % (phim3s, url)), 3, logos + 'phim3s.png', fanart)
	elif 'phim14' in url:
		add_dir('[COLOR lime]phim14.net[B]   [COLOR lime]>[COLOR orange]>[COLOR blue]>[COLOR magenta]>   [/B][COLOR lime]Tìm Phim[/COLOR]', phim14, 1, logos + 'phim14.png', fanart)
		match = re.compile('href="http://phim14.net/the-loai([^"]*)">(.+?)<').findall(content)[0:15]
		for url, name in match:	
			add_dir('[COLOR yellow]' + name + '[/COLOR]', phim14 + 'the-loai' + url, 3, logos + 'phim14.png', fanart)
		match = re.compile('href="http://phim14.net/quoc-gia(.+?)">(.+?)<').findall(content)[0:11]
		for url, name in match:  
			add_dir('[COLOR cyan]' + name + '[/COLOR]', phim14 + 'quoc-gia' + url, 3, logos + 'phim14.png', fanart)	
		match = re.compile('href="http://phim14.net/danh-sach([^"]*)".*>(.+?)<').findall(content)[0:5]
		for url, name in match:  
			add_dir('[COLOR violet]' + name + '[/COLOR]', phim14 + 'danh-sach' + url, 3, logos + 'phim14.png', fanart)
	elif 'phim7' in url:
		add_dir('[COLOR lime]phim7.com[B]   [COLOR lime]>[COLOR orange]>[COLOR blue]>[COLOR magenta]>   [/B][COLOR yellow]Tìm Phim[/COLOR]', phim7, 1, logos + 'phim7.png', fanart)
		match = re.compile("href='(.+?)' title='(.+?)'>").findall(content)[0:25]
		for url, name in match:	
			add_dir('[COLOR cyan]' + name + '[/COLOR]', phim7 + url, 3, logos + 'phim7.png', fanart)	
		add_dir('[COLOR lime]Video mới[/COLOR]', 'http://phim7.com/video-moi.html', 3, logos + 'phim7.png', fanart)
		add_dir('[COLOR lime]Video clip hay[/COLOR]', 'http://phim7.com/video.html', 3, logos + 'phim7.png', fanart)  
		match = re.compile('href="(.+?)" title="(.+?)">').findall(content)[1:27]
		for url, name in match:
			if 'video clip hay' in name:
				pass	
			else:  
				add_dir('[COLOR yellow]' + name + '[/COLOR]', phim7 + url, 3, logos + 'phim7.png', fanart)
	elif 'phimb' in url:			
		add_dir('[COLOR lime]phimb.net[B]   [COLOR lime]>[COLOR orange]>[COLOR blue]>[COLOR magenta]>   [/B][COLOR lime]Tìm Phim[/COLOR]', phimb, 1, logos + 'phimb.png', fanart)
		match = re.compile('class="add" href="(.+?)" title="(.+?)"').findall(content)
		for url, name in match:  
			add_dir('[COLOR yellow]' + name + '[/COLOR]', phimb + url, 3, logos + 'phimb.png', fanart)
		match = re.compile('title="Phim(.+?)" href="(.+?)"').findall(content)
		for name, url in match:	
			add_dir('[COLOR cyan]' + name + '[/COLOR]', url, 3, logos + 'phimb.png', fanart)	
	elif 'anhtrang' in url:  
		add_dir('[COLOR yellow]anhtrang[B]   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [/B][COLOR yellow]Tìm Phim[/COLOR]', anhtrang, 1, logos + 'anhtrang.png', fanart)
		match = re.compile("<a class=\"link\" href=\"http:\/\/.+?\/([^\"]*)\" >\s*<span>(.+?)<\/span>").findall(content)
		for url, name in match:
			add_dir('[COLOR lime]' + name + '[/COLOR]', anhtrang + url, 3, logos + 'anhtrang.png', fanart)  
		match = re.compile("<a class=\"link\" href=\"http:\/\/.+?\/([^\"]+)\">\s*<span>(.+?)<\/span>").findall(content)[0:7]
		for url, name in match:
			add_dir('[COLOR cyan]' + name + '[/COLOR]', anhtrang + url, 3, logos + 'anhtrang.png', fanart)
		match = re.compile("<a class=\"link\" href=\"http:\/\/.+?\/([^\"]+)\">\s*<span>(.+?)<\/span>").findall(content)[7:19]
		for url, name in match:
			add_dir('[COLOR orange]' + name + '[/COLOR]', anhtrang + url, 3, logos + 'anhtrang.png', fanart)	
		match = re.compile('<li class="item27">\s*<a class="topdaddy link" href="http:\/\/.+?\/([^"]*)">\s*<span>(.+?)<\/span>').findall(content)
		for url, name in match:
			add_dir('[COLOR magenta]' + name + '[/COLOR]', anhtrang + url, 3, logos + 'anhtrang.png', fanart) 
		match = re.compile('<li class="item28">\s*<a class="topdaddy link" href="http:\/\/.+?\/(.+?)">\s*<span>(.+?)<\/span>').findall(content)
		for url, name in match:
			add_dir('[COLOR lightblue]' + name + '[/COLOR]', anhtrang + url, 3, logos + 'anhtrang.png', fanart) 
	elif 'megabox' in url:  
		add_dir('[COLOR cyan]megabox[B]   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [/B][COLOR cyan]Tìm Phim[/COLOR]', megaboxvn, 1, logos + 'megabox.png', fanart)
		match = re.compile("href=\"tvonline\/(.+?)\">([^>]*)<").findall(content)[:3]  
		for url, name in match: 
			if 'the-loai' in url:  
				add_dir('[COLOR yellow]TV - ' + name + '[/COLOR]', ('%stvonline/%s' % (megaboxvn, url)), 3, logos + 'megabox.png', fanart)
			else:	  
				add_dir('[COLOR yellow]TV - ' + name + '[/COLOR]', ('%stvonline/%s' % (megaboxvn, url)), 10, logos + 'megabox.png', fanart)
		add_dir('[COLOR lime]Phim Lẻ - Mới Nhất[/COLOR]', megaboxvn + 'phim-le/moi-nhat.html', 11, logos + 'megabox.png', fanart)	  
		match = re.compile("href=\"phim-le\/(.+?)\">([^>]*)<").findall(content)[:3] 
		for url, name in match: 
			if 'the-loai' in url:  
				add_dir('[COLOR lime]Phim Lẻ - ' + name + '[/COLOR]', megaboxvn + 'phim-le/' + url, 3, logos + 'megabox.png', fanart)
			else:
				add_dir('[COLOR lime]Phim Lẻ - ' + name.replace('Phim ', '') + '[/COLOR]', megaboxvn + 'phim-le/' + url, 11, logos + 'megabox.png', fanart)	  
		add_dir('[COLOR lime]Phim Lẻ - Dành Cho Bạn[/COLOR]', megaboxvn + 'for_you_movies.html', 11, logos + 'megabox.png', fanart)
		add_dir('[COLOR yellow]Phim Bộ - Mới Nhất[/COLOR]', megaboxvn + 'phim-bo/moi-nhat.html', 10, logos + 'megabox.png', fanart)  
		match = re.compile("href=\"phim-bo\/(.+?)\">([^>]*)<").findall(content)[:4] 
		for url, name in match:
			if 'the-loai' in url:  
				add_dir('[COLOR yellow]Phim Bộ - ' + name + '[/COLOR]', ('%sphim-bo/%s' % (megaboxvn, url)), 11, logos + 'megabox.png', fanart)	
			else:
				add_dir('[COLOR yellow]Phim Bộ - ' + name + '[/COLOR]', ('%sphim-bo/%s' % (megaboxvn, url)), 10, logos + 'megabox.png', fanart)		
		match = re.compile("href=\"video-clip\/(.+?)\">([^>]*)<").findall(content)[1:5]
		for url, name in match:  
			add_dir('[COLOR lime]Videos - ' + name + '[/COLOR]', megaboxvn + 'video-clip/' + url, 11, logos + 'megabox.png', fanart)				
	elif 'dangcaphd' in url:
		add_dir('[COLOR yellow]dangcaphd[B]   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR lightgreen]>   [/B][COLOR yellow]Tìm Phim[/COLOR]', dchd + '', 1, logos + 'dchd.png', fanart)
		match = re.compile("<a href=\"([^\"]*)\" class='menutop' title='([^']+)'>").findall(content)
		for url, name in match:
			add_dir('[COLOR lime]' + name + '[/COLOR]', url, 3, logos + 'dchd.png', fanart)  
		match = re.compile("<li><a href=\"http:\/\/dangcaphd.com\/cat(.+?)\" title=\"([^\"]*)\">").findall(content)[0:22]
		for url, name in match:
			add_dir('[COLOR cyan]' + name + '[/COLOR]', dchd + 'cat' + url, 3, logos + 'dchd.png', fanart)
		match = re.compile("<li><a href=\"http:\/\/dangcaphd.com\/country(.+?)\" title=\"([^\"]+)\">").findall(content)[0:12]
		for url, name in match:
			add_dir('[COLOR orange]' + name + '[/COLOR]', dchd + 'country' + url, 3, logos + 'dchd.png', fanart)
		match = re.compile("<a href=\"http:\/\/dangcaphd.com\/movie(.+?)\"><span>(.*?)<\/span><\/a>").findall(content)[0:3]
		for url, name in match:
			add_dir('[COLOR lightgreen]' + name + '[/COLOR]', dchd + 'movie' + url, 3, logos + 'dchd.png', fanart)					
	elif 'dangcapmovie' in url:
		add_dir('[COLOR lime]dangcapmovie.com   [COLOR lime]>[COLOR cyan]>[COLOR orange]>[COLOR magenta]>   [COLOR lime]Movie Search[/COLOR]', dangcapmovie, 1, logos + 'dcm.png', fanart)
		match = re.compile('href="http:\/\/dangcapmovie.com\/cat(.+?)" title="(.+?)">').findall(content)[0:23] 
		for url, name in match:
			add_dir('[COLOR cyan]' + name.replace('Hàng động', 'Hành động') + '[/COLOR]', dangcapmovie + 'cat' + url, 3, logos + 'dcm.png', fanart)      
		match = re.compile('href="http:\/\/dangcapmovie.com\/country(.+?)" title="(.+?)">').findall(content)[0:10]
		for url, name in match:  
			add_dir('[COLOR yellow]' + name + '[/COLOR]', dangcapmovie + 'country' + url, 3, logos + 'dcm.png', fanart) 
		match = re.compile('href="http:\/\/dangcapmovie.com\/movie\/(.+?)" title="(.+?)">').findall(content)
		for url, name in match:  
			add_dir('[COLOR lime]' + name + '[/COLOR]', dangcapmovie + 'movie/' + url, 3, logos + 'dcm.png', fanart) 

def media_list(url):
	home()
	content = make_request(url)
	if 'phim3s' in url:
		match = re.compile("<div class=\"inner\"><a href=\"(.*?)\" title=\"([^\"]*)\"><img src=\"(.+?)\"").findall(content)
		for url, name, thumb in match:
			add_dir('[COLOR yellow]' + name + '[/COLOR]', ('%s%sxem-phim' % (phim3s, url)), 5, thumb, fanart)					
		match = re.compile("<span class=\"item\"><a href=\"([^\"]*)\">(\d+)<\/a><\/span>").findall(content)
		for url, name in match:
			add_dir('[COLOR lime]Trang ' + name + '[/COLOR]', ('%s%s' % (phim3s, url)), 3, logos + 'phim3s.png', fanart)
	elif 'phim14' in url:	  
		match = re.compile('href="(.+?)" title="(.+?)"><img src="(.+?)"').findall(content)
		for url, name, thumb in match:
			add_dir('[COLOR yellow]' + name + '[/COLOR]', url.replace('/phim/', '/xem-phim/'), 4, thumb, fanart)
		match = re.compile('<span class="item"><a href="(.+?)">(\d+)<').findall(content)
		for url, pageNum in match:
			add_dir('[COLOR lime]Trang ' + pageNum + '[/COLOR]', url, 3, logos + 'phim14.png', fanart)
	elif 'phim7' in url:
		match = re.compile('href="(.+?)" title="(.+?)"><span class="poster">\s*<img src=".+?" alt="" />\s*<img class=".+?" src=".+?" data-original="(.+?)"').findall(content)
		for url, name, thumb in match:
			if '/video/' in url:
				add_link('[COLOR lime]' + name + '[/COLOR]', phim7 + url, 99, thumb, fanart)
			else:
				add_dir('[COLOR yellow]' + name + '[/COLOR]', phim7 + url.replace('/phim/', '/xem-phim/'), 4, thumb, fanart)
		match = re.compile("href='(.+?)' >(\d+)<").findall(content)
		for url, page in match:
			add_dir('[COLOR lime]Page ' + page + '[/COLOR]', phim7 + url, 3, logos + 'phim7.png', fanart)
	elif 'phimb' in url:		
		match = re.compile('href="(.+?)" title="(.+?)"><img.+?src="(.+?)"').findall(content)
		for url, name, thumb in match:
			add_dir('[COLOR yellow]' + name + '[/COLOR]', url.replace('/phim/', '/xem-phim/'), 4, thumb, fanart)
		match = re.compile("title='Trang(.+?)' href='(.+?)'").findall(content)
		for page, url in match:
			if 'đầu' in page:
				add_dir('[COLOR cyan]Trang ' + page + '[/COLOR]', phimb + url, 3, logos + 'phimb.png', fanart)	
			elif 'cuối' in page:
				add_dir('[COLOR red]Trang ' + page + '[/COLOR]', phimb + url, 3, logos + 'phimb.png', fanart)	
			else:
				add_dir('[COLOR lime]Trang ' + page + '[/COLOR]', phimb + url, 3, logos + 'phimb.png', fanart) 
	elif 'anhtrang' in url:
		match = re.compile("<a href=\"([^\"]*)\" title=\"([^\"]+)\"><img src=\"(.+?)\"").findall(content)		
		for url, name, thumb in match:
			add_dir('[COLOR yellow]' + name + '[/COLOR]', url, 5, thumb, fanart)
		match = re.compile("<a class=\"pagelink\" href=\"(.+?)\">(.+?)<\/a>").findall(content)
		for url, name in match:	
			add_dir('[COLOR lime]Trang ' + name + '[COLOR cyan] >>>>[/COLOR]', url, 3, logos + 'anhtrang.png', fanart)
		match = re.compile("<a class=\"pagelast\" href=\"([^\"]*)\">(.+?)<\/a>").findall(content)
		for url, name in match:	
			add_dir('[COLOR red]Trang ' + name.replace('Cuối', '[COLOR red]Cuối[COLOR magenta] >>>>') + '[/COLOR]', url, 3, logos + 'anhtrang.png', fanart)	
	elif 'megabox' in url:
		if 'tvonline' in url:
			match = re.compile('<div class="infoC"> <a href="(.+?)" >\s*<h4>(.+?)<span>\((\d+)\)<\/span>').findall(content)
			for url, title, inum in match:
				if inum == '0':
					pass
				else:
					add_dir('[COLOR yellow]' + title + '[/COLOR]', url, 10, logos + 'megabox.png', fanart)
		elif 'phim-le' in url:
			match = re.compile('<div class="infoC"> <a href="(.+?)" >\s*<h4>(.+?)<span>\((\d+)\)<\/span>').findall(content)[6:]
			for url, title, inum in match:
				if inum == '0':
					pass
				else:
					add_dir('[COLOR lime]' + title + '[/COLOR]', url, 11, logos + 'megabox.png', fanart)  
		elif 'phim-bo' in url:
			match = re.compile('<div class="infoC"> <a href="(.+?)" >\s*<h4>(.+?)<span>\((\d+)\)<\/span>').findall(content)[5:]
			for url, title, inum in match:
				if inum == '0':
					pass
				else:
					add_dir('[COLOR yellow]' + title + '[/COLOR]', url, 10, logos + 'megabox.png', fanart)  	
	elif 'dangcaphd' in url:
		match = re.compile('<a href="(.+?)" title="(.+?)">\s*<img src="(.+?)"').findall(content)
		for url, name, thumb in match:
			if 'Trailer' in name:
				pass
			else:      
				add_link('[COLOR yellow]' + name + '[/COLOR]', (url.replace('movie', 'watch')), 99, thumb, fanart) 
		match = re.compile("<a href=\"([^\"]+)\">&lt;&lt;<\/a>").findall(content)
		for url in match:
			add_dir('[COLOR cyan]Trang Đầu[/COLOR]', url.replace('amp;', ''), 3, logos + 'dchd.png', fanart)
		match = re.compile("<a href=\"([^>]*)\">(\d+)<\/a>").findall(content)
		for url, name in match:
			add_dir('[COLOR lime]Trang ' + name + '[/COLOR]', url.replace('amp;', ''), 3, logos + 'dchd.png', fanart)
		match = re.compile("<a href=\"([^\"]*)\">&gt;&gt;<\/a>").findall(content)
		for url in match:
			add_dir('[COLOR red]Trang Cuối[/COLOR]', url.replace('amp;', ''), 3, logos + 'dchd.png', fanart)			
	elif 'dangcapmovie' in url:
		match = re.compile('href="(.+?)" title="(.+?)" data-tooltip=".+?">\s*<img src="(.+?)"').findall(content)
		for url, name, thumb in match:
			url = url.replace('/movie-', '/watch-')
			add_dir('[COLOR cyan]' + name  + '[/COLOR]', url.replace('/movie-', '/watch-'), 5, thumb, fanart)
		match = re.compile('href="([^"]*)">(\d+|&gt;&gt;|&lt;&lt;)<').findall(content)
		for url, name in match:
			url = url.replace('&amp;', '&')
			if '&lt;&lt;' in name:
				name = name.replace('&lt;&lt;', 'First')
				add_dir('[COLOR yellow]' + name + ' Page[/COLOR]', url, 3, logos + 'dcm.png', fanart)
			elif '&gt;&gt;' in name:
				name = name.replace('&gt;&gt;', 'Last')
				add_dir('[COLOR red]' + name + ' Page[/COLOR]', url, 3, logos + 'dcm.png', fanart)      
			else:
				add_dir('[COLOR lime]Page ' + name + '[/COLOR]', url, 3, logos + 'dcm.png', fanart)
	xbmc.executebuiltin('Container.SetViewMode(500)')
	
def server_list(url):
	home()
	content = make_request(url)
	if 'phim7' in url:
		match = re.compile('<p class=".+?"><b>(.+?)</b>').findall(content)
		for server_name in match:
			add_dir('[COLOR lime]' + server_name + '[/COLOR]', url, 5, iconimage, fanart)
	elif 'phim14' in url:	 
		match = re.compile('<strong><img src="http://phim14.net/res//images/flag/vn.png"/>(.+?)</strong>').findall(content) #duplicate servers' name
		for server_name in match:
			if 'Download' in server_name:
				pass
			else:
				add_dir('[COLOR lime]' + server_name + '[/COLOR]', url, 5, iconimage, fanart)
	elif 'phimb' in url:
		match = re.compile('<div class="svname">(.+?)<\/div>').findall(content)
		for server_name in match:
			add_dir('[COLOR lime]' + server_name + '[/COLOR]', url, 5, iconimage, fanart)	
 				
def episode(name, url):
	home()
	content = make_request(url)
	if 'phim3s' in url:
		thumb = re.compile("<meta property=\"og:image\" content=\"([^\"]*)\"").findall(content)[0]		
		match = re.compile("data-type=\"watch\" data-episode-id.+?href=\"([^\"]*)\" title=\"(.*?)\"").findall(content)
		for url, title in match:
			add_link(('%s   -   %s' % ('[COLOR lime]' + title + '[/COLOR]', name )), ('%s%svideo.mp4' % (phim3s, url)), 99, thumb, fanart)	
	elif 'phim14' in url:
		name = name.replace('[COLOR lime]', '').replace('[/COLOR]', '')
		match = re.compile('<strong><img src=".+?"/>' + name + '</strong>\s*<ul((?s).+?)</ul>').findall(content)  
		for vlinks in match:
			match = re.compile('href="(.+?)" episode-type=".+?" title="(.+?)">(.+?)<').findall(vlinks)
			for url, title, eps in match:
				add_link('[COLOR cyan]' + title + '[/COLOR]', url, 99, iconimage, fanart)	
	elif 'phim7' in url: 
		name = name.replace('[COLOR lime]', '').replace('[/COLOR]', '')
		match = re.compile('<p class=".+?"><b>' + name + '</b>((?s).+?)</p>').findall(content)
		for vlinks in match:
			match = re.compile('href="(.+?)" title="(.+?)" class=".+?">(.+?)<').findall(vlinks)
			for url, title, eps in match:
				add_link('[COLOR cyan]' + eps + '[/COLOR]', phim7 + url, 99, iconimage, fanart)	
	elif 'phimb' in url:
		name = name.replace('[COLOR lime]', '').replace('[/COLOR]', '')  
		match = re.compile('<div class="svname">' + name + '</div><div class="svep"><div class="border">(.+?)</div>').findall(content)
		for vlinks in match:
			match = re.compile('href="(.+?)"  title="(.+?)">(.+?)<').findall(vlinks)
			for url, title, eps in match:
				add_link('[COLOR cyan]' + eps + '[/COLOR]', url, 99, iconimage, fanart)
	elif 'anhtrang' in url:
		thumb = re.compile('meta property="og:image" content="(.+?)"').findall(content)[0]
		newurl = url.replace(anhtrang, m_anhtrang)
		content = make_request(newurl)  
		add_link('[COLOR lime]Tập 1' + '[COLOR cyan][B]  -  [/B][/COLOR]' + name, newurl, 99, thumb, fanart)
		match = re.compile('<a href="(.+?)" class="ep">(.+?)<\/a>').findall(content)
		for url, title in match:
			add_link('[COLOR lime]Tập ' + title + '[COLOR cyan][B]  -  [/B][/COLOR]' + name, url, 99, thumb, fanart)   				
	elif 'megabox' in url:
		thumb = re.compile ('<link rel="image_src" href="(.+?)"').findall(content)[-1]
		match = re.compile('<option selected="selected"  value="(.+?)">(.+?)<\/option>').findall(content)
		for url, title in match:
			add_link('[COLOR cyan]' + title + '[COLOR magenta] - ' + name + '[/COLOR]', megaboxvn + url, 99, thumb + '?.jpg', fanart)     
		match = re.compile('<option  value="(.+?)">(.+?)<\/option>').findall(content)
		for url, title in match:
			add_link('[COLOR cyan]' + title + '[COLOR magenta] - ' + name + '[/COLOR]', megaboxvn + url, 99, thumb + '?.jpg', fanart) 
	elif 'dangcapmovie' in url:
		thumb = re.compile('rel="image_src" href="(.+?)"').findall(content)[0]
		match = re.compile('episode="(.+?)" _link="(.+?)" _sub=".+?"').findall(content)
		for eps, url1 in match:
			content1 = make_request(url1)
			match1 = re.compile('{"url":"https://redirector(.+?)","height".+?"video.+?"}').findall(content1)
			if eps == '1':
				add_link(name, 'https://redirector' + match1[-1], 99, thumb, fanart)    
			else:
				add_link('[COLOR yellow]Tập ' + eps+ '[/COLOR]', 'https://redirector' + match1[-1], 99, thumb, fanart)
				
def megabox_list_eps(url):	
	home()
	content = make_request(url)
	if 'phim-bo' in url:
		match = re.compile("title = '(.+?)' href='(.+?)'.+\s.+\s.*\s.+src=\"(.+?)\"").findall(content)
		for title, url, thumb in match:
			add_dir('[COLOR yellow]' + title + '[/COLOR]', url, 5, thumb + '?.jpg', fanart)  
	else:	  
		match = re.compile("title = '(.+?)' href='(.+?)'.+\s.+\s*\s.+\s.+src=\"(.+?)\"").findall(content)
		for title, url, thumb in match:
			if 'victorias-secret-fashion-show' in url:
				add_link('[COLOR lime]' + title + '[/COLOR]', url.replace('/phim-', '/xem-phim-'), 99, thumb + '?.jpg', fanart)
			else:		
				add_dir('[COLOR yellow]' + title + '[/COLOR]', url, 5, thumb + '?.jpg', fanart)
				 	  	
def other_megabox_list(url):
	home()	
	content = make_request(url)
	if 'video-clip' in url:
		match = re.compile("title = '(.+?)' href='(.+?)'.+\s.+\s*\s.+\s.+src=\"(.+?)\"").findall(content)
		for title, url, thumb in match:
			add_link('[COLOR lime]' + title + '[/COLOR]', url.replace('/phim-', '/xem-phim-'), 99, thumb + '?.jpg', fanart)  
	else:
		match = re.compile("title = '(.+?)' href='(.+?)'.+\s.+\s.*\s.+src=\"(.+?)\"").findall(content)
		for title, url, thumb in match:
			add_link('[COLOR lime]' + title + '[/COLOR]', url.replace('/phim-', '/xem-phim-'), 99, thumb + '?.jpg', fanart)		
										             		
def resolve_url(url):
	if 'dangcaphd' in url:
		content = make_request(url)
		try:	
			media_url = re.compile('<a _episode="1" _link="(.+?)_\d_\d+.mp4"').findall(content)[0].replace('demophimle', 'phimle2112') + '.mp4'	  
		except:
			media_url = re.compile('<a _episode="1" _link="(.+?)"').findall(content)[0].replace(' ', '%20')
	elif 'anhtrang' in url:
		content = make_request(url)
		try:
			media_url = re.compile("<source src=\"([^\"]*)\"").findall(content)[0]
		except: 
			media_url = re.compile("var video_src_mv=\"(.+?)\"").findall(content)[0]
	elif 'megabox' in url:
		content = make_request(url)
		video_url = re.compile('file: "(.+?)"').findall(content)[0]
		if 'youtube' in video_url:
			media_url = video_url.replace('https://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/play/?video_id=')
		else:
			media_url = video_url        
	elif 'phim7' in url:
		content = make_request(url)  
		try:
			media_url = 'https://redirector' + re.compile('file: "https://redirector(.+?)", label:".+?", type: "video/mp4"').findall(content)[-1]
		except:
			media_url = 'plugin://plugin.video.youtube/play/?video_id=' + re.compile('file : "http://www.youtube.com/watch\?v=(.+?)&amp').findall(content)[0]
	elif 'phimb' in url:
		url = url.replace('http://www.phimb.net', 'http://m.phimb.net')
		req = urllib2.Request(url)
		req.add_header('User-agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16')
		response = urllib2.urlopen(req, timeout = 60)
		content = response.read()
		response.close()
		try:  
			media_url = re.compile('source src="(.+?)"').findall(content)[0]
		except:
			media_url = 'plugin://plugin.video.youtube/play/?video_id=' + re.compile('src="http://www.youtube.com/embed/(.+?)\?.+?"').findall(content)[0]    
	elif 'phim14' in url:
		url = url.replace('http://phim14.net', 'http://m.phim14.net')
		req = urllib2.Request(url)
		req.add_header('User-Agent' , 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; da-dk) AppleWebKit/534.46.0 (KHTML, like Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3')
		req.add_header('Cookie', 'window.location.href')
		response = urllib2.urlopen(req, timeout = 60)
		content = response.read()
		response.close()  
		try:  
			media_url = re.compile('source src="(.+?)"').findall(content)[0]
		except:
			try:
				media_url = 'plugin://plugin.video.youtube/play/?video_id=' + re.compile('src="http://www.youtube.com/embed/(.+?)\?.+?"').findall(content)[0]  
			except:
				media_url = 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=' + re.compile('<iframe src="http://www.dailymotion.com/embed/video/(.+?)" width.+?</iframe>').findall(content)[0]	
	else:
		media_url = url  
	item = xbmcgui.ListItem(name, path = media_url)
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
				  
def add_dir(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

def add_link(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)	
	liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
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

if mode == None or url == None or len(url)<1:
	main()

elif mode == 1:
	search()
		
elif mode == 2:
	category(url)
				
elif mode == 3:
	media_list(url)

elif mode == 4:
	server_list(url)	
	
elif mode == 5:
	episode(name, url)
	
elif mode == 10:
	megabox_list_eps(url) 
  
elif mode == 11:
	other_megabox_list(url)
		
elif mode == 99:
	resolve_url(url)
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))