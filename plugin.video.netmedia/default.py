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

import urllib,urllib2,re,os
import xbmcplugin,xbmcgui,xbmcaddon

mysettings=xbmcaddon.Addon(id='plugin.video.netmedia')
profile=mysettings.getAddonInfo('profile')
home=mysettings.getAddonInfo('path')
icon=xbmc.translatePath(os.path.join(home, 'icon.png'))
logos=xbmc.translatePath(os.path.join(home, 'logos\\'))
homemenu=xbmc.translatePath(os.path.join(home, 'menulist.xml'))
homelink='https://raw.githubusercontent.com/daveln/repository.daveln/master/playlists/menulist.xml'
dict={'&amp;':'&', '&quot;':'"', '.':' ', '&#39':'\'', '&#038;':'&', '&#039':'\'', '&#8211;':'-', '&#8220;':'"', '&#8221;':'"', '&#8230':'...'}

if not os.path.exists(homemenu):
  try:
    open(homemenu, 'w+').close()
  except:
    pass  	
	
status=urllib.urlopen(homelink).getcode()
if status==200:
  urllib.urlretrieve (homelink, homemenu)
else:
  pass

def menulist():
  try:
    mainmenu=open(homemenu, 'r')  
    mlink=mainmenu.read()
    mainmenu.close()
    match=re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(mlink)
    return match
  except:
    pass	
    
def replaceAll(text, dict):
  try:
    for a, b in dict.iteritems():
      text = text.replace(a, b)
    return text
  except:
    pass	
        
def makeRequest(url):
  try:
    req=urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
    response=urllib2.urlopen(req)
    link=response.read()
    response.close()  
    return link
  except:
    pass
		
def main():
  for title, url, thumbnail in menulink:
    if 'Main Menu - ' in title:  
      addDir(title.replace('Main Menu - ',''),url,2,logos+thumbnail)
    elif 'Main Menu Plus - ' in title:  
      addDir(title.replace('Main Menu Plus - ',''),url,1,logos+thumbnail)	  
    else:
      pass

def directories():
  addDir('Tin Tức & TV Hải Ngoại',url,2,logos+'haingoai.png')
  addDir('Tin Tức & TV Trong Nước',url,2,logos+'vietnam.png')
      
