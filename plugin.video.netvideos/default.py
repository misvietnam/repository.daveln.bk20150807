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

mysettings=xbmcaddon.Addon(id='plugin.video.netvideos')
profile=mysettings.getAddonInfo('profile')
home=mysettings.getAddonInfo('path')
fanart=xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon=xbmc.translatePath(os.path.join(home, 'icon.png'))
logos=xbmc.translatePath(os.path.join(home, 'logos\\'))
homemenu=xbmc.translatePath(os.path.join(home, 'netvideos.xml'))
homelink='https://raw.githubusercontent.com/daveln/repository.daveln/master/playlists/netvideos.xml'
dict={'&amp;':'&', '&quot;':'"', '.':' ', '&#39':'\'', '&#038;':'&', '&#039':'\'', '&#8211;':' - ', '&#8220;':'"', '&#8221;':'"', '&#8230':'...'}
dongnai='http://www.dnrtv.org.vn'
CaliToday='http://truyenhinhcalitoday.com/'
nguoiviettvcom='http://nguoiviettv.com'
cailuongus='http://phimtailieu.haikich.us'

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
    response=urllib2.urlopen(req, timeout=90)
    link=response.read()
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
  addDir('Hải Ngoại','HaiNgoai',1,logos+'haingoai.png')
  addDir('Trong Nước','TrongNuoc',2,logos+'vietnam.png')  
      
def trongnuoc():
  addDir('Đài Phát Thanh - Truyền Hình Đồng Nai',dongnai,3,logos+'dongnai.png')
  
def haingoai(): 
  addDir('nguoiviettv.com',nguoiviettvcom,4,logos+'nguoiviet.png') 
  addDir('Truyền Hình Cali Today',CaliToday,3,logos+'cali.png')  
  addDir('Cải Lương - Hài Kịch',cailuongus,3,logos+'cailuongus.png') 
  
def mediaStations(url):
  content=makeRequest(url)
  if 'www.dnrtv.org' in url:
    match=re.compile("tabindex=\"0\"><a href=\"([^\"]+)\">(.+?)<").findall(content)[13:]
    for url,name in match:  	
      addDir(name,dongnai+url,5,logos+'dongnai.png')
  elif 'truyenhinhcalitoday' in url:
    match=re.compile('href="http://truyenhinhcalitoday.com/category([^>]+)">([^>]+)<').findall(content)[0:12]
    for url,name in match:	
      addDir(name,CaliToday+'category'+url,5,logos+'cali.png')			
  elif 'haikich' in url:
    addDir('Phim Tài Liệu Tổng Hợp','http://phimtailieu.haikich.us/',7,logos+'cailuongus.png')
    match=re.compile('class="cat-item.+?"><a href="([^"]*)".*?><span>([^>]*)<').findall(content)
    for url,name in match:	    
      addDir(name,url,5,logos+'cailuongus.png')
        
def NguoiViet():
  for title, url, thumbnail in menulink:
    if 'nguoiviet.com - ' in title:
      addDir(title.replace('nguoiviet.com - ',''),url,5,logos+thumbnail)
    else: pass      
     
