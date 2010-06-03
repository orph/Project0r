# coding=utf-8
#
# app.py --
#       Application settings and URLs.
#
#       Copyright © 2009 Beatnik Software, LLC. All rights reserved.
#

import os
import sys

import tornado.web

import views


urls = [
    (r"/",       views.PlayHandler),
    (r"/upload", views.PlayHandler),
]


settings = {
    'cookie_secret': 'f3f65a30dfc94378b7600c4f9e837956',
    'debug': True,
    'auto_reload': True,
    'youtube_api_key': 'AI39si4rAd8kCv__-DDgXRf2SdQSvVJOCa5VSuuET37SJRtm7O4iqeQ63hggCt8lpDmU7HxWl-ejeKldy0-aeLUkoeKe1Bb6Xw',
}


app = tornado.web.Application(urls, **settings)
