
import tornado.web
from tornado import ioloop

import os
import time

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', addr='', file='')

def fileplay(addr):
    pass

class PlayHandler(tornado.web.RequestHandler):
    wget_pid = None
    mplayer_pid = None
    chrome_pid = None

    def play(self, addr):
        try:
            pid = open("/tmp/.X3-lock", 'r').read().strip()
            print 'killing pid:', pid
            os.kill(int(pid), 9)
        except (IOError, OSError):
            pass

        try:
            os.unlink("/tmp/.X3-lock")
        except OSError:
            pass

        addr = addr.replace('https://amnesia.mit.edu/oblivious/Movies/',
                            'https://marcos:pizzicato@amnesia.mit.edu/oblivious/Movies/')

        #addr = addr.replace('http://www.youtube.com/watch?',
        #                    'http://www.youtube.com/watch_videos?

        if PlayHandler.wget_pid:
            os.killpg(PlayHandler.wget_pid, 9)
            wget_pid = None
        if PlayHandler.chrome_pid:
            os.kill(PlayHandler.chrome_pid, 9)
            chrome_pid = None

        if addr.endswith('.avi'):
            PlayHandler.wget_pid = os.fork()
            if PlayHandler.wget_pid == 0:
                os.system('wget -q \'%s\' --no-check-certificate -O - | mplayer -fs -cache 8192 -' % addr)
        else:
            PlayHandler.chrome_pid = os.fork()
            if PlayHandler.chrome_pid == 0:
                os.execvpe('google-chrome', ['google-chrome', '--app=%s' % addr], { 'DISPLAY': ':0' })
        # run Xephyr
        #if os.fork() == 0:
        #    os.execvpe("Xephyr", ['Xephyr', ':3', '-ac', '-reset', '-terminate'], {})
        #time.sleep(2)
        # start google-chrome with addr fullscreen
        #if os.fork() == 0:
        #    os.execvpe('google-chrome', [addr], { 'DISPLAY': ':3' })

    def get(self):
        addr = self.get_argument('addr', None)
        file = self.get_argument('file', None)
        if addr:
            self.play(addr)
        elif file:
            fileplay(file)
        self.render('index.html', addr=addr, file=file)
