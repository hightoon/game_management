#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  Simple web server for local application management, based on bottle framework
  Author: haitong.chen@gmail.com
"""

import time, urllib2, sqlite3
from datetime import datetime
from subprocess import Popen
from bottle import route, request, redirect, template,static_file, run

# globals for debug purpose
apps = []
act_user = None

# database manipulation
class GMDatabase:
  def __init__(self, dbfile='default.db'):
    self.dbfile = dbfile
    self.conn = sqlite3.connect(dbfile)

  def create_table(self, tabname, fmt):
    c = self.conn.cursor()
    try:
      c.execute("CREATE TABLE %s %s"%(tabname, fmt))
    except sqlite3.OperationalError:
      pass

  def commit(self):
    self.conn.commit()

  def close(self):
    self.conn.close()

  @property
  def cursor(self):
    return self.conn.cursor()

# user object
class User:
  IS_ADMIN = 1
  NOT_ADMIN = 0
  op_db_file = 'test_op_0.db'
  usr_db_file = 'test_user_0.db'
  user_db = GMDatabase(usr_db_file)
  op_db = GMDatabase(op_db_file)
  user_db.text_factory = str
  def __init__(self, usrname, password, is_admin=NOT_ADMIN,
              nickname='guest', email='', desc='',):
    self._usrname = usrname
    self._password = password
    self._nickname = nickname
    self._email = email
    self._desc = desc
    self._is_admin = is_admin
    self.login_time = datetime.now()
    self.operations = 0

  @property
  def usrname(self):
    return self._usrname

  @usrname.setter
  def usrname(self, name):
    self._usrname = name

  @property
  def password(self):
    return self._password

  @password.setter
  def password(self, passwd):
    self._password = passwd

  @property
  def nickname(self):
    return self._nickname

  @nickname.setter
  def nickname(self, nickname):
    self._nickname = nickname

  @property
  def email(self):
    return self._email

  @email.setter
  def email(self, email):
    self._email = email

  @property
  def desc(self):
    return self._desc

  @property
  def is_admin(self):
    return self._is_admin

  @is_admin.setter
  def is_admin(self, yesorno):
    self._is_admin = yesorno

@route('/')
def main():
  redirect('/login')
  #redirect('./management_front_end/login_page.html')

@route('/login')
def login():
  if act_user is not None:
    #redirect('/static/management_front_end/admin_mngm/index.html')
    redirect('/index/%s'%(act_user.usrname,))
  else:
    redirect('/static/management_front_end/login_page.html')

@route('/login', method='POST')
def do_login():
  global act_user
  print "get login post"
  forgot = None
  username = request.forms.get('username')
  password = request.forms.get('password')
  forgot = request.forms.get('forget_passwd')

  if forgot:
    print forgot
    print 'sending password to %s'%(username,)
    return "密码发送至，请查看邮箱并返回登录页面重新登录。。。"

  isvalid, isadmin = validate_from_db(username, password)
  print isvalid, isadmin
  if isvalid:
    act_user = User(username, password, isadmin)
    if isadmin == User.IS_ADMIN:
      redirect('/index/admin')
    else:
      redirect('/index/%s'%username)
  else:
    redirect('/')

def check_login(usr, pwd):
  if usr == 'admin' and pwd == 'admin':
    return True
  else:
    return False

def validate_from_db(usr, passwd):
  c = User.user_db.cursor
  try:
    u, p, r, _, _, _ = c.execute("SELECT * FROM users WHERE name=?", (usr,)).fetchone()
  except:
    return False, User.NOT_ADMIN
  print u, p, r
  if u == usr and p == passwd:
    return True, r
  return False, User.NOT_ADMIN

@route('/logout')
def user_logout():
  global act_user
  act_user = None
  redirect('/login')

@route('/logout', method='POST')
def logout_change_passwd():
  global act_user
  act_user = None
  redirect('/login')

@route('/change_passwd')
def change_passwd():
  print 'change password'
  return "修改密码"

@route('/index/<username>')
def user_index(username):
  if act_user is not None and act_user.usrname == username:
    now = datetime.now()
    return template('./management_front_end/admin_mngm/index',
                    is_admin=act_user.is_admin, username=act_user.usrname,
                    nowtime="%d:%d:%d"%(now.hour, now.minute, now.second))
  else:
    redirect('/')

@route('/static/<filename:path>')
def send_static(filename):
  return static_file(filename, root='./')

@route('/usermng')
def mng_user():
  if not act_user:
    redirect('/')
  else:
    if act_user.is_admin:
      return template('./management_front_end/view/user_mng.tpl',
                      is_admin=(act_user.is_admin))
    else:
      redirect('/restricted')

@route('/add_user', method="POST")
def add_user():
  if act_user.is_admin:
    usrname = request.forms.get("username")
    passwd = request.forms.get("password")
    email = request.forms.get("useremail")
    nickname = request.forms.get("name")
    sex = request.forms.get("sex")
    print usrname, passwd, email, nickname, sex
    usr_db = User.user_db
    try:
      usr_db.cursor.execute('SELECT * FROM users WHERE name=?', (usrname,)).fetchone()
    except:
      usr_db.cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)',
        (usrname, passwd, User.NOT_ADMIN, email, nickname, u"not admin"))
      usr_db.commit()
      redirect('/index/%s'%(act_user.usrname,))
    else: # user existing
      return "用户名%s已存在，请重试！"%usrname
  else:
    redirect('/restricted')

@route('/delete_user', method="POST")
def delete_user():
  if act_user.is_admin:
    usrname = request.forms.get("username")
    usr_db = User.user_db
    usr_db.cursor.execute('DELETE FROM users WHERE name=?', (usrname,))
    usr_db.commit()
    print usrname, 'has been deleted from DB'
    redirect('/index/%s'%(act_user.usrname,))

@route("/gamemng")
def mng_game():
  if act_user is not None:
    return template('./management_front_end/view/game_mng.tpl',
                    username=act_user.usrname, is_admin=act_user.is_admin)
  else:
    goto_login()

@route("/pricingmng")
def mng_pricing():
  if act_user is not None:
    return "敬请期待。。。"
  else:
    goto_login()

@route("/statistics")
def stat_mng():
  if act_user is not None:
    return "敬请期待。。。"
  else:
    goto_login()

@route("/notification")
def notif_mng():
  if act_user is not None:
    return "敬请期待。。。"
  else:
    goto_login()

@route('/test_temp')
def test_temp():
  myGames = [('hostA', '192.168.0.1', 'basketball', 'running'),
           ('hostA', '192.168.0.1', 'basketball', 'running'),]
  return template('./management_front_end/usr_mgr/test_temp.tpl', games=myGames)

@route("/start_game/<host>/<game>", method="POST")
def start_app(host, game):
  global apps
  f = urllib2.urlopen('http://192.168.0.4:8080/start_game')
  print f.read()
  f.close()
  redirect('/index/%s'%(user,))

@route("/stop_game/<host>/<game>", method="POST")
def stop_app(host, game):
  global apps
  f = urllib2.urlopen('http://192.168.0.4:8080/stop_game')
  print f.read()
  f.close()
  redirect('/%s/index'%(user))

@route('/restricted')
def restricted():
  abort(401, "对不起，您没有管理员权限！请联系管理员！")

def goto_login():
  redirect('/')


def main():
  # add admin as default user
  admin = User('admin', '000000', email='admin@mhg.org', desc=u'管理员', is_admin=User.IS_ADMIN)
  usr_db = User.user_db
  usr_db.create_table('users',
    '(name text, passwd text, admin integer, email text, nickname text, desc text)')
  c = usr_db.cursor
  try:
    c.execute('SELECT * FROM users WHERE name=?', (admin.usrname,)).fetchone()
  except:
    c.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)',
      (admin.usrname, admin.password, admin.is_admin, admin.email, admin.nickname, admin.desc))
    usr_db.commit()
  else:
    print "admin already existed"

  run(host='0.0.0.0', port=80, Debug=True, reloader=False)
  #run(host='localhost', port=80, Debug=True)

if __name__ == '__main__':
  main()
