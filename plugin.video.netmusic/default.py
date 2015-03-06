# -*- coding: utf-8 -*-

'''
Copyright (C) 2014                                                     

This program is free software: you can redistribute it and/or modify   
it under the terms of the GNU General Public License as published by   
the Free Software Foundation, either version 4 of the License, or      
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

mysettings=xbmcaddon.Addon(id='plugin.video.netmusic')
profile=mysettings.getAddonInfo('profile')
home=mysettings.getAddonInfo('path')
fanart=xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon=xbmc.translatePath(os.path.join(home, 'icon.png'))
logos=xbmc.translatePath(os.path.join(home, 'logos\\'))
homemenu=xbmc.translatePath(os.path.join(home, 'menulist.xml'))
homelink='https://raw.githubusercontent.com/daveln/repository.daveln/master/playlists/menulist.xml'
karaoke = 'http://www.timkaraoke.com'
nctm='http://m.nhaccuatui.com/'
nhacso='http://nhacso.net/'
csn='http://chiasenhac.com/'
ThuyNga='http://ott.thuynga.com/'

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
  addDir('[COLOR lightgreen]Hát Karaoke Online[/COLOR]','KaraokeOnline',6,logos+'karaoke.png')
  addDir('[COLOR yellow]Thuý Nga - Paris by Night[/COLOR]','thuynga',11,logos+'thuynga.png')  
  addDir('[COLOR lightblue]Video Nhạc Số[/COLOR]',nhacso,2,logos+'ns.png')		
  addDir('[COLOR lime]Video Chia Sẻ Nhạc[/COLOR]',csn,2,logos+'csn.png')
  addDir('[COLOR cyan]Video Nhạc Của Tui[/COLOR]',nctm+'mv.html',2,logos+'nct.png')  
  #addLink('[COLOR orange]SCTV2 - [COLOR white]Âm Nhạc Quốc Tế[/COLOR]','rtmpe://112.197.2.154/live//sctv2_2 live=1 swfUrl=http://tv24.vn/getflash.ashx pageUrl=http://tv24.vn/LiveTV token=1b#K8!3zc65ends!',logos+'sctv2.png')  
  addLink('[COLOR gold]Vmusic[/COLOR]','http://206.190.140.142:1935/liveStream/mtv_1/playlist.m3u8',logos+'vmusic.png')	
  addLink('[COLOR magenta]Viet MTV[/COLOR]','http://64.62.143.5:1935/live/donotstealmy-Stream1/playlist.m3u8?bitrate=800&q=high',logos+'vietmtv.png')		
  #addLink('[COLOR lightblue]Viet MTV[/COLOR]','rtmpe://64.62.143.5:1935/live/donotstealmy-Stream1 swfUrl=http://www.vietstartv.com/player.swf pageUrl=http://www.vietstartv.com',logos+'vietmtv.png')		
  #addLink('[COLOR lightblue]Viet MTV[/COLOR]','rtmpe://64.62.143.5/live playpath=donotstealmy-Stream1 swfUrl=http://www.vietstartv.com/player.swf pageUrl=http://zui.vn/livetv/viet-mtv-83.html',logos+'vietmtv.png')		
  #addLink('[COLOR lightblue]Nhạc Của Tui - [COLOR gold]N+ Live[/COLOR]','rtmp://123.30.134.108:1935/live playpath=nctlive swfUrl=http://hktivi.net/player.swf pageUrl=http://hktivi.net/kenh/nhaccuatui.php',logos+'nlive.png')	
  #addLink('[COLOR lightgreen]Nhạc Của Tui - [COLOR gold]N+ Live[/COLOR]','rtmp://123.30.134.108/live/ playpath=nctlive swfUrl=http://zui.vn/templates/images/jwplayer.swf pageUrl=http://zui.vn/livetv/nhac-cua-tui-40.html',logos+'nlive.png')	
  addLink('[COLOR violet]VPop TV[/COLOR]','http://206.190.136.254:1935/liveStream/vpoptv_1/playlist.m3u8',logos+'vpop.png')
  addLink('[COLOR chocolate]iTV[/COLOR]','rtmp://live.kenhitv.vn/liveweb/ playpath=itv_web_500k.stream swfUrl=http://zui.vn/templates/images/jwplayer.swf pageUrl=http://zui.vn/livetv/itv-10.html',logos+'itv.png')
  #addLink('[COLOR silver]iTV[/COLOR]','http://117.103.224.73:1935/live/_definst_/ITV/ITV_live.smil/playlist.m3u8',logos+'itv.png')
  addLink('[COLOR orange]M[COLOR red]TV[/COLOR][/COLOR]','rtmp://85.132.78.6:1935/live/ playpath=muztv.stream swfUrl=http://zui.vn/templates/images/jwplayer.swf pageUrl=http://zui.vn/livetv/mtv-81.html',logos+'mtv.png')

def thuynga():
  addDir('PBN SHOWS | [COLOR yellow]VARIETY[/COLOR]',ThuyNga+'en/genre/index/22/3/',3,logos+'thuynga.png')  
  addDir('PBN SHOWS | [COLOR cyan]COMEDY[/COLOR]',ThuyNga+'en/genre/index/26/3',3,logos+'thuynga.png')  
  addDir('PBN SHOWS | [COLOR lime]BTS[/COLOR]',ThuyNga+'en/genre/index/64/3',3,logos+'thuynga.png')    
  
def search(): 
  try:
    keyb=xbmc.Keyboard('', '[COLOR yellow]Enter search text[/COLOR]')
    keyb.doModal()
    if (keyb.isConfirmed()):
      searchText=urllib.quote_plus(keyb.getText())
    if 'Nhạc Số' in name:  
      url=nhacso+'tim-kiem/'+searchText.replace('+',' ')+'.html'
      print "Searching URL: "+url      
      mediaList(url)
    elif 'Chia Sẻ Nhạc' in name: 
      url=csn+'search.php?s='+searchText+'&cat=video'
      print "Searching URL: "+url      
      CSN_mediaList_Search(url)      
    elif 'Nhạc Của Tui' in name:
      url=nctm+'tim-kiem/mv?q='+searchText
      print "Searching URL: "+url      
      mediaList(url)
    elif 'Tìm Karaoke' in name:
      url=karaoke+'/search/karaoke/'+searchText.replace('+',' ')
      print "Searching URL: "+url      
      mediaList(url) 
  except: pass
    
def categories(url):
  content=makeRequest(url)
  if 'nhacso' in url:
    addDir('[COLOR lime]Nhạc Số[B]   [COLOR lime]>[COLOR magenta]>[COLOR cyan]>[COLOR orange]>   [/B][COLOR lime]Tìm Nhạc[/COLOR]',nhacso,1,logos+'ns.png')			
    match=re.compile("<a href=\"http:\/\/nhacso.net\/the-loai-video(.+?)\" title=\"([^\"]*)\"").findall(content)[0:21]
    for url,name in match:
      if 'Nhạc Cách Mạng' in name: 
        pass
      else:	
	    addDir('[COLOR yellow]'+name+'[/COLOR]',nhacso+'the-loai-video'+url,3,logos+'ns.png')	  
    match=re.compile("<a href=\"http:\/\/nhacso.net\/nghe-si(.+?)\">(.*?)</a>").findall(content)[0:36]
    for url,name in match:
      if 'Lord Wind' in name: 
        pass
      else:		
        addDir('[COLOR cyan]'+name+'[/COLOR]',nhacso+'video-cua-nghe-si'+url.replace('.html','-1-1.html'),3,logos+'ns.png')	  	  
  elif 'chiasenhac' in url:
    addDir('[COLOR yellow]Chia Sẻ Nhạc[B]   [COLOR lime]>[COLOR magenta]>[COLOR cyan]>[COLOR orange]>   [/B][COLOR yellow]Tìm Nhạc[/COLOR]',csn,1,logos+'csn.png')		
    match=re.compile("<a href=\"hd(.+?)\" title=\"([^\"]*)\"").findall(content)[1:8]
    for url,name in match:
	  addDir('[COLOR lime]'+name+'[/COLOR]',csn+'hd'+url,3,logos+'csn.png')
  elif 'nhaccuatui' in url:
    addDir('[COLOR yellow]Nhạc Của Tui   [B][COLOR lime]>[COLOR orange]>[COLOR blue]>[COLOR magenta]>   [/B][COLOR yellow]Tìm Video[/COLOR]',nctm,1,logos+'nhaccuatui.png')
    match=re.compile("href=\"http:\/\/m.nhaccuatui.com\/mv\/(.+?)\" title=\"([^\"]*)\"").findall(content)
    for url,name in match:		
      if 'Cách Mạng' in name or 'Phim' in name:
	    pass
      else:	  
        addDir('[COLOR lime]'+name+'[/COLOR]',nctm+'mv/'+url,3,logos+'nct.png')
    match=re.compile("href=\"http:\/\/m.nhaccuatui.com\/mv\/(.+?)\" title=\"([^\"]*)\"").findall(content)
    for url,name in match:
      if 'Phim' in name:
        addDir('[COLOR orange]'+name+'[/COLOR]',nctm+'mv/'+url,3,logos+'nhaccuatui.png')		
  elif 'timkaraoke' in url:
    addDir('[COLOR cyan]Tìm Karaoke[B]   [COLOR cyan]>[COLOR orange]>[COLOR blue]>[COLOR magenta]>   [/B][COLOR cyan]Karaoke Search[/COLOR]', karaoke, 1, logos + 'timkaraoke.png') 
    match = re.compile('pagespeed_url_hash="1785647900".+?href="([^"]*)">([^>]+)<').findall(content)
    for url, name in match: 
      add_Link('[COLOR yellow]' + name + '[/COLOR]', ('%s%s' % (karaoke, url)), logos + 'timkaraoke.png')  
    match = re.compile('<\/i> <br\/>\s*<a href="([^"]*)">([^>]+)<').findall(content)
    for url, name in match: 
      add_Link('[COLOR lime]' + name + '[/COLOR]',('%s%s' % (karaoke, url)), logos + 'timkaraoke.png')
      
def getKaraoke():
  addDir('[COLOR cyan]Vietnamese[COLOR magenta] - [COLOR lightgreen]timkaraoke.com[/COLOR]',karaoke,2,logos+'timkaraoke.png')
  for title, url, thumbnail in menulink:
    if 'Karaoke - ' in title:
      addDir(title.replace('Karaoke - ',''),url,3,logos+thumbnail) 
  
def mediaList(url):
  content=makeRequest(url)
  if 'chiasenhac' in url:		
    match=re.compile("<a href=\"([^\"]*)\" title=\"(.*?)\"><img src=\"([^\"]+)\"").findall(content)
    for url,name,thumbnail in match:
      add_Link('[COLOR yellow]'+name+'[/COLOR]',(csn+url),thumbnail)
    match=re.compile("<a href=\"(.+?)video\/\" class=\"npage\">1<\/a>").findall(content)[0:1]
    for url in match:
      addDir('[COLOR cyan]Trang Đầu Tiên ([COLOR lime]Nhạc Video Mới Chia Sẻ[COLOR cyan] + [COLOR orange]Download Mới Nhất[COLOR cyan])[/COLOR]',csn+url+'video/',3,logos+'csn.png')
    match=re.compile("<a href=\"hd\/video\/([a-z]-video\/new[0-9]+).html\" class=\"npage\">(\d+)<\/a>").findall(content)
    for url,name in match:
      addDir('[COLOR lime]Trang Mới Chia Sẻ '+name+'[/COLOR]',csn+'hd/video/'+url+'.html',3,logos+'csn.png')
    match=re.compile("<a href=\"hd\/video\/([a-z]-video\/down[0-9]+).html\" class=\"npage\">(\d+)<\/a>").findall(content)
    for url,name in match:
      addDir('[COLOR orange]Trang Download Mới Nhất '+name+'[/COLOR]',csn+'hd/video/'+url+'.html',3,logos+'csn.png')	  
  elif 'nhacso' in url:		
    if 'the-loai-video' in url:
      match=re.compile("<a href=\"([^\"]*)\" title=\"(.*?)\".+?\s.*?src=\"([^\"]+)\" width").findall(content)
      for url,name,thumbnail in match:
        add_Link('[COLOR yellow]'+name+'[/COLOR]',url,thumbnail)
      match=re.compile("<li ><a href=\"(.+?)\">(\d+)<\/a><\/li>").findall(content)
      for url,name in match:
        addDir('[COLOR lime]Trang '+name+'[/COLOR]',url,3,logos+'ns.png')								
    else:
      match=re.compile("<a class=\"png_img playlist\" href=\"(.+?)\" title=\"([^\"]*)\".+?\s.*?src=\"([^\"]+)\" onerror").findall(content)
      for url,name,thumbnail in match:
        add_Link('[COLOR cyan]'+name+'[/COLOR]',url,thumbnail)
      match=re.compile("<li ><a href=\"(.+?)\">(\d+)<\/a><\/li>").findall(content)
      for url,name in match:
        addDir('[COLOR lime]Trang '+name+'[/COLOR]',url,3,logos+'ns.png')
  elif 'nhacso.net/tim-kiem' in url or 'nhacso.net/tim-video' in url:	
    match=re.compile("href=\"(.+?)\" title=\"(.+?)\".+?>\s*<img width.+?src=\"(.+?)\"").findall(content)
    for url,name,thumbnail in match:
      add_Link('[COLOR yellow]'+name+'[/COLOR]',url,thumbnail) 
    match=re.compile("class=\"xemthem\" href=\"http:\/\/nhacso.net\/tim-video(.+?)\"").findall(content)
    for url in match:
      addDir('[COLOR lime]Xem Tất Cả[COLOR orange]  >>>>[/COLOR]','http://nhacso.net/tim-video' + url.replace(' ','%20'),3,logos+'ns.png')	
    match=re.compile("style=\"cursor: pointer;\" href=\"(.+?)\"><ins>(\d+)<\/ins>").findall(content)
    for url,name in match:
      addDir('[COLOR lime]Trang '+name+'[COLOR orange]  >>>>[/COLOR]',url.replace(' ','%20'),3,logos+'ns.png')	  	  
  elif 'nhaccuatui' in url:
    match=re.compile("href=\"http:\/\/m.nhaccuatui.com\/video\/([^\"]*)\" title=\"([^\"]+)\"><img alt=\".+?\" src=\"(.*?)\"").findall(content)		
    for url,name,thumbnail in match:
      add_Link('[COLOR yellow]'+name+'[/COLOR]',nctm+'video/'+url,thumbnail)
    match=re.compile("href=\"([^\"]*)\" class=\"next\" titlle=\"([^\"]+)\"").findall(content)
    for url,name in match:	
      addDir('[COLOR cyan]'+name+'[COLOR orange]  >>>>[/COLOR]',url,3,logos+'nct.png')
  elif 'timkaraoke' in url:
    match = re.compile('pagespeed_url_hash="1785647900".+?href="([^"]*)">([^>]+)<').findall(content)
    for url, name in match: 
      add_Link('[COLOR cyan]' + name + '[/COLOR]', ('%s%s' % (karaoke, url)), logos + 'timkaraoke.png') 
  elif 'youtube' in url:	  
    match=re.compile("player url='(.+?)\&.+?><media.+?url='(.+?)' height=.+?'plain'>(.+?)<\/media").findall(content)
    for url,thumbnail,name in match:       
      name=name.replace("&#39;", "'").replace('&amp;', '&').replace('&quot;', '"')
      #url=url.replace('http://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/?action=play_video&videoid=')
      url=url.replace('http://www.youtube.com/watch?v=', 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=')	      
      add_Link(name, url, thumbnail)
    match=re.compile("<link rel='next' type='application\/atom\+xml' href='(.+?)'").findall(content)
    for url in match:  
      addDir('[COLOR yellow]Trang kế  [COLOR cyan]>[COLOR magenta]>[COLOR orange]>[COLOR yellow]>[/COLOR]',url.replace('&amp;','&'),3,icon)		  
  elif 'thuynga' in url:
	match=re.compile("style=\"background-image: url\('(.+?)'\)\">\s*<span class.+?</span>\s.+\s.+\s.+\s*<a href=\"(.+?)\">(.+?)<").findall(content)
	for thumbnail,url,name in match:
	  add_Link(name,ThuyNga+url,thumbnail+'?.jpg')
	match=re.compile('href="http://ott.thuynga.com/([^>]+)">(\d+)<').findall(content)	
	for url,name in match:
	  addDir('[COLOR magenta]Trang '+name+'[/COLOR]',ThuyNga+url,3,logos+'thuynga.png')	
	       
def CSN_mediaList_Search(url):
  content=makeRequest(url)			
  match=re.compile("<a href=\"([^\"]*)\" title=\"(.*?)\"><img src=\"([^\"]+)\"").findall(content)
  for url,name,thumbnail in match:
    add_Link('[COLOR yellow]'+name+'[/COLOR]',(csn+url),thumbnail)
  match=re.compile("href=\"(.+?)\" class=\"npage\">(\d+)<").findall(content)
  for url,name in match:
    addDir('[COLOR cyan]Trang '+name+'[/COLOR]',url.replace('&amp;','&'),5,logos+'csn.png')  
		
def resolveUrl(url):
  content=makeRequest(url)
  if 'chiasenhac' in url:		
    try:
      mediaUrl=re.compile("\"hd-2\".+?\"([^\"]+)\"").findall(content)[0].replace('%3A',':').replace('%2F','/').replace('%2520','%20')
    except:
      mediaUrl=re.compile("\"file\".*?\"([^\"]*)\"").findall(content)[-1].replace('%3A',':').replace('%2F','/').replace('%2520','%20')
  elif 'nhacso' in url:		
    mediaUrl=re.compile("src=\"([^\"]+)\" data-setup").findall(content)[0]	
  elif 'nhaccuatui' in url:
    mediaUrl=re.compile("title=\".+?\" href=\"([^\"]*)\"").findall(content)[0] 
  elif 'timkaraoke' in url:
    mediaUrl=re.compile('source src="(.+?)"').findall(content)[0].replace(' ','%20')  
  elif 'youtube' in url:
    mediaUrl=url 
  elif 'thuynga' in url:
    mediaUrl=re.compile("var iosUrl = '(.+?)'").findall(content)[0]  
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
  
def add_Link(name,url,iconimage):
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=4"  
  liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  liz.setProperty('IsPlayable', 'true')  
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)  
  
def addLink(name,url,iconimage):
  ok=True
  liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
  return ok

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
  search()	
		
elif mode==2:
  categories(url)		
		
elif mode==3:
  mediaList(url)
		
elif mode==4:
  resolveUrl(url)		

elif mode==5:
  CSN_mediaList_Search(url)		

elif mode==6:
  getKaraoke() 

elif mode==11:
  thuynga()
  
xbmcplugin.endOfDirectory(int(sys.argv[1]))

