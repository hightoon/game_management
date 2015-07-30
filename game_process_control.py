#!/usr/bin/python
#-* encoding: utf-8 *-

import time
import win32api, win32con
from subprocess import Popen
from bottle import route, request, get, post, run
from SendKeys import SendKeys
running_game = None

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

@route('/start_game')
def start_game():
    global running_game
    game = Game("D:\\GameManagememt\\[vrword.cn]超级篮球\\Baskhead v0.1\\Baskhead", "BaskHead")
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

def mouse_click(x, y):
    pass

def run_svr():
    run(host='192.168.0.4', port=8080, debug=True)

def main():
    scrn_w = win32api.GetSystemMetrics(0)
    scrn_h = win32api.GetSystemMetrics(1)
    game = Game("D:\GameManagememt\玩家体验测试时间隧道2\Doctor_Who_Time_Tunnel-pc\Tardis", "Tardis")
    game.start()
    time.sleep(1)
    #SendKeys("{ENTER}")
    #time.sleep(10)
    #game.stop()
    win32api.SetCursorPos([scrn_w/2, scrn_h/2])
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

if __name__ == '__main__':
    #run_svr()
    main()