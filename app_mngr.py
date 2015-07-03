#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  Simple web server for local application management, based on bottle framework

  Author: haitong.chen@gmail.com
"""
import urllib2
from subprocess import Popen
from bottle import route, request, redirect, template,static_file, run

apps = []
user = None

@route('/')
def main():
  redirect('/login')
  #redirect('./management_front_end/login_page.html')

@route('/login')
def login():
  if user=='admin':
    redirect('/static/index.html')
  else:
    redirect('/static/management_front_end/login_page.html')
  if 0:
    return '''
        <html>
        <head>
            <h3>登录</h3>
            <style>
                html,body{text-align:center;margin:100px auto;}
            </style>
        </head>
        <body>
        <form action="/login" method="post">
            用户名: <input name="username" type="text" /><br/><br/>
            密   码: <input name="password" type="password" />
            <br/><input value="Login" type="submit" />
        </form></body>
        </html>
    '''

@route('/login', method='POST')
def do_login():
  global user
  print "get login post"
  username = request.forms.get('username')
  password = request.forms.get('password')
  print username, password
  if check_login(username, password):
    user = username
    if user == 'admin':
      redirect('/static/management_front_end/admin_mngm/index.html')
  else:
    #return "<p>Login failed.</p>"
    pass

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

@route('/static/<filename:path>')
def send_static(filename):
  return static_file(filename, root='./')
  #if user != 'admin':
  #  redirect('/')
  #else:
  #  return template('./management_front_end/admin_mngm/index')

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


run(host='localhost', port=8080, debug=True)
