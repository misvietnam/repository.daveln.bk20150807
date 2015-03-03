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

mysettings=xbmcaddon.Addon(id='plugin.video.netporn')
profile=mysettings.getAddonInfo('profile')
home=mysettings.getAddonInfo('path')
fanart=xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon=xbmc.translatePath(os.path.join(home, 'icon.png'))
logos=xbmc.translatePath(os.path.join(home, 'logos\\'))
homemenu=xbmc.translatePath(os.path.join(home, 'x_playlist.m3u'))
homelink='https://raw.githubusercontent.com/daveln/repository.daveln/master/playlists/x_playlist.m3u'
hardcoresextv='rtmpe://64.62.143.5/live/do%20not%20steal%20my-Stream2'

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
    content=mainmenu.read()
    mainmenu.close()
    match=re.compile('#EXTINF.+,(.+)\s*(.+)\n').findall(content)
    return match
  except:
    pass	

def makeRequest(url):
  try:
    req=urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
    response=urllib2.urlopen(req, timeout=60)
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
  addLink('[COLOR cyan]Hardcore [COLOR red]Sex TV[/COLOR]',hardcoresextv,logos+'hardcore.png')
  addDir('[COLOR lime]Asian [COLOR red]Porn TV[/COLOR]','asianporn',1,logos+'asian.png')
  addDir('[COLOR magenta]XXX[COLOR red] by ATF01[/COLOR]','ATF01_XXX',2,logos+'atf01xxx.png') 
  addDir('[COLOR blue]XXX[COLOR red] by thanh51[/COLOR]','thanh51_xxx',4,logos+'thanh51xxx.png')  
  content=makeRequest('http://www.giniko.com/watch.php?id=95')
  match=re.compile('image: "([^"]*)",\s*file: "([^"]+)"').findall(content)
  for thumb,url in match:
    addLink('[COLOR yellow]Miami [COLOR red]TV[/COLOR]',url,thumb)
  for name,url in menulink: 
    if 'Miami International TV' in name:
      addLink('[COLOR yellow]Miami International [COLOR red]TV[/COLOR]',url,'http://www.miamitvchannel.com/images/MIAMITV-international.png')
    else:
      pass 
  '''    
  content=makeRequest('http://www.miamitvchannel.com/miami-tv.php#.VNpT4C6YHTo')
  match=re.compile("rtmp(.+?)%27%2C").findall(content)
  for url in match:
    url=urllib.unquote_plus("rtmp"+url+' live=1 timeout=60')  
    addLink('[COLOR yellow]Miami International [COLOR red]TV[/COLOR]',url,'http://www.miamitvchannel.com/images/MIAMITV-international.png') 	
  '''
  
def pornList():
  for name,url in menulink: 
    if 'Miami International TV' in name or 'ATF01' in name or 'thanh51' in name:
      pass
    else:
      addLink('[COLOR lime]'+name+'[/COLOR]',url,logos+'asian.png')
	  
def ATF01XXX():
  for name,url in menulink: 
    if 'ATF01' in name:
      addLink('[COLOR magenta]'+name.replace('ATF01 - ','')+'[/COLOR]',url,logos+'atf01xxx.png')
    else:
      pass

def thanh51xxx():
  for name,url in menulink: 
    if 'thanh51' in name:
      addLink('[COLOR blue]'+name.replace('thanh51 - ','')+'[/COLOR]',url,logos+'thanh51xxx.png')
    else:
      pass
	  
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
  pornList()

elif mode==2:
  ATF01XXX()

elif mode==4:
  thanh51xxx()
  
xbmcplugin.endOfDirectory(int(sys.argv[1]))