def mediaList(url):	
  content=makeRequest(url)
  if 'www.dnrtv.org.vn' in url:
    match=re.compile("img src=\"([^\"]+)\" \/><\/a>\s*<a href=\"([^\"]*)\" class=\"title\">(.+?)<").findall(content)
    for thumbnail,url,name in match:     
      addLink(name,url,thumbnail)
    match=re.compile('class=\'paging_normal\' href=\'([^\']*)\'>Trang đầu<').findall(content)
    for url in match:	
      addDir('[COLOR yellow]Trang đầu[/COLOR]',url,5,logos+'dongnai.png')    
    match=re.compile('class=\'paging_normal\' href=\'([^\']+)\'>(\d+)<').findall(content)
    for url,name in match:	
      addDir('[COLOR lime]Trang '+name+'[/COLOR]',url,5,icon)	
    match=re.compile('class=\'paging_normal\' href=\'([^\']*)\'>Trang cuối<').findall(content)
    for url in match:	
      addDir('[COLOR red]Trang cuối[/COLOR]',url,5,logos+'dongnai.png')	
  elif 'truyenhinhcalitoday' in url:
    match=re.compile('href="(.+?)">\s*<span class="clip">\s*<img src="(.+?)" alt="(.+?)"').findall(content)
    for url,thumbnail,name in match:
      name=replaceAll(name,dict)
      addLink(name,url,thumbnail)
    match=re.compile("href='([^']*)' class='first'").findall(content)
    for url in match:	
      addDir('[COLOR yellow]Trang đầu[/COLOR]',url,5,logos+'cali.png')    
    match=re.compile("href='([^']*)' class='page larger'>(\d+)<").findall(content)
    for url,name in match:	
      addDir('[COLOR lime]Trang '+name+'[/COLOR]',url,5,logos+'cali.png')	
    match=re.compile("href='([^']*)' class='last'").findall(content)
    for url in match:	
      addDir('[COLOR red]Trang cuối[/COLOR]',url,5,logos+'cali.png')	
  elif 'nguoiviettv' in url:
    if 'orderby=views' in url:
      match=re.compile('title="([^"]*)" href="([^"]+)">\s*<span class="clip">\s*<img src="(.+?)"').findall(content)[0:24]
      for name,url,thumbnail in match:
        name=replaceAll(name,dict)
        addLink(name,url,thumbnail)
    else: 
      match=re.compile('title="([^"]*)" href="([^"]+)">\s*<span class="clip">\s*<img src="(.+?)"').findall(content)[15:-6]
      for name,url,thumbnail in match:
        name=replaceAll(name,dict)
        addLink(name,url,thumbnail)    
    match=re.compile("href='([^']*)' class='.+?'>(\d+)<").findall(content)
    for url,name in match:	
      addDir('[COLOR yellow]Trang '+name+'[/COLOR]',url.replace('#038;',''),5,logos+'nguoiviet.png')
  elif 'haikich' in url:
    match=re.compile('href="([^"]*)" title="([^"]+)"><img src="([^"]*)"').findall(content)
    for url,name,thumbnail in match:
      name=replaceAll(name,dict)    
      addLink(name,url,thumbnail)    
    match=re.compile("href='([^']*)' class='.+?'>(\d+)<").findall(content)
    for url,name in match:	
      addDir('[COLOR yellow]Trang '+name+'[/COLOR]',url,5,logos+'cailuongus.png')
           
def resolveUrl(url):
  if 'www.dnrtv.org.vn' in url:
    content=makeRequest(url)  
    mediaUrl=re.compile("url: '(.+?)mp4'").findall(content)[0]+'mp4' 
  elif 'truyenhinhcalitoday' in url or 'nguoiviettv' in url:
    content=makeRequest(url)  
    videoID=re.compile("http://www.youtube.com/embed/(.+?)\?").findall(content)[0]  
    mediaUrl='plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid='+videoID 
  elif 'haikich' in url:
    content=makeRequest(url)  
    videoID=re.compile('embed src="http://www.youtube.com/v/(.+?)\?version.+?"').findall(content)[0]  
    mediaUrl='plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid='+videoID         
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
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
  ok=True
  liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
  return ok
 	  
def addLink(name,url,iconimage):
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=6"+"&iconimage="+urllib.quote_plus(iconimage)  
  liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  liz.setProperty('IsPlayable', 'true')  
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)  
	  
menulink=menulist()
params=get_params()
url=None
name=None
mode=None
iconimage=None

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
try:
  iconimage=urllib.unquote_plus(params["iconimage"])
except:
  pass  

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "iconimage: "+str(iconimage)

if mode==None or url==None or len(url)<1:
  main()

elif mode==1:
  haingoai()

elif mode==2:
  trongnuoc()

elif mode==3:
  mediaStations(url)

elif mode==4:
  NguoiViet()
  
elif mode==5:
  mediaList(url)
		
elif mode==6:
  resolveUrl(url)
 
xbmcplugin.endOfDirectory(int(sys.argv[1]))