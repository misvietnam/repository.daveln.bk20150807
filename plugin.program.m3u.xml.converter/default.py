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
fanart=xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon=xbmc.translatePath(os.path.join(home, 'icon.png'))
logos=xbmc.translatePath(os.path.join(home, 'logos\\'))
xml_file=mysettings.getSetting('xml_file')
m3u_file=mysettings.getSetting('m3u_file')
thumb=mysettings.getSetting('thumb')
dest=mysettings.getSetting('dest')
m3u_regex='#.+,(.+?)\n(.+?)\n'
xml_regex='<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>'
convert_m3u_to_xml=xbmc.translatePath(os.path.join(dest, (time.strftime("%m%d%Y_%H%M%S_")+m3u_file.split('/')[-1].split('\\')[-1].replace('.m3u','.xml').replace('.M3U','.xml'))))
convert_xml_to_m3u=xbmc.translatePath(os.path.join(dest, (time.strftime("%m%d%Y_%H%M%S_")+xml_file.split('/')[-1].split('\\')[-1].replace('.xml','.m3u').replace('.XML','.m3u'))))

def main():
  addDir('[COLOR yellow]XML to M3U Converter[COLOR magenta]  *****  [COLOR white]NO REGEX[/COLOR]','XML2M3U','XMLtoM3U',logos+'icon.png')
  addDir('[COLOR cyan]M3U to XML Converter[COLOR magenta]  *****  [COLOR white]NO REGEX[/COLOR]','M3U2XML','M3UtoXML',icon)
  
def XML_to_M3U():
  if len(xml_file) <= 0:
    mysettings.openSettings()
    main()	
  else:
    try:
      print >> open(convert_xml_to_m3u, 'a+'), ('#EXTM3U' + '\n\n' + '#EXTINF:-1,[COLOR lime]****[COLOR cyan] CREATED ON ' + time.strftime("[COLOR yellow]%m-%d-%Y") + ' [COLOR lime]****[/COLOR]' + '\n' + 'http://www.youtube.com' + '\n')	
      xml_list=open(xml_file, 'r')  
      link=xml_list.read()
      xml_list.close()
      match=re.compile(xml_regex).findall(link) 
      for title, url, thumbnail in match:
        url=url.replace('&amp;','&').replace('rtmp://$OPT:rtmp-raw=','')
        print >> open(convert_xml_to_m3u, 'a+'), ('#EXTINF:-1,' + title + '\n' + url)
      print >> open(convert_xml_to_m3u, 'a+'), '\n\n\n\n'
      xbmcgui.Dialog().ok('[COLOR yellow]XML to M3U Converter[/COLOR]', 'Done.', '', 'Congratulations!')
      main()
    except:	
      xbmcgui.Dialog().ok('[COLOR yellow]XML to M3U Converter[/COLOR]', 'Please choose a different path to destination folder.', '', 'Then try again.')
      main()
  
def M3U_to_XML():
  if len(m3u_file) > 0:
    try: 	
      print >> open(convert_m3u_to_xml, 'a+'), ('<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n\n<stream>\n\n<item>\n<title>[COLOR lime]****[COLOR cyan] ' + time.strftime('CREATED ON [COLOR yellow]%m-%d-%Y [COLOR lime]****[/COLOR]</title>\n<link>http://www.youtube.com</link>\n<thumbnail>') + thumb + '</thumbnail>\n</item>\n')		
      m3u_list=open(m3u_file, 'r')  
      link=m3u_list.read()
      m3u_list.close()
      match=re.compile(m3u_regex).findall(link) 
      for title, url in match:
        url=url.replace('&','&amp;').replace('rtmp://$OPT:rtmp-raw=','')	  
        print >> open(convert_m3u_to_xml, 'a+'), ('<item>\n<title>' + title + '</title>\n<link>' + url + '</link>\n<thumbnail>' + thumb + '</thumbnail>\n</item>')
      print >> open(convert_m3u_to_xml, 'a+'), '\n</stream>\n\n\n\n'	
      xbmcgui.Dialog().ok('[COLOR cyan]M3U to XML Converter[/COLOR]', 'Đã xong.', '', 'Chúc mừng!')
      main()	  
    except:	
      xbmcgui.Dialog().ok('[COLOR cyan]M3U to XML Converter[/COLOR]', 'Vui lòng chọn lại đường dẫn khác đến thư mục.', '', 'Thử lại.')
      main()
  else:	
    mysettings.openSettings()
    main()
  
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
  u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode=1"  
  liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
  liz.setInfo( type="Video", infoLabels={ "Title": name } )
  liz.setProperty('IsPlayable', 'true')  
  ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)  

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
  mode=(params["mode"])
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
  
elif mode=='XMLtoM3U':
  XML_to_M3U() 

elif mode=='M3UtoXML':
  M3U_to_XML() 
  
xbmcplugin.endOfDirectory(int(sys.argv[1]))

