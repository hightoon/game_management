#!/usr/bin/python
#-* encoding: utf-8 *-

import time
from subprocess import Popen
from bottle import route, request, get, post, run

running_games = None

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

@post('/start_game')
def start_game():
    global running_game
    game = Game("D:\\GameManagememt\\[vrword.cn]³¬¼¶ÀºÇò\\Baskhead v0.1\\Baskhead", "BaskHead")
    game.start()
    if running_game:
        running_game.stop()
    running_game = game

@post('/stop_game')
def stop_game():
    global running_game
    if running_game:
        running_game.stop()
        running_game = None

def run_svr():
    run(host='192.168.0.4', port=8080, debug=True)

def main():
    game = Game("D:\\GameManagememt\\[vrword.cn]³¬¼¶ÀºÇò\\Baskhead v0.1\\Baskhead", "BaskHead")
    game.start()
    time.sleep(10);
    print game.get_status()
    time.sleep(10)
    game.stop()

if __name__ == '__main__':
    run_svr()