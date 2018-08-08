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
        if checkLogin(name, ADMINPASSW) == -1:
            return red_writing_1(u'用户尚未登录','/login',u'点击登录')
        ipaddr = request.environ.get('X-Real-IP2')
        log.info('index ip is %s'%ipaddr)
        index_html = read_file('templates/index.html')
        return index_html


# login 
@app.route('/login')
def login():
	login_html = read_file("templates/login.html")
	return login_html

@app.route('/api/v1/login', method="POST")
def apiLogin():
        name = request.forms.get('name')
        password = request.forms.get('password')
        checkret = checkLogin(name, password)
        if checkret == -1:
           return red_writing_1(u'用户名密码不正确','/login',u'点击重新登录')
        response.set_cookie('cookie_name', name, secret = 'asf&*457', domain='admin.fish-23.com', path = '/')
        redirect('/')


# 产品管理
@app.route('/product_list')
def list():
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        log.info('222222222222222')
        log.info('product_list name is %s'%name)
        if checkLogin(name, ADMINPASSW) == -1:
            return red_writing_1(u'用户尚未登录','/login',u'点击登录')
        findret = findProduct(name)
        h = listHtml(findret)
        return h          

@app.route('/product_add')
def add():
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        if checkLogin(name, ADMINPASSW) == -1:
            return red_writing_1(u'用户尚未登录','/login',u'点击登录')
        ipaddr = request.environ.get('X-Real-IP2')
        log.info('product_add ip is %s'%ipaddr)
        proadd_html = read_file('templates/product_add.html')
        return proadd_html

@app.route('/api/v1/product_add', method='POST')
def apiAdd():
        user_name = request.get_cookie('cookie_name', secret = 'asf&*457')
        name = request.forms.get('name')
        name = name.strip()
        num = request.forms.get('num')
        price = request.forms.get('price')
        discount = request.forms.get('discount')
        description = request.forms.get('description')
        pic = request.files.get('pic')
        category = request.forms.get('category')
        proret = saveProduct(name, num, price, discount, description, pic, user_name, category)
        if proret == -1:
            return red_writing_1(u'价格,折扣价格,数量必须是正数','/product_add',u'返回')
        if proret == -2:
            return red_writing_1(u'产品名格式不正确','/product_add',u'返回')
        if proret == -3:
            return red_writing_1(u'产品存在','/product_add',u'返回')
        if proret == -4:
            return red_writing_1(u'缩略图错误','/product_add',u'返回')
        product_id = proret[0]
        group_id = proret[1]
        picret = saveImage(name, pic, product_id)
        if picret == -1:
            return red_writing_1(u'图片格式不是常用图片格式','/product_add',u'返回')
        return red_writing_1(u'产品录入成功','/product_list',u'点击进入产品列表')

@app.route('/product_del/<html_nid>')
def lis_del(html_nid):
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        if checkLogin(name, ADMINPASSW) == -1:
            return red_writing_1(u'用户尚未登录','/login',u'点击登录')            
        delProduct(html_nid)  
        return redirect('/product_list')

@app.route('/product_modify/<html_nid>')
def product_modify(html_nid):
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        if checkLogin(name, ADMINPASSW) == -1:
            return red_writing_1(u'用户尚未登录','/login',u'点击登录') 
        listModifyHtml = modifyProduct(html_nid)
        return listModifyHtml

@app.route('/api/v1/product_modify', method='POST')
def product_modify():
        name = request.forms.get('name')
        name = name.strip()
        num = request.forms.get('num')
        price = request.forms.get('price')
        discount = request.forms.get('discount')
        description = request.forms.get('description')
        pic = request.files.get('pic')
        picaddr = request.forms.get('picaddr')
        return red_writing_1(u'功能开发中','/product_list',u'点击返回')

@app.route('/parameters_list/<html_nid>')
def list(html_nid):
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        if checkLogin(name, ADMINPASSW) == -1:
            return red_writing_1(u'用户尚未登录','/login',u'点击登录')
        findret = findParameters(html_nid)
        product_nid = html_nid
        h = parametersHtml(findret, product_nid)
        return h

