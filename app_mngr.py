#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
  Simple web server for local application management, based on bottle framework
  Author: haitong.chen@gmail.com
"""

import time, urllib2, sqlite3
from datetime import datetime, timedelta
from subprocess import Popen
from bottle import route, request, redirect, template,static_file, run

import NewsFeed
# globals for debug purpose
apps = []
act_user = None
daily_running_stat = {}
tot_game_runnings = 0
login_timestamps = {}
game_stats = []
host_ip_name_mapping = {}

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
    except sqlite3.OperationalError as e:
      print e

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
  usr_db_file = 'users.db'
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

class GameStat:
  db_file = 'game_stat.db'
  stat_db = GMDatabase(db_file)
  def __init__(self, user, host, game, reported):
    self.user = user
    self.host = host
    self.game = game
    self.reported = reported
    self.tsformat = '%Y-%m-%d %H:%M:%S'

  def insert2db(self):
    "update game stat info"
    now = datetime.now()
    timestamp = datetime.strftime(now, self.tsformat)
    price = self.get_price(now, self.host, self.game)
    cur = GameStat.stat_db.cursor
    #res = cur.execute('select * from gstat where user=:user and game=:game',\
    #  {'user': user, 'game': game}).ftechone()
    #if res == []:
    #  cur.execute('insert into gstat values (?, ?, ?, ?, ?)',
    #    (user, host, game, start, end, ireported))
    cur.execute('insert into gstat values (?, ?, ?, ?, ?, ?)',
      (self.user, self.host, self.game, price, timestamp, self.reported))
    GameStat.stat_db.commit()
    cur.close()

  @classmethod
  def get_price(self, now, host, game):
    cur = GamePrice.gp_db.cursor
    hostinfo = cur.execute('select * from gameprice where host=? and game=?',\
                  (host, game)).fetchall()
    for h in hostinfo:
      time_range = map(datetime.strptime, h[3].split('-'), ['%H:%M', '%H:%M'])
      if (now.hour*60+now.minute) in \
          range(time_range[0].hour*60+time_range[0].minute,
                time_range[1].hour*60+time_range[1].minute+1):
        return h[2]
    return -1

  @classmethod
  def store_report(self):
    import csv, os
    from ftplib import FTP
    try:
      host, usr, passwd = '120.25.234.94', 'vr', 'vrword.cn'
      #host, usr, passwd = '10.140.162.182', 'codec', '111111'
      ftp = FTP(host)
      ftp.login(usr, passwd)
    except Exception as e:
      print e
      return False
    now = datetime.now()
    today_strf = datetime.strftime(now, '%Y-%m-%d')
    file = today_strf + '.csv'
    start = today_strf + ' 00:00:00'
    end   = today_strf + ' 23:59:59'
    with open(file, 'wb') as f:
      f.write('\xEF\xBB\xBF')
      writer = csv.writer(f)
      header = ('店员', '主机', '游戏', '价格', '时间', '是否上报')
      writer.writerow(header)
      conn = sqlite3.connect(GameStat.db_file)
      conn.text_factory = str
      cur = conn.cursor()
      cur.execute('select * from gstat where datetime(timestamp) between datetime(?) and datetime(?)',\
        (start, end))
      writer.writerows(cur.fetchall())
      cur.close()
      conn.close()
    ftp.storbinary('STOR ' + file, open(file, 'rb'))
    ftp.quit()
    return True

class GamePrice():
  db_file = 'game_price.db'
  gp_db = GMDatabase(db_file)

  def __init__(self, host, game, price, period, shop):
    self.host = host
    self.game = game
    self.price = price
    self.period = period
    self.shop = shop

  def insert2db(self):
    cur = GamePrice.gp_db.cursor
    res = cur.execute('select * from gameprice where host=:host and game=:game and period=:period',\
      {'host': self.host, 'game': self.game, 'period':self.period}).fetchone()
    if res is None:
      print 'insert item into gameprice'
      cur.execute('insert into gameprice values (?, ?, ?, ?, ?)',
        (self.host, self.game, self.price, self.period, self.shop))
    else:
      print 'update gameprice'
      cur.execute('update gameprice set price=? where host=? and game=? and period=?',
        (self.price, self.host, self.game, self.period))
    GamePrice.gp_db.commit()
    cur.close()

class GameState():
  db_file = 'game_states.db'
  gs_db = GMDatabase(db_file)

  def __init__(self, host, game, state='idle'):
    self.host = host
    self.game = game
    self.state = state
    self.timeformat = '%Y-%m-%d %H:%M:%S'

  def insert2db(self):
    now = datetime.strftime(datetime.now(), self.timeformat)
    cur = GameState.gs_db.cursor
    games = cur.execute('replace into gamestate values (?, ?, ?, ?)',
                        (self.host, self.game, self.state, now))
    GameState.gs_db.commit()
    cur.close()

def parse_line(s):
  res = s.split()
  return res[0], ' '.join(res[1:])

def get_hosts():
  hosts = []
  fd = open('hosts.txt')
  for ln in fd:
    hosts.append(parse_line(ln))
  fd.close()
  return hosts

def get_host_by_name(name):
  for h in get_hosts():
    if h[0] == name:
      return h[1]
  return None

def get_games():
  games = []
  fd = open('games.txt')
  for ln in fd:
    games.append(parse_line(ln))
  fd.close()
  return games

def get_game_path_by_name(name):
  for game in get_games():
    if game[0] == game:
      return game[1]
  return None

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
  print request.get('REMOTE_ADDR'), ' connected'
  forgot = None
  username = request.forms.get('username')
  password = request.forms.get('password')
  forgot = request.forms.get('forget_passwd')
  print username, password
  if forgot:
    print 'sending password to %s'%(username,)
    mail_passwd_to(username)
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

def mail_passwd_to(usr):
  import smtplib
  cur = User.user_db.cursor
  cur.execute('select * from users where name=?', (usr,))
  res = cur.fetchone()
  if res is None:
    return '用户不存在，请联系管理员添加用户！'
  else:
    _, passwd, _, email, _, _ = res
    fromaddr = 'bbs@vrword.cn'
    toaddrs = [email]
    msg = ("From: %s\r\nTo: %s\r\n\r\n"
       % (fromaddr, ", ".join(toaddrs)))
    msg = msg + '您好，您的VR游戏关系系统登录密码为%s'%passwd
    server = smtplib.SMTP('smtp.vrword.cn')
    #server.set_debuglevel(1)
    svr.login('bbs@vrword.cn', 'lovexue1314.com')
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

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
                    usrinfo=usrinfo, news_title=NewsFeed.title)
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
                      username=act_user.usrname, news_title=NewsFeed.title)
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
    cur = GameState.gs_db.cursor
    running_games = cur.execute('select * from gamestate where state=?', ('running',)).fetchall()
    running_pairs = []
    idle_ip_hosts = []
    running_hosts = []
    for game in running_games:
      running_pairs.append((game[0], game[1], get_host_by_name(game[0]),))
      running_hosts.append(game[0])
    for h in hosts:
      if h[0] not in running_hosts:
        idle_ip_hosts.append((h[0], h[1],))
    cur.close()
    return template('./management_front_end/view/game_mng.tpl',
                    username=act_user.usrname, is_admin=act_user.is_admin,
                    tot_game_ops=tot_game_runnings,
                    num_of_ops=daily_running_stat[act_user.usrname],
                    hosts=idle_ip_hosts, game_states=running_pairs,
                    games=games, news_title=NewsFeed.title)
  else:
    goto_login()

@route("/game_control", method="POST")
def control_game():
  if act_user is not None:
    op = request.forms.get("op")
    # check if game price has been set
    # only game with price can be started
    if op == 'start':
      host = request.forms.get("host")
      game = request.forms.get("game")
      print host, game
      for hostinfo in get_hosts():
        if hostinfo[1] == host:
          hostname = hostinfo[0]
          break
      for gameinfo in get_games():
        if gameinfo[1] == game:
          gamename = gameinfo[0]
          break
      if GameStat.get_price(datetime.now(), hostname, gamename) < 0:
        return '游戏价格未设置，请进入<价格管理>界面进行设置，或联系管理员。'
      #inc_num_of_ops(act_user.usrname)
      if act_user.usrname in daily_running_stat.keys():
        daily_running_stat[act_user.usrname] = \
          daily_running_stat[act_user.usrname] + 1
      else:
        daily_running_stat[act_user.usrname] = 1
      try:
        f = urllib2.urlopen('http://%s:8081/mc_start_game/%s'%(host, game),
            timeout=30)
      except Exception as e:
        print 'connect to game client %s failed: %s'%(host, e)
      else:
        print f.read()
        f.close()
        gstate = GameState(hostname, gamename, state='running')
        gstate.insert2db()
        gstat = GameStat(act_user.usrname, hostname, gamename, "no")
        gstat.insert2db()
    elif op == 'stop':
      host, game = tuple(request.forms.get('host').split(':'))
      try:
        f = urllib2.urlopen('http://%s:8081/mc_stop_game'%(get_host_by_name(host),), timeout=20)
      except:
        print 'connect to game client %s failed'%host
      else:
        print f.read()
        f.close()
        gstate = GameState(host, game, state='idle')
        gstate.insert2db()
        gstat = GameStat(act_user.usrname, host, game, "yes")
        gstat.insert2db()
    elif op == 'reset':
      host, game = tuple(request.forms.get('host').split(':'))
      gstate = GameState(host, game, state='idle')
      gstate.insert2db()
    #calc tot runnings
    global tot_game_runnings
    tot_game_runnings = sum(daily_running_stat.values())
    redirect('/index/%s'%(act_user.usrname,))

@route("/pricingmng")
def mng_pricing():
  if act_user is not None:
    hosts = get_hosts()
    games = get_games()
    cur = GamePrice.gp_db.cursor
    price_list = cur.execute('select * from gameprice').fetchall()
    print price_list
    cur.close()
    print price_list
    return template('./management_front_end/view/price_mng.tpl',
                    username=act_user.usrname, is_admin=act_user.is_admin,
                    tot_game_ops=tot_game_runnings,
                    num_of_ops=daily_running_stat[act_user.usrname],
                    hosts=hosts, games=games, price_list=price_list,
                    news_title=NewsFeed.title)
  else:
    goto_login()

@route("/change_price", method="POST")
def change_price():
  if act_user is not None:
    shop = request.forms.get('shopname')
    host = request.forms.get('hostname')
    game = request.forms.get('gamename')
    period    = request.forms.get('gametiming')
    price     = request.forms.get('price')
    try:
      price = float(price)
    except ValueError:
      return '价格格式有误(只能包含数字和小数点)，请返回重新修改!'
    try:
      map(datetime.strptime, period.split('-'), ['%H:%M', '%H:%M'])
    except ValueError:
      return '时间格式有误，请返回重新输入，例如00:00-23:59'
    gp = GamePrice(host, game, float(price), period, shop)
    gp.insert2db()
    redirect('/pricingmng')
  else:
    goto_login()

@route("/statistics")
def stat_mng():
  if act_user is not None:
    cur = GameStat.stat_db.cursor
    now = datetime.now()
    today_strf = datetime.strftime(now, '%Y-%m-%d')
    start = today_strf + ' 00:00:00'
    end   = today_strf + ' 23:59:59'
    gmlist = cur.execute(
      'select * from gstat where datetime(timestamp) between datetime(?) and datetime(?)'
      , (start, end,)).fetchall()
    cur.close()
    gen_gm_lst = {}
    for gm in gmlist:
      if gm[:3] not in gen_gm_lst.keys():
        if gm[4] == 'yes':
          gen_gm_lst[gm[:3]] = (0, 'yes')
        else:
          gen_gm_lst[gm[:3]] = (1, 'no')
      else:
        if gm[4] == 'yes':
          gen_gm_lst[gm[:3]] = (gen_gm_lst[gm[:3]][0], 'yes')
        else:
          gen_gm_lst[gm[:3]] = (gen_gm_lst[gm[:3]][0]+1, 'no')
    gen_gm_info_lst = []
    for k in gen_gm_lst:
      gen_gm_info_lst.append(list(k)+list(gen_gm_lst[k]))
    return template('./management_front_end/view/game_stat.tpl',
        username=act_user.usrname, is_admin=act_user.is_admin,
        tot_game_ops=tot_game_runnings,
        num_of_ops=daily_running_stat[act_user.usrname],
        gminfolist=gen_gm_info_lst, detailed_game_info=gmlist,
        news_title=NewsFeed.title)
  else:
    goto_login()

@route("/statistics", method='POST')
def stat_mng():
  print 'post stat'
  if act_user is not None:
    days = int(request.forms.get('period'))
    order = request.forms.get('order')
    print days, order
    cur = GameStat.stat_db.cursor
    now = datetime.now()
    start = now - timedelta(days=days)
    end = now
    gmlist = cur.execute(
      'select * from gstat where datetime(timestamp) between datetime(?) and datetime(?) order by %s'%order
      , (start, end, )).fetchall()
    cur.close()
    gen_gm_lst = {}
    for gm in gmlist:
      if gm[:3] not in gen_gm_lst.keys():
        if gm[4] == 'yes':
          gen_gm_lst[gm[:3]] = (0, 'yes')
        else:
          gen_gm_lst[gm[:3]] = (1, 'no')
      else:
        if gm[4] == 'yes':
          gen_gm_lst[gm[:3]] = (gen_gm_lst[gm[:3]][0], 'yes')
        else:
          gen_gm_lst[gm[:3]] = (gen_gm_lst[gm[:3]][0]+1, 'no')
    gen_gm_info_lst = []
    for k in gen_gm_lst:
      gen_gm_info_lst.append(list(k)+list(gen_gm_lst[k]))
    return template('./management_front_end/view/game_stat.tpl',
        username=act_user.usrname, is_admin=act_user.is_admin,
        tot_game_ops=tot_game_runnings,
        num_of_ops=daily_running_stat[act_user.usrname],
        gminfolist=gen_gm_info_lst, detailed_game_info=gmlist,
        news_title=NewsFeed.title)
  else:
    goto_login()

@route("/notification")
def notif_mng():
  if act_user is not None:
    news = NewsFeed.desc + '(' + NewsFeed.link + ')'
    return template('./management_front_end/view/notif_mng.tpl',
                    username=act_user.usrname, is_admin=act_user.is_admin,
                    latest_news=news, tot_game_ops=tot_game_runnings,
                    num_of_ops=daily_running_stat[act_user.usrname],
                    news_title=NewsFeed.title)
  else:
    goto_login()

@route('/test_temp')
def test_temp():
  myGames = [('hostA', '192.168.0.1', 'basketball', 'running'),
           ('hostA', '192.168.0.1', 'basketball', 'running'),]
  return template('./management_front_end/usr_mgr/test_temp.tpl', games=myGames)

#------- demo code ---------#
@route("/start_game/<host>/<game>", method="POST")
def start_app(host, game):
  global apps
  f = urllib2.urlopen('http://192.168.0.4:8081/start_game')
  print f.read()
  f.close()
  redirect('/index/%s'%(user,))

@route("/stop_game/<host>/<game>", method="POST")
def stop_app(host, game):
  global apps
  f = urllib2.urlopen('http://192.168.0.4:8081/stop_game')
  print f.read()
  f.close()
  redirect('/%s/index'%(user))
#------- demo code ---------#

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

def create_tables():
  User.user_db.create_table('users',
    '(name text, passwd text, admin integer, email text, nickname text, desc text)')
  GameStat.stat_db.create_table('gstat',
      '(user text, host text, game text, price real, timestamp text, reported text)'
  )
  GamePrice.gp_db.create_table('gameprice',
    '(host text, game text, price real, period text, shop text)')
  GameState.gs_db.create_table('gamestate',
    '(host text, game text, state text, time text, primary key (host, game))')

def drop_tables():
  GameStat.stat_db.cursor.execute('drop table gstat')
  GamePrice.gp_db.cursor.execute('drop table gameprice')
  GameState.gs_db.cursor.execute('drop table gamestate')

# timer
import time
import threading
class Timer(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
  def run(self):
    while True:
      if GameStat.store_report():
        print 'sent report'
        return
      time.sleep(3600)

def main():
  # add admin as default user
  #drop_tables()
  create_tables()
  admin = User('admin', '000000', email='admin@mhg.org', desc=u'管理员', is_admin=User.IS_ADMIN)
  usr_db = User.user_db
  c = usr_db.cursor
  res = c.execute('SELECT * FROM users WHERE name=?', (admin.usrname,)).fetchone()
  if res is None:
    c.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)',
      (admin.usrname, admin.password, admin.is_admin, admin.email, admin.nickname, admin.desc))
    usr_db.commit()
  else:
    print "admin already existed"

  rprtimer = Timer()
  #rprtimer.start()
  run(host='localhost', port=8081, Debug=True, reloader=False)
  #run(host='localhost', port=80, Debug=True)

if __name__ == '__main__':
  main()