def categories():
  for title, url, thumbnail in menulink:
    if 'Tôn Giáo' in name:   
      if 'Religion - ' in title:	
        addDir(title.replace('Religion - ',''),url,3,logos+thumbnail)      
      else: pass        
    elif 'Tin Tức & TV Hải Ngoại' in name:
      if 'OverseaNews - ' in title:	
        addDir(title.replace('OverseaNews - ',''),url,3,logos+thumbnail)
      else: pass	
    elif 'Tin Tức & TV Trong Nước' in name:
      if 'NewsInVN - ' in title:	
        addDir(title.replace('NewsInVN - ',''),url,3,logos+thumbnail)
      else: pass	      
    elif 'Thiếu Nhi' in name:
      if 'Children - ' in title:	
        addDir(title.replace('Children - ',''),url,3,logos+thumbnail)
      else: pass      
    elif 'Ca Nhạc' in name:
      if 'Music - ' in title:	
        addDir(title.replace('Music - ',''),url,3,logos+thumbnail)
      else: pass
    elif 'Hát Karaoke' in name:
      if 'Karaoke - ' in title:	
        addDir(title.replace('Karaoke - ',''),url,3,logos+thumbnail)
      else: pass	
    elif 'Cải Lương' in name:
      if 'CailuongTV - ' in title:
        addLink(title.replace('CailuongTV - ',''),url,logos+thumbnail)
      elif 'Cailuong - ' in title:	
        addDir(title.replace('Cailuong - ',''),url,3,logos+thumbnail)  
      else: pass	      
    elif 'Hài Kịch' in name:
      if 'Sitcom - ' in title:	
        addDir(title.replace('Sitcom - ',''),url,3,logos+thumbnail)
      else: pass
    elif 'Talk Shows' in name:
      if 'TalkShows - ' in title:	
        addDir(title.replace('TalkShows - ',''),url,3,logos+thumbnail)
      else: pass      
    elif 'TV Shows' in name:
      if 'TiviShows - ' in title:	
        addDir(title.replace('TiviShows - ',''),url,3,logos+thumbnail)
      else: pass
    elif 'Thể Thao' in name:
      if 'Sports - ' in title:	
        addDir(title.replace('Sports - ',''),url,3,logos+thumbnail)
      else: pass
    elif 'Du Lịch' in name:
      if 'Travel - ' in title:	
        addDir(title.replace('Travel - ',''),url,3,logos+thumbnail)
      else: pass
    elif 'Y Khoa' in name:
      if 'Medical - ' in title:	
        addDir(title.replace('Medical - ',''),url,3,logos+thumbnail)
      elif 'Y Tế NguoiVietTV - ' in title:
        addDir(title.replace('Y Tế NguoiVietTV - ',''),url,5,logos+thumbnail)         
      elif 'Y Tế Đồng Nai' in title:
        addDir(title.replace('Y Tế Đồng Nai - ',''),url,5,logos+thumbnail)        
      else: pass
    elif 'Ẩm Thực Tình Yêu' in name:
      if 'Cooking - ' in title:	
        addDir(title.replace('Cooking - ',''),url,3,logos+thumbnail)     
      else: pass		
    elif 'Trang Điểm' in name:
      if 'MakeUp - ' in title:	
        addDir(title.replace('MakeUp - ',''),url,3,logos+thumbnail)
      else: pass		
    elif 'Đọc Truyện' in name:
      if 'AudioBook - ' in title:	
        addDir(title.replace('AudioBook - ',''),url,3,logos+thumbnail)
      else: pass
    elif 'Di trú và Nhập Tịch Hoa Kỳ' in name:
      if 'Immigration - ' in title:	
        addDir(title.replace('Immigration - ',''),url,3,logos+thumbnail)
      else: pass
    elif 'America\'s Funniest Videos' in name:
      if 'AFV - ' in title:	
        addDir(title.replace('AFV - ',''),url,3,logos+thumbnail)
      else: pass	  
    elif 'Dicovery Channels & Animal Planet' in name:
      if 'DCAP - ' in title:	
        addDir(title.replace('DCAP - ',''),url,3,logos+thumbnail)
      else: pass	        
    elif 'Những Mục Khác' in name:
      if 'Other - ' in title:	
        addDir(title.replace('Other - ',''),url,3,logos+thumbnail)
      else: pass	  

def medicalSites(url):
  content=makeRequest(url)
  if 'www.dnrtv.org.vn' in url:
    match=re.compile("img src=\"([^\"]+)\" \/><\/a>\s*<a href=\"([^\"]*)\" class=\"title\">(.+?)<").findall(content)
    for thumbnail,url,name in match:	
      addLink(name,url,thumbnail)
    match=re.compile('class=\'paging_normal\' href=\'([^\']*)\'>Trang đầu<').findall(content)
    for url in match:	
      addDir('[COLOR violet]Trang đầu[/COLOR]',url,5,logos+'dongnai.png')    
    match=re.compile('class=\'paging_normal\' href=\'([^\']+)\'>(\d+)<').findall(content)
    for url,name in match:	
      addDir('[COLOR lime]Trang '+name+'[/COLOR]',url,5,logos+'dongnai.png')	
    match=re.compile('class=\'paging_normal\' href=\'([^\']*)\'>Trang cuối<').findall(content)
    for url in match:	
      addDir('[COLOR red]Trang cuối[/COLOR]',url,5,logos+'dongnai.png')	
  elif 'nguoiviettv' in url:
    match=re.compile('title="([^"]*)" href="([^"]+)">\s*<span class="clip">\s*<img src="(.+?)"').findall(content)[15:-6]
    for name,url,thumbnail in match:
      name=replaceAll(name,dict)  
      addLink(name,url,thumbnail)   
    match=re.compile("href='([^']*)' class='.+?'>(\d+)<").findall(content)
    for url,name in match:	
      addDir('[COLOR yellow]Trang '+name+'[/COLOR]',url.replace('&#038;','&'),5,logos+'bacsi.png')
      
