
import tornado.web
from tornado import ioloop

from Phidgets.PhidgetException import *
from Phidgets.Events.Events import *
from Phidgets.Devices.InterfaceKit import *

import os
import sys
import time
import urllib
import urlparse

interfaceKit = InterfaceKit()
interfaceKit.openPhidget()
try:
    interfaceKit.waitForAttach(10000)
except:
    print "Cannot connect to Phidgets!"
    sys.exit(1)


class PlayHandler(tornado.web.RequestHandler):
    wget_pid = None
    mplayer_pid = None
    chrome_pid = None
    xrandr_pid = None

    def kill_helpers(self):
        if PlayHandler.wget_pid:
            os.kill(PlayHandler.wget_pid, 9)
            wget_pid = None
        if PlayHandler.mplayer_pid:
            os.kill(PlayHandler.mplayer_pid, 9)
            mplayer_pid = None
        if PlayHandler.chrome_pid:
            os.kill(PlayHandler.chrome_pid, 9)
            chrome_pid = None
        if PlayHandler.xrandr_pid:
            os.kill(PlayHandler.xrandr_pid, 9)
            xrandr_pid = None

        try:
            os.unlink("/tmp/vidfifo")
        except OSError:
            pass
        try:
            os.mkfifo("/tmp/vidfifo")
        except OSError:
            pass


    def play_mplayer(self, filename):
        os.system("killall -9 mplayer")
        PlayHandler.mplayer_pid = os.fork()
        if PlayHandler.mplayer_pid == 0:
            args = ['mplayer', '-idx', '-fs', '-cache', '8192', filename]
            os.execvp('mplayer', args)


    def play(self, addr):
        addr = addr.replace('http://www.youtube.com/watch?',
                            'http://www.youtube.com/watch_popup?')

        addr_parse = urlparse.urlparse(addr)
        addr_info = urllib.urlopen(addr).info()

        if addr_info.gettype() == 'application/octet-stream' or \
                addr_info.getmaintype() == 'video':
            PlayHandler.wget_pid = os.fork()
            if PlayHandler.wget_pid == 0:
                os.execvp('wget', ['-q', addr, '--no-check-certificate', '-O', '/tmp/vidfifo'])
            self.play_mplayer('/tmp/vidfifo')
        else:
            PlayHandler.chrome_pid = os.fork()
            if PlayHandler.chrome_pid == 0:
                os.execvpe('google-chrome', ['google-chrome', '--app=%s' % addr], { 'DISPLAY': ':0' })

    def projector_cycle(self):
        if not interfaceKit.getOutputState(0):
            interfaceKit.setOutputState(0,1)
            time.sleep(16)
        self.display_cycle()

    def display_cycle(self):
        os.system('xrandr --output VGA1 --mode 1360x768') # turn on
        PlayHandler.xrandr_pid = os.fork()
        if PlayHandler.xrandr_pid == 0:
            if PlayHandler.mplayer_pid:
                os.wait(PlayHandler.mplayer_pid)
            else:
                # XXX: find out when browser video ends
                time.sleep(60 * 15)
            os.system('xrandr --output VGA1 --off') # turn off
            interfaceKit.setOutputState(0,0)
            sys.exit(0)

    def post(self):
        name = self.get_argument('file.name')
        path = self.get_argument('file.path')
        print "XXX", 'name=%s, path=%s' % (name, path)
        print "XXX path size =", os.stat(path).st_size

        self.kill_helpers()
        self.projector_cycle()
        self.play_mplayer(path)

        self.redirect('/?file=%s' % name)

    def get(self):
        addr = self.get_argument('addr', '')
        if addr:
            self.kill_helpers()
            self.projector_cycle()
            self.play(addr)
        self.render('index.html', addr=addr, file=self.get_argument('file', ''))
