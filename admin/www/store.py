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


# index
@app.route('/')
def index():
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        if check_login(name, ADMINPASSW) == -1:
            return red_writing_1(u'用户尚未登录','/login',u'点击登录')
        ipaddr = request.environ.get('X-Real-IP')
        log.info('index ip is %s'%ipaddr)
        index_html = read_file('templates/index.html')
        return index_html


# login 
@app.route('/login')
def login_page():
	login_html = read_file("templates/login.html")
	return login_html

@app.route('/api/v1/login', method="POST")
def apilogin():
        name = request.forms.get('name')
        password = request.forms.get('password')
        checkret = check_login(name, password)
        if checkret == -1:
           return red_writing_1(u'用户名密码不正确','/login',u'点击重新登录')
        response.set_cookie('cookie_name', name, secret = 'asf&*457', domain='114.67.224.92', path = '/')
        redirect('/')


# 产品管理
@app.route('/product_list')
def list():
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        if check_login(name, ADMINPASSW) == -1:
            return red_writing_1(u'用户尚未登录','/login',u'点击登录')
        

@app.route('/product_add')
def add():
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        if check_login(name, ADMINPASSW) == -1:
            return red_writing_1(u'用户尚未登录','/login',u'点击登录')
        ipaddr = request.environ.get('X-Real-IP')
        log.info('product_add ip is %s'%ipaddr)
        proadd_html = read_file('templates/product_add.html')
        return proadd_html

@app.route('/api/v1/product_add', method='POST')
def apiadd():
        name = request.forms.get('name')
        name = name.strip()
        num = request.forms.get('num')
        price = request.forms.get('price')
        discount = request.forms.get('discount')
        description = request.forms.get('description')
        pic = request.files.get('pic')
        proret = saveproduct(name, num, price, discount, description, pic)
        if proret == -1:
            return red_writing_1(u'价格,折扣价格,数量必须是数字','/product_add',u'点击返回主页')
        if proret == -2:
            return red_writing_1(u'产品名格式不正确','/product_add',u'点击返回主页')
        if proret == -3:
            return red_writing_1(u'产品存在','/product_add',u'点击返回主页')
        if proret == -4:
            return red_writing_1(u'缩略图错误','/product_add',u'点击返回主页')
        nid = proret
        picret = saveImage(name, pic, nid)
        if picret == -1:
            return red_writing_1(u'图片格式不是常用图片格式','/',u'点击返回主页')
        return red_writing_1(u'产品录入成功','/list',u'点击返回主页')

 
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
