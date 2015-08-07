#!/usr/bin/python
# -*- coding: utf-8 -*-

""" news feed
"""

import xml.dom.minidom, urllib2

def fetch_xml(url):
  f = urllib2.urlopen(url)
  xml = f.read()
  f.close()
  return xml

def get_root(xml_str):
  dom = xml.dom.minidom.parseString(xml_str)
  return dom.documentElement

def get_items(root):
  return root.getElementsByTagName('item')

def get_title(item):
  return item.getElementsByTagName('title')[0].childNodes[0].nodeValue

def get_desc(item):
  return item.getElementsByTagName('description')[0].childNodes[0].nodeValue

def get_link(item):
  return item.getElementsByTagName('link')[0].childNodes[0].nodeValue

title = get_title(
          get_items(
            get_root(
              fetch_xml(
                'http://www.vrword.cn/portal.php?mod=rss&catid=11'
              )
            )
          )[0]
        )

desc = get_desc (
          get_items(
            get_root(
              fetch_xml(
                'http://www.vrword.cn/portal.php?mod=rss&catid=11'
              )
            )
          )[0]
        )

link = get_link (
          get_items(
            get_root(
              fetch_xml(
                'http://www.vrword.cn/portal.php?mod=rss&catid=11'
              )
            )
          )[0]
        )
#for node in title.childNodes:
#print link
