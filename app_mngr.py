#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  Simple web server for local application management, based on bottle framework

  Author: haitong.chen@gmail.com
"""
import urllib2
from subprocess import Popen
from bottle import route, request, redirect, template, run

apps = []
user = None

@route('/')
def main():
  redirect('/login')

@route('/login')
def login():
  if user:
    redirect('/%s/index'%(user))
  else:
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
  username = request.forms.get('username')
  password = request.forms.get('password')
  if check_login(username, password):
    user = username
    redirect('/%s/index'%(user))
  else:
    #return "<p>Login failed.</p>"
    pass

def check_login(usr, pwd):
  if usr == 'admin' and pwd == 'admin':
    return True
  else:
    return False

@route('/admin/index')
def admin_page():
  if user != 'admin':
    redirect('/')
  else:
    return template('admin_main')
  #else:
  #  return """
  #    <html>
  #      <h1>网吧网络应用管理系统</h1>
  #      <body>
  #        <h3>Host-1</h3>
  #        PPS影音     <a href="/start">启动</a>     <a href="/stop">停止</a>
  #      </body>
  #    </html>
  #  """

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
