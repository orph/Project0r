#!/usr/bin/python
# coding=utf-8
#
# main.py --
#       Environment setup, Tornado server initialization
#
#       Copyright © 2009 Beatnik Software, LLC. All rights reserved.
#

import code
import os.path
import logging
import sys
import site
import time

from tornado import httpserver, ioloop, options

import app


options.define('shell', default=False, type=bool, help='Start an interactive shell')
options.parse_command_line()


if __name__ == "__main__":
    if options.options.shell:
        code.interact('Project0r Interactive Shell (Ctrl-D to exit)',
                      local={ '__name__': '__console__' })
        sys.exit(0)

    http_server = httpserver.HTTPServer(app.app)

    logging.info('Starting HTTPServer at http://127.0.0.1:8889')
    if app.settings['debug']:
        http_server.listen(8889)
    else:
        http_server.bind(8889)
        http_server.start() # Forks multiple sub-processes

    ioloop.IOLoop.instance().start()
