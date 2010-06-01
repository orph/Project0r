
import tornado.web
from tornado import ioloop

import multiprocessing
import os
import sys
import time
import urllib
import urlparse


class PlayHandler(tornado.web.RequestHandler):
    wget_pid = None
    mplayer_pid = None
    chrome_pid = None

    def kill_helpers(self):
        if PlayHandler.wget_pid:
            os.kill(PlayHandler.wget_pid, 9)
            wget_pid = None
        if PlayHandler.mplayer_pid:
            os.kill(PlayHandler.mplayer_pid, 9)
            wget_pid = None
        if PlayHandler.chrome_pid:
            os.kill(PlayHandler.chrome_pid, 9)
            chrome_pid = None

        try:
            os.unlink("/tmp/vidfifo")
        except OSError:
            pass
        try:
            os.mkfifo("/tmp/vidfifo")
        except OSError:
            pass


    def kill_xephyr(self):
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


    def play_mplayer(self, filename):
        os.system("killall -9 mplayer")
        PlayHandler.mplayer_pid = os.fork()
        if PlayHandler.mplayer_pid == 0:
            args = ['mplayer', '-idx', '-cache', '8192', filename]
            os.execvp('mplayer', args)


    def play(self, addr):
        addr = addr.replace('https://amnesia.mit.edu/oblivious/',
                            'https://marcos:pizzicato@amnesia.mit.edu/oblivious/')
        addr = addr.replace('http://www.youtube.com/watch?',
                            'http://www.youtube.com/watch_popup?')

        addr_parse = urlparse.urlparse(addr)

        self.kill_helpers()

        if urllib.urlopen(addr).info().gettype() == 'application/octet-stream':
            PlayHandler.wget_pid = os.fork()
            if PlayHandler.wget_pid == 0:
                os.execvp('wget', ['-q', addr, '--no-check-certificate', '-O', '/tmp/vidfifo'])
            self.play_mplayer('/tmp/vidfifo')
        else:
            PlayHandler.chrome_pid = os.fork()
            if PlayHandler.chrome_pid == 0:
                os.execvpe('google-chrome', ['google-chrome', '--app=%s' % addr], { 'DISPLAY': ':0' })

    def post(self):
        name = self.get_argument('file.name')
        path = self.get_argument('file.path')
        print "XXX", 'name=%s, path=%s' % (name, path)

        print "XXX path size =", os.stat(path).st_size

        self.kill_helpers()
        self.play_mplayer(path)

        self.redirect('/?file=%s' % name)

    def get(self):
        addr = self.get_argument('addr', '')
        if addr:
            self.play(addr)
        self.render('index.html', addr=addr, file=self.get_argument('file', ''))
