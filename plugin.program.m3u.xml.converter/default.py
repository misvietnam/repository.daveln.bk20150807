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

import urllib,urllib2,re,os,sys,time
import xbmcplugin,xbmcgui,xbmcaddon

mysettings=xbmcaddon.Addon(id='plugin.program.m3u.xml.converter')
profile=mysettings.getAddonInfo('profile')
home=mysettings.getAddonInfo('path')
my_settings=mysettings.getSetting
fanart=xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon=xbmc.translatePath(os.path.join(home, 'icon.png'))
logos=xbmc.translatePath(os.path.join(home, 'logos\\'))
xml_file=my_settings('xml_file')
m3u_file=my_settings('m3u_file')
thumb=my_settings('thumb')
dest=my_settings('dest')
m3u_regex='#.+,(.+?)\n(.+?)\n'
xml_regex='<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>'
convert_m3u_to_xml=xbmc.translatePath(os.path.join(dest, (time.strftime("%m%d%Y_%H%M%S_")+m3u_file.split('/')[-1].split('\\')[-1].replace('.m3u','.xml').replace('.M3U','.xml'))))
convert_xml_to_m3u=xbmc.translatePath(os.path.join(dest, (time.strftime("%m%d%Y_%H%M%S_")+xml_file.split('/')[-1].split('\\')[-1].replace('.xml','.m3u').replace('.XML','.m3u'))))

def open_file(file):
  try:
    f=open(file, 'r')
    content=f.read()
    f.close()
    return content	
  except:
    pass 
  	
def main():
  addDir('[COLOR yellow]XML to M3U Converter[COLOR magenta]  *****  [COLOR white]NO REGEX[/COLOR]','XML2M3U',1,logos+'icon.png')
  addDir('[COLOR cyan]Đổi M3U Sang XML[COLOR magenta]  *****  [COLOR white]KHÔNG REGEX[/COLOR]','M3U2XML',2,icon)
  
def XML_to_M3U():
  if len(xml_file) <= 0:
    mysettings.openSettings()
  else:
    try:
      f=open(convert_xml_to_m3u, 'w+')
      f.write('#EXTM3U' + '\n\n' + '#EXTINF:-1,[COLOR lime]****[COLOR cyan] CREATED ON ' + time.strftime("[COLOR yellow]%m-%d-%Y") + ' [COLOR lime]****[/COLOR]' + '\n' + 'http://www.youtube.com' + '\n\n')	
      link=open_file(xml_file)  
      match=re.compile(xml_regex).findall(link) 
      for title,url,thumbnail in match:
        url=url.replace('&amp;','&')
        f.write('#EXTINF:-1,' + title + '\n' + url + '\n')
      f.write('\n\n\n\n')
      f.close()
      xbmcgui.Dialog().ok('[COLOR yellow]XML to M3U Converter[/COLOR]', 'Done.')
    except:	
      xbmcgui.Dialog().ok('[COLOR yellow]XML to M3U Converter[/COLOR]', 'Please choose a different path to destination folder.', '', 'Then try again.')
  
def M3U_to_XML():
  if len(m3u_file) > 0:
    try: 	
      f=open(convert_m3u_to_xml, 'w+')
      f.write('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n\n<stream>\n\n<item>\n<title>[COLOR lime]****[COLOR cyan] ' + time.strftime('CREATED ON [COLOR yellow]%m-%d-%Y [COLOR lime]****[/COLOR]</title>\n<link>http://www.youtube.com</link>\n<thumbnail>') + thumb + '</thumbnail>\n</item>\n\n')		
      link=open_file(m3u_file)  
      match=re.compile(m3u_regex).findall(link) 
      for title,url in match:
        url=url.replace('&','&amp;').replace('rtmp://$OPT:rtmp-raw=','')	  
        f.write('<item>\n<title>' + title + '</title>\n<link>' + url + '</link>\n<thumbnail>' + thumb + '</thumbnail>\n</item>\n')
      f.write('\n</stream>\n\n\n\n')
      f.close()	  
      xbmcgui.Dialog().ok('[COLOR cyan]Đổi M3U Sang XML[/COLOR]', 'Xong.')
    except:	
      xbmcgui.Dialog().ok('[COLOR cyan]Đổi M3U Sang XML[/COLOR]', 'Vui lòng chọn lại đường dẫn khác đến thư mục.', '', 'Thử lại.')
  else:	
    mysettings.openSettings()
  
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
  XML_to_M3U() 
  sys.exit()

elif mode==2:
  M3U_to_XML() 
  sys.exit()
  
xbmcplugin.endOfDirectory(int(sys.argv[1]))
