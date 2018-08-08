#!/usr/bin/python
# -*- coding: UTF-8 -*-
from bottle import route, run, static_file,request
import bottle,os.path,base64,io,struct
import sys
sys.path.append('../')
sys.path.append('/root')
from log import *
from config import *
from PIL import Image



app = application = bottle.Bottle()
@app.route('/')
def store():
        return('1111111111')
     

class StripPathMiddleware(object):

    def __init__(self, a):
        self.a = a
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.a(e, h)

if __name__ == '__main__':
    bottle.run(
        host='127.0.0.1',
        port='10071',
        app=StripPathMiddleware(app),
        reloader=True,
        debug=True
        )
