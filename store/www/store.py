#!/usr/bin/python
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


# index
@app.route('/')
def index():
        ipaddr = request.environ.get('X-Real-IP3')
        log.info('index ip is %s'%ipaddr)
        index_html = read_file('templates/index.html')
        return index_html


# 用户注册
@app.route('/register')
def register():
	register_html = read_file("templates/register.html")
	return register_html

@app.route('/api/v1/register')
def register():
        cellphone = request.forms.get('cellphone')
        checkret = checkCellphone(cellphone)
        if checkret == -1:
            return red_writing_2(u'该手机号已注册','/login',u'点击登录','/',u'点击返回主页')
        if checkret == -2:
            return red_writing_1(u'手机号格式不正确','/register',u'点击重新输入')
        


# 商品分类
@app.route('/product_list')
def product_list():  
        return red_writing_1(u'功能开发中','/',u'点击返回')   

# 购物车
@app.route('/shopping_cart')
def shopping_cart():
        return red_writing_1(u'功能开发中','/',u'点击返回')

# 个人中心
@app.route('/user_list')
def user_list():
        return red_writing_1(u'功能开发中','/',u'点击返回')




@app.error(404)
def err(err):
	return red_writing_1(u'页面不存在','/',u'点击返回')

@app.error(405)
def err(err):
	return red_writing_1(u'访问方式不正确','/',u'点击返回')

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
