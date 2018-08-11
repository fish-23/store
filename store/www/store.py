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
        ipaddr = request.headers.get('X-Real-IP3')
        log.info('index browser ip is %s'%ipaddr)
        index_html = read_file('templates/index.html')
        return index_html


# 用户注册
@app.route('/register')
def register():
        ipaddr = request.headers.get('X-Real-IP3')
        log.info('register browser ip is %s'%ipaddr)
        register_html = read_file("templates/register.html")
        return register_html

@app.route('/api/v1/register', method="post")
def register():
        cellphone = request.forms.get('cellphone')
        checkret = checkCellphone(cellphone)
        if checkret == -1:
            return red_writing_2(u'该手机号已注册','/login',u'点击登录','/',u'点击返回主页')
        if checkret == -2:
            return red_writing_1(u'手机号格式不正确','/register',u'点击重新输入')
        ret = checkIp()
        if ret == -1:
            return red_writing_1(u'每个IP每天最多接收5条短信','/',u'点击返回主页')
        sendsmsret = registerSendSms(cellphone,ret[0])
        lis = []
        lis.append(cellphone)
        lis.append(sendsmsret)
        lis.append(ret[1])
        response.set_cookie('register_info', lis, domain='www.fish-23.com', path = '/', secret = 'asf&*4561')
        redirect('/register_add')

@app.route('/register_add')
def register_add():
        info = request.get_cookie('register_info', secret = 'asf&*4561')
        register_add_html = read_file('templates/register_add.html')
        return register_add_html
        
@app.route('/api/v1/register_add', method="post")
def register_add():
        info = request.get_cookie('register_info', secret = 'asf&*4561')
        if checkRegCookie(info) == -1:
            return red_writing_1(u'注册异常，异常的访问方式','/register',u'点击重新注册')
        name = request.forms.get('name')
        password = request.forms.get('password')
        password2 = request.forms.get('password2')
        nickname = request.forms.get('nickname')
        birthday = request.forms.get('birthday')
        gender = request.forms.get('gender')
        avatur = request.files.get('avatur')
        send_sms = request.forms.get('send_sms')
        name = name.strip()
        nickname = nickname.strip()
        birthday = birthday.strip()
        picret = checkPic(avatur)
        if picret == -1:
            return red_writing_1(u'图片不能为空','/register_add',u'返回')
        if picret == -2:
            return red_writing_1(u'图片不能大于1M','/register_add',u'返回')
        if picret == -3:
            return red_writing_1(u'该文件不是真正的图片','/register_add',u'返回')
        if picret == -4:
            return red_writing_1(u'图片格式不是常用图片格式','/register_add',u'返回')
        checkret = SaveInfo(name,password,password2,nickname,birthday,send_sms,gender,info)
        if checkret == -1:
            return red_writing_1(u'该用户名存在','/register_add',u'点击重新输入')
        if checkret == -2:
            return red_writing_1(u'两次密码不一致','/register_add',u'点击重新输入')
        if checkret == -3:
            return red_writing_1(u'账号密码格式错误，不能小于6位','/register_add',u'点击重新输入')
        if checkret == -4:
            return red_writing_1(u'昵称，生日不能小于1位','/register_add',u'点击重新输入')
        if checkret == -5:
            return red_writing_1(u'验证码错误','/register_add',u'点击重新输入')
        if checkret == -6:
            return red_writing_1(u'验证码是六位纯数字','/register_add',u'点击重新输入')
        if checkret == -7:
            return red_writing_1(u'验证码超时','/register',u'点击重新注册')
        nid = checkret 
        saveImage(name, avatur, nid)   
        return red_writing_1(u'注册成功','/login',u'点击登陆')


# 用户登陆
@app.route('/login')
def login():
        login_html = read_file("templates/login.html")
        return login_html


@app.route('/api/v1/login', method="post")
def login():
        name = request.forms.get('name')
        password = request.forms.get('password')
        loginret = loginCheck(name, password)
        if loginret == -1:
            return red_writing_1(u'用户名密码不能为空','/login',u'点击重新登录')
        if loginret == -2:
            return red_writing_1(u'用户名不存在','/',u'点击返回主页')
        if loginret == -3:
            return red_writing_1(u'用户名密码不正确','/login',u'点击重新登录')
        response.set_cookie('login_name', name, domain='www.fish-23.com', path = '/', secret = 'asf&*181183')
        redirect('/product_list')


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
