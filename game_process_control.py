#!/usr/bin/python
#-* encoding: utf-8 *-

import time
import win32api, win32con
from subprocess import Popen
from bottle import route, request, get, post, run
#from SendKeys import SendKeys
running_game = None
is_on_game_page = False

class Game(object):
    def __init__(self, path, name):
        self._path = path
        self._name = name
        self._process  = None
        self._running = False
        self._pause   = False

    def start(self):
        self._process = Popen(self._path, shell=False)
        self._running = True

    def stop(self):
        if self._process:
            self._process.terminate()

    def get_status(self):
        if self._running:
            return self._process.poll()

@route('/start_game/')
def start_game():
    global running_game
    game = Game("D:\\GameManagememt\\[vrword.cn]��������\\Baskhead v0.1\\Baskhead", "BaskHead")
    game.start()
    if running_game:
        running_game.stop()
    running_game = game
    return 'baskhead'

@route('/stop_game')
def stop_game():
    global running_game
    if running_game:
        running_game.stop()
        running_game = None
    return 'ok'

@route('/mc_start_game/<game_path>')
def mc_start_game(game_path):
  print game_path
  if game_path.startswith('pos'):
    pos = int(game_path[4:])
    if not is_on_game_page:
      enter_game_page()
      time.sleep(0.5)
    mc_choose_game(pos)
    time.sleep(0.5)
    mc_click_start_button()
  elif game_path.startswith('dir'):
    global running_game
    path = game_path[4:].replace('|', '\\').replace('_', ' ')
    print path
    game = Game(path, "anonymous")
    game.start()
    if running_game:
        running_game.stop()
    running_game = game
  else: 
    print 'game path not valid'
    return 'nok'
  return 'ok'

@route('/mc_stop_game')
def mc_stop_game():
  print 'stop game'
  global running_game
  if running_game:
    running_game.stop()
    running_game = None
    return 'ok'
  time.sleep(0.5)
  mc_stop_game()
  return 'ok'
  
@route('/press_keyboards/space', method='POST')
def press_space():
  win32api.keybd_event(32, 0, 0, 0)
  win32api.keybd_event(32, 0, win32con.KEYEVENTF_KEYUP, 0)
  print 'space pressed'
  return 'ok'
  
@route('/press_keyboards/enter', method='POST')
def press_enter():
  win32api.keybd_event(13, 0, 0, 0)
  win32api.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
  print 'enter pressed'
  return 'ok'

def get_host():
  #fd = open('client_host.txt')
  #host = fd.read()
  #fd.close()
  #return host
  pass

def run_svr():
  host = get_host()
  print host
  run(host='0.0.0.0', port=8081, debug=True)

def mc_click_left():
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

def mc_click_start_button():
  scrn_w = win32api.GetSystemMetrics(0)
  scrn_h = win32api.GetSystemMetrics(1)
  win32api.SetCursorPos([scrn_w*2/5, scrn_h/2])
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

def mc_click_stop_button():
  scrn_w = win32api.GetSystemMetrics(0)
  scrn_h = win32api.GetSystemMetrics(1)
  win32api.SetCursorPos([scrn_w*13/14, scrn_h/2])
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

def enter_game_page():
  scrn_w = win32api.GetSystemMetrics(0)
  scrn_h = win32api.GetSystemMetrics(1)
  win32api.SetCursorPos([scrn_w*2/3, scrn_h/2])
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
  win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
  is_on_game_page = True

def mc_stop_game():
  #SendKeys("{ESC}")
  win32api.keybd_event(27,0,0,0)
  win32api.keybd_event(27,0, win32con.KEYEVENTF_KEYUP,0)
  time.sleep(10)
  mc_click_stop_button()

def mc_choose_game(position):
  resol_w = win32api.GetSystemMetrics(0)/5
  resol_h = win32api.GetSystemMetrics(1)/8
  offset_h = win32api.GetSystemMetrics(1)/16
  #goto_top
  win32api.SetCursorPos([resol_w, resol_h*1+offset_h])
  mc_click_left()
  for i in range(16):
    # press pageup key
    win32api.keybd_event(33, 0, 0, 0)
    win32api.keybd_event(33, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.1)
  if position < 8:
    win32api.SetCursorPos([resol_w, resol_h*position+offset_h])
    mc_click_left()
  else:
    win32api.SetCursorPos([resol_w, resol_h*7+offset_h])
    mc_click_left()
    #invoke kb resp by press down arrow twice
    for i in range(2):
      win32api.keybd_event(34, 0, 0, 0)
      win32api.keybd_event(34, 0, win32con.KEYEVENTF_KEYUP, 0)
    for i in range(position-7):
      win32api.keybd_event(34, 0, 0, 0)
      win32api.keybd_event(34, 0, win32con.KEYEVENTF_KEYUP, 0)
      time.sleep(0.1)
    win32api.SetCursorPos([resol_w, resol_h*7+offset_h])
    mc_click_left()

def main():
    #scrn_w = win32api.GetSystemMetrics(0)
    #scrn_h = win32api.GetSystemMetrics(1)
    #game = Game("D:\GameManagememt\������������ʱ������2\Doctor_Who_Time_Tunnel-pc\Tardis", "Tardis")
    #game.start()
    time.sleep(8)
    #SendKeys("{ENTER}")
    #time.sleep(10)
    #game.stop()
    if not is_on_game_page:
      enter_game_page()
    time.sleep(3)
    mc_choose_game(1)
    time.sleep(3)
    mc_choose_game(3)
    time.sleep(3)
    mc_choose_game(5)
    time.sleep(3)
    mc_choose_game(7)
    time.sleep(3)
    mc_choose_game(9)
    time.sleep(3)
    mc_choose_game(13)
    time.sleep(3)
    mc_choose_game(15)
    time.sleep(3)

def test_exe_file():
    fd = open('games.txt', 'rb')
    path = ''
    fd.close()
    print path
    g = Game(path, '')
    g.start()
    time.sleep(5)
    g.stop()

if __name__ == '__main__':
    run_svr()
    #main()
    #test_exe_file()
