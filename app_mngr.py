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
daily_running_stat = {}
tot_game_runnings = 0
login_timestamps = {}

# database manipulation
class GMDatabase:
  def __init__(self, dbfile='default.db'):
    self.dbfile = dbfile
    self.conn = sqlite3.connect(dbfile)
    self.conn.text_factory = str

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

def parse_line(s):
  return s.split()

def get_hosts():
  hosts = []
  fd = open('hosts.txt')
  for ln in fd:
    hosts.append(parse_line(ln))
  fd.close()
  return hosts

def get_games():
  games = []
  fd = open('games.txt')
  for ln in fd:
    games.append(parse_line(ln))
  fd.close()
  return games

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
    if username not in daily_running_stat.keys():
      daily_running_stat[username] = 0
    now = datetime.now()
    login_timestamps[username] = "%02d:%02d:%02d"%(now.hour, now.minute, now.second)
    #if isadmin == User.IS_ADMIN:
    #  redirect('/index/admin')
    #else:
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

@route('/change_passwd', method="POST")
def change_passwd():
  redirect('/change_password')

@route('/change_password')
def change_password():
  if act_user is not None:
    return template('./management_front_end/change_password.tpl')
  else:
    redirect('/')

@route('/change_password', method="POST")
def change_password():
  if act_user is not None:
    username = request.forms.get('username')
    new_password = request.forms.get('password_new')
    confirm_password = request.forms.get('password_confirm')
    if new_password != confirm_password:
      return "两次密码输入不一致，请返回重新输入！"
    else:
      cur = User.user_db.cursor
      cur.execute('UPDATE users SET passwd=? WHERE name=?',
                  (new_password, act_user.usrname,))
      User.user_db.commit()
      cur.close()
      redirect('/')
  else:
    redirect('/')

@route('/index/<username>')
def user_index(username):
  if act_user is not None and act_user.usrname == username:
    now = datetime.now()
    usrinfo = []
    for usr in daily_running_stat.keys():
      usrinfo.append((usr, daily_running_stat[usr], login_timestamps[usr]))
    return template('./management_front_end/admin_mngm/index',
                    is_admin=act_user.is_admin, username=act_user.usrname,
                    nowtime="%02d:%02d:%02d"%(now.hour, now.minute, now.second),
                    tot_game_ops=tot_game_runnings,
                    num_of_ops=daily_running_stat[act_user.usrname],
                    usrinfo=usrinfo)
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
                      is_admin=act_user.is_admin,
                      tot_game_ops=tot_game_runnings,
                      num_of_ops=daily_running_stat[act_user.usrname],
                      username=act_user.usrname)
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
      existing_user = \
        usr_db.cursor.execute('SELECT * FROM users WHERE name=?', (usrname,)).fetchone()
    except Exception as e:
      return e
    else: # user existing
      if existing_user is None:
        usr_db.cursor.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)',
          (usrname, passwd, User.NOT_ADMIN, email, nickname, u"not admin"))
        usr_db.commit()
        redirect('/index/%s'%(act_user.usrname,))
      else:
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
    hosts = get_hosts()
    games = get_games()
    return template('./management_front_end/view/game_mng.tpl',
                    username=act_user.usrname, is_admin=act_user.is_admin,
                    tot_game_ops=tot_game_runnings,
                    num_of_ops=daily_running_stat[act_user.usrname],
                    hosts=hosts, games=games)
  else:
    goto_login()

@route("/game_control", method="POST")
def control_game():
  print 'start game remote control'
  if act_user is not None:
    host = request.forms.get("host")
    game = request.forms.get("game")
    op = request.forms.get("op")
    print host, game, op
    if op == 'start':
      #inc_num_of_ops(act_user.usrname)
      if act_user.usrname in daily_running_stat.keys():
        daily_running_stat[act_user.usrname] = \
          daily_running_stat[act_user.usrname] + 1
      else:
        daily_running_stat[act_user.usrname] = 1
      f = urllib2.urlopen('http://%s:8080/mc_start_game'%(host,))
      print f.read()
      f.close()
    elif op == 'stop':
      f = urllib2.urlopen('http://%s:8080/mc_stop_game'%(host,))
      print f.read()
      f.close()

    #calc tot runnings
    global tot_game_runnings
    tot_game_runnings = sum(daily_running_stat.values())
    redirect('/index/%s'%(act_user.usrname,))

@route("/pricingmng")
def mng_pricing():
  if act_user is not None:
    return template('./management_front_end/view/price_mng.tpl',
                    username=act_user.usrname, is_admin=act_user.is_admin,
                    tot_game_ops=tot_game_runnings,
                    num_of_ops=daily_running_stat[act_user.usrname])
  else:
    goto_login()

@route("/change_price", method="POST")
def change_price():
  shop_name = request.forms.get('shopname')
  host_name = request.forms.get('hostname')
  game_name = request.forms.get('gamename')
  timing    = request.forms.get('gametiming')
  price     = request.forms.get('price')
  todo

@route("/statistics")
def stat_mng():
  if act_user is not None:
    return "敬请期待。。。"
  else:
    goto_login()

@route("/notification")
def notif_mng():
  if act_user is not None:
    news="""
    青年朋友们：

　　值此中华全国青年联合会第十二届委员会全体会议和中华全国学生联合会第二十六次代表大会开幕之际，我代表党中央，向大会的召开表示热烈的祝贺！向全国各族各界青年和青年学生、向广大海外中华青年，表示诚挚的问候！

　　紧跟时代砥砺前行，担当责任奋发有为，是我国青年的光荣传统，也是党和人民对广大青年的殷切期望。5年来，在党的坚强领导和共青团帮助指导下，各级青联和学联组织围绕中心、服务大局，积极组织青年、宣传青年、教育青年、引导青年，各项工作取得可喜成绩。广大青年和青年学生响应党的号召，胸怀祖国和人民，奉献社会和他人，积极投身坚持和发展中国特色社会主义伟大实践，以实际行动证明，当代中国青年不愧为大有希望、大有作为的一代。

　　“士不可以不弘毅，任重而道远。”国家的前途，民族的命运，人民的幸福，是当代中国青年必须和必将承担的重任。一代青年有一代青年的历史际遇。我们的国家正在走向繁荣富强，我们的民族正在走向伟大复兴，我们的人民正在走向更加幸福美好的生活。当代中国青年要有所作为，就必须投身人民的伟大奋斗。同人民一起奋斗，青春才能亮丽；同人民一起前进，青春才能昂扬；同人民一起梦想，青春才能无悔。
    """
    return template('./management_front_end/view/notif_mng.tpl',
                    username=act_user.usrname, is_admin=act_user.is_admin,
                    latest_news=news, tot_game_ops=tot_game_runnings,
                    num_of_ops=daily_running_stat[act_user.usrname])
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

def inc_num_of_ops(usrname):
  cur = User.op_db.cursor
  op_num = cur.execute('SELECT * FROM game_op WHERE usrname=?', (usrname,)).fetchone()[1]
  print op_num
  cur.execute('UPDATE game_op SET num_of_ops = ? WHERE usrname=?', (op_num+1, usrname))
  cur.close()

def main():
  # add admin as default user
  admin = User('admin', '000000', email='admin@mhg.org', desc=u'管理员', is_admin=User.IS_ADMIN)
  usr_db = User.user_db
  usr_db.create_table('users',
    '(name text, passwd text, admin integer, email text, nickname text, desc text)')
  #User.op_db.create_table('game_op',
  #  '(usrname text primary key, integer num_of_ops)')
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
