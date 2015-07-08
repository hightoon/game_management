#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  Simple web server for local application management, based on bottle framework
  Author: haitong.chen@gmail.com
"""

import time
import urllib2
from subprocess import Popen
from bottle import route, request, redirect, template,static_file, run

apps = []
user = None

class User:
  def __init__(self, usrname, password, nickname, description):
    self._usrname = usrname
    self._password = password
    self._nickname = nickname
    self._desc =description

  def write2db(self):
    # store user info to database
    pass

@route('/')
def main():
  redirect('/login')
  #redirect('./management_front_end/login_page.html')

@route('/login')
def login():
  if user=='admin':
    redirect('/static/management_front_end/admin_mngm/index.html')
  else:
    redirect('/static/management_front_end/login_page.html')

@route('/login', method='POST')
def do_login():
  global user
  print "get login post"
  forgot = None
  username = request.forms.get('username')
  password = request.forms.get('password')
  forgot = request.forms.get('forget_passwd')
  if forgot:
    print forgot
    print 'sending password to %s'%(username,)
    return "密码发送至，请查看邮箱并返回登录页面重新登录。。。"
    #redirect('/static/management_front_end/login_page.html')
  print username, password
  if check_login(username, password):
    user = username
    redirect('/index/%s'%(user,))
      #redirect('/static/management_front_end/admin_mngm/index.html')
  else:
    redirect('/login')

def check_login(usr, pwd):
  if usr == 'admin' and pwd == 'admin':
    return True
  else:
    return False

@route('/logout')
def user_logout():
  global user
  user = None
  redirect('/login')

@route('/index/<user>')
def user_index(user=user):
  if user == 'admin':
    myGames = [('hostA', '192.168.0.1', 'basketball', 'running'),
             ('hostA', '192.168.0.1', 'basketball', 'running'),]
    return template('./management_front_end/admin_mngm/index', is_admin=True, games=myGames)

@route('/static/<filename:path>')
def send_static(filename):
  return static_file(filename, root='./')
  #if user != 'admin':
  #  redirect('/')
  #else:
  #  return template('./management_front_end/admin_mngm/index')

@route('/test_temp')
def test_temp():
  myGames = [('hostA', '192.168.0.1', 'basketball', 'running'),
           ('hostA', '192.168.0.1', 'basketball', 'running'),]
  return template('./management_front_end/usr_mgr/test_temp.tpl', games=myGames)

@route("/start_game", method="POST")
def start_app():
  global apps
  f = urllib2.urlopen('http://192.168.0.4:8080/start_game')
  print f.read()
  f.close()
  redirect('/%s/index'%(user))

@route("/stop_game", method="POST")
def stop_app():
  global apps
  f = urllib2.urlopen('http://192.168.0.4:8080/stop_game')
  print f.read()
  f.close()
  redirect('/%s/index'%(user))


run(host='0.0.0.0', port=80, Debug=True)
#run(host='localhost', port=80, Debug=True)