def mediaLists(url):
  content=makeRequest(url)
  if 'youtube' in url:	  
    match=re.compile("player url='(.+?)\&.+?><media.+?url='(.+?)' height=.+?'plain'>(.+?)<\/media").findall(content)
    for url,thumbnail,name in match:
      name=replaceAll(name,dict)
      url = url.replace('http://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/play/?video_id=') #new
      #url = url.replace('http://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/?action=play_video&videoid=')  #old
      #url = url.replace('http://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=') #old     
      addLink(name, url, thumbnail)
    match=re.compile("<link rel='next' type='application\/atom\+xml' href='(.+?)'").findall(content)
    for url in match:	      
      addDir('[COLOR yellow]Trang kế  [COLOR cyan]>[COLOR magenta]>[COLOR orange]>[COLOR yellow]>[/COLOR]',url.replace('&amp;','&'),3,icon)		  
  elif 'dailymotion' in url:	    
    match=re.compile('<title>(.+?)<\/title>\s*<link>(.+?)_.+?<\/link>\s*<description>.+?src="(.+?)"').findall(content)
    for name,url,thumbnail in match:
      name=replaceAll(name,dict)    
      url = url.replace('http://www.dailymotion.com/video/', 'plugin://plugin.video.dailymotion_com/?mode=playVideo&url=')	  
      addLink(name, url, thumbnail)
    match=re.compile('<dm:link rel="next" href="(.+?)"').findall(content)
    for url in match:  
      addDir('[COLOR lime]Trang kế  [COLOR cyan]>[COLOR magenta]>[COLOR orange]>[COLOR yellow]>[/COLOR]',url,3,icon)	
	  
def resolveUrl(url):
  if 'www.dnrtv.org.vn' in url:
    content=makeRequest(url)
    mediaUrl=re.compile("url: '(.+?)mp4'").findall(content)[0]+'mp4'
  elif 'nguoiviettv' in url:
    content=makeRequest(url)
    videoID=re.compile('src="http://www.youtube.com/embed/(.+?)\?').findall(content)[0]
    mediaUrl='plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid='+videoID        
  else:  
    mediaUrl = url	
  item=xbmcgui.ListItem(path=mediaUrl)
  xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)  
  return

def get_params():
  param=[]
  paramstring=sys.argv[2]
  if len(paramstring)>=2:
    params=sys.argv[2]
    cleanedparams=params.replace('?','')
    if (params[len(params)-1]=='/'):
      params=params[0:len(params)-2]
    pairsofparams=cleanedparams.split('&')
    param={}
    for i in range(len(pairsofparams)):
      splitparams={}
      splitparams=pairsofparams[i].split('=')
      if (len(splitparams))==2:
        param[splitparams[0]]=splitparams[1]
  return param
				  
def addDir(name,url,mode,iconimage):
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
  ok=True
  liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
  return ok
   
def addLink(name,url,iconimage):
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=4"  
  liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  liz.setProperty('IsPlayable', 'true')  
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)  

menulink=menulist()  
params=get_params()
url=None
name=None
mode=None

try:
  url=urllib.unquote_plus(params["url"])
except:
  pass
try:
  name=urllib.unquote_plus(params["name"])
except:
  pass
try:
  mode=int(params["mode"])
except:
  pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
  main()
  
elif mode==1:
   directories()  
  
elif mode==2:
   categories()  

elif mode==3:
   mediaLists(url)
   
elif mode==4:
  resolveUrl(url)

elif mode==5:
  medicalSites(url)  
  
xbmcplugin.endOfDirectory(int(sys.argv[1]))