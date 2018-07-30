#!/usr/local/python3
# -*- coding: UTF-8 -*-

import bottle
import os.path
import base64
import io
import struct
import sys
sys.path.append('../')
sys.path.append('/root')
from log import *
from config import *
from PIL import Image
from store_view import *
from bottle import *
# python3 -m pip install Pillow


app = application = bottle.Bottle()



@app.route('/product_add')
def store():
        #ipaddr = request.environ.get('X-Real-IP')
        #log.info('product_add ip is %s'%ipaddr)
	proadd_html = read_file("templates/product_add.html")
	return proadd_html

@app.route('/api/v1/product_add', method='POST')
def store():
        pic = request.files.get('pic')
        print('type pic is', type(pic))
        print('pic is', pic)
        name, ext = os.path.splitext(pic.filename)
        print('name is', name)
        print('ext is', ext)        
        pic.filename = ''.join(('',ext))
        pic = pic.file.read()
        print('type pic is', type(pic))
        print('pic is', pic)        
        pic.save('/root',overwrite=True)




@app.route('/show')
def show():
        return(store_show)     
 
class StripPathMiddleware(object):

    def __init__(self, a):
        self.a = a
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.a(e, h)

if __name__ == '__main__':
    bottle.run( host='127.0.0.1', port='10070',
                app=StripPathMiddleware(app),
                reloader=True, debug=True
              )
