#!/usr/local/python3
# -*- coding: UTF-8 -*-

import bottle
import os
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
from store_user import *
from bottle import *


app = application = bottle.Bottle()



@app.route('/product_add')
def store():
        ipaddr = request.environ.get('X-Real-IP')
        log.info('product_add ip is %s'%ipaddr)
        proadd_html = read_file('templates/product_add.html')
        return proadd_html

@app.route('/api/v1/product_add', method='POST')
def store():
        name = request.forms.get('name')
        num = request.forms.get('num')
        price = request.forms.get('price')
        discount = request.forms.get('discount')
        description = request.forms.get('description')
        pic = request.files.get('pic')
        x = pic.file
        log.info('x is %s'%x)
        saveret = saveImage(name, pic)
        if saveret == -1:
            return red_writing_1(u'图片格式不是常用图片格式','/',u'点击返回主页')
        

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
