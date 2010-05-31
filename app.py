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
    (r"/",     views.PlayHandler),
]


settings = {
    'cookie_secret': 'efd2d36fe8255807e998e660f7a53d71',
    'debug': True,
    'auto_reload': True,
    'user_agent': 'LearnList/1.0 +http://learnlist.com/',
    'youtube_api_key': 'AI39si4rAd8kCv__-DDgXRf2SdQSvVJOCa5VSuuET37SJRtm7O4iqeQ63hggCt8lpDmU7HxWl-ejeKldy0-aeLUkoeKe1Bb6Xw',
}


app = tornado.web.Application(urls, **settings)