@app.route('/parameters_add/<product_nid>')
def add(product_nid):
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        if checkLogin(name, ADMINPASSW) == -1:
            return red_writing_1(u'用户尚未登录','/login',u'点击登录')
        ipaddr = request.environ.get('X-Real-IP2')
        log.info('product_add ip is %s'%ipaddr)
        paramadd_html = read_file('templates/parameters_add.html')
        response.set_cookie('product_nid', product_nid, secret = 'asf&*458', domain='admin.fish-23.com', path = '/')
        return paramadd_html

@app.route('/api/v1/parameters_add', method='POST')
def apiAdd():
        product_nid = request.get_cookie('product_nid', secret = 'asf&*458')
        num = request.forms.get('num')
        price = request.forms.get('price')
        discount = request.forms.get('discount')
        description = request.forms.get('name')
        pararet = saveParameters(product_nid, num, price, discount, description)
        if pararet == -1:
            return red_writing_1(u'价格,折扣价格,数量必须是正数','/parameters_add/%s'%product_nid, u'返回')
        if pararet == -2:
            return red_writing_1(u'规格描述不能为空','/product_add/%s'%product_nid, u'返回')
        return red_writing_1(u'规格录入成功','/parameters_list/%s'%product_nid,u'点击进入规格列表')

@app.route('/parameters_del/<html_nid>')
def lis_del(html_nid):
        product_nid = request.get_cookie('product_nid', secret = 'asf&*458')
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        if checkLogin(name, ADMINPASSW) == -1:
            return red_writing_1(u'用户尚未登录','/login',u'点击登录')
        delret = delParameters(html_nid)
        return redirect('/parameters_list/%s'%product_nid)


# 用户管理
@app.route('/user_list')
def list():
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        if checkLogin(name, ADMINPASSW) == -1:
            return red_writing_1(u'用户尚未登录','/login',u'点击登录')
        userret = findUser(name)
        h = userListHtml(userret)
        return h

@app.route('/user_del/<html_nid>')
def lis_del(html_nid):
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        if checkLogin(name, ADMINPASSW) == -1:
            return red_writing_1(u'用户尚未登录','/login',u'点击登录')
        delret = delUser(html_nid)
        if delret == -1:
            return red_writing_1(u'不能删除系统管理员','/user_list',u'点击返回')
        return redirect('/user_list')


# 运费管理
@app.route('/carriage_list')
def list():
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        if checkLogin(name, ADMINPASSW) == -1:
            return red_writing_1(u'用户尚未登录','/login',u'点击登录')
        findret = findCarriage(name)
        h = carriageHtml(findret)
        return h
 
@app.route('/carriage_del/<html_nid>')
def lis_del(html_nid):
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        if checkLogin(name, ADMINPASSW) == -1:
            return red_writing_1(u'用户尚未登录','/login',u'点击登录')
        delret = delCarriage(html_nid)
        return redirect('/carriage_list')

@app.route('/carriage_add')
def add():
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        if checkLogin(name, ADMINPASSW) == -1:
            return red_writing_1(u'用户尚未登录','/login',u'点击登录')
        ipaddr = request.environ.get('X-Real-IP2')
        log.info('carriage_add ip is %s'%ipaddr)
        caradd_html = read_file('templates/carriage_add.html')
        return caradd_html

@app.route('/api/v1/carriage_add', method='POST')
def apiAdd():
        name = request.forms.get('name')
        value = request.forms.get('value')
        pararet = saveCarriage(name,value)
        if pararet == -1:
            return red_writing_1(u'保有界限和邮费必须是正数','/carriage_add', u'返回')
        return red_writing_1(u'邮费录入成功','/carriage_list',u'点击返回')


@app.error(404)
def err(err):
	return red_writing_1(u'页面不存在','/',u'点击返回主页')

@app.error(405)
def err(err):
	return red_writing_1(u'访问方式不正确','/',u'点击返回主页')

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
