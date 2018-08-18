#!/usr/bin/python
# -*- coding: UTF-8 -*-

import bottle
import os
import base64
import io
import struct
import sys
import json
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
        register_add_html = read_file('templates/register_add.html')
        return register_add_html
        
@app.route('/api/v1/register_add', method="post")
def register_add():
        info = request.get_cookie('register_info', secret = 'asf&*4561')
        log.info('/api/v1/register_add  info is %s'%info)
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
        redirect('/')


# 商品分类
@app.route('/product_list/<name>')
def product_list(name):  
        ipaddr = request.headers.get('X-Real-IP3')
        log.info('store product_list ip is %s'%ipaddr)
        h = productInfo(name)
        return h

@app.route("/api/v1/product_list", method="post")
def product_list():
        name = request.forms.get('name')
        name = name.strip()
        searchret = productSearch(name)
        if searchret == -1:
           redirect('/product_list/none') 
        redirect('/product_list/%s'%name)

@app.route('/product_details/<nid>')
def product_details(nid):
        h = productDetails(nid)
        return h

@app.route("/api/v1/product_details", method="post")
def product_details():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        if checkLogin(login_name) == -1:
            return red_writing_2(u'用户尚未登录','/login',u'点击登录', '/register',u'点击注册')
        if checkLogin(login_name) == -2:
            return red_writing_1(u'用户不存在', '/register',u'点击注册')    
        order_now = request.forms.get('buy')
        shopping_cart = request.forms.get('cart')
        parameter_id = request.forms.get('parameter')
        product_id = request.forms.get('html_nid')
        buy_num = request.forms.get('buynum')
        buy_num = buy_num.strip()
        checkret = checkDetailsInfo(order_now,shopping_cart,product_id,parameter_id,buy_num,login_name) 
        if checkret == -1:
            return red_writing_1(u'购买数量不能为空','/product_details/%s'%product_id,u'点击返回')
        if checkret == -2:
            return red_writing_1(u'购买数量只能是纯数字，大于1小于100','/product_details/%s'%product_id,u'点击返回')
        if checkret == -3:
            return red_writing_1(u'请选择需要购买的规格','/product_details/%s'%product_id,u'点击返回')
        if checkret == 1:
            return red_writing_2(u'加入购物车成功','/product_list/none',u'点击继续购买','/shopping_cart',u'点击进入购物车')
        if checkret == -5:
            return '商品立即购买'


# 购物车
@app.route('/shopping_cart')
def shopping_cart():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        checkret = checkLogin(login_name)
        if checkret == -1:
            return red_writing_2(u'用户尚未登录','/login',u'点击登录', '/register',u'点击注册')
        if checkret == -2:
            return red_writing_1(u'用户不存在', '/register',u'点击注册')        
        h = cartInfo(login_name)
        return h

@app.route('/shopping_cart_del/<nid>')
def shopping_cart_del(nid):
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        checkret = checkLogin(login_name)
        if checkret == -1:
            return red_writing_2(u'用户尚未登录','/login',u'点击登录', '/register',u'点击注册')
        if checkret == -2:
            return red_writing_1(u'用户不存在', '/register',u'点击注册')
        del_ret = cartDel(login_name,nid)        
        if del_ret == -1:
            return red_writing_1(u'只能删除自己的购物车产品', '/shopping_cart',u'点击返回')
        redirect('/shopping_cart')


# 订单
@app.route('/api/v1/transaction_confirm', method="post")
def transaction_confirm():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        checkret = checkLogin(login_name)
        if checkret == -1:
            return red_writing_2(u'用户尚未登录','/login',u'点击登录', '/register',u'点击注册')
        if checkret == -2:
            return red_writing_1(u'用户不存在', '/register',u'点击注册')
        proditems = request.forms.get('proditems')
        proditems = proditems.replace("'","\"")
        proditems = json.loads(proditems)
        trans_ret = transConfirm(proditems, login_name)
        if trans_ret == -1:
            return red_writing_1(u'请添加收货地址', '/address_add',u'点击添加')
        if trans_ret == -3:
            return red_writing_1(u'请设置默认收货地址', '/address_list',u'点击设置')
        if trans_ret == -2:
            return red_writing_1(u'购买异常，请联系网站工作人员', '/',u'返回主页')        
        return trans_ret         

@app.route('/api/v1/transaction_create', method="post")
def transaction_create():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        checkret = checkLogin(login_name)
        if checkret == -1:
            return red_writing_2(u'用户尚未登录','/login',u'点击登录', '/register',u'点击注册')
        if checkret == -2:
            return red_writing_1(u'用户不存在', '/register',u'点击注册')
        address_id = request.forms.get('choice')
        send_way = request.forms.get('send_way')
        print('send_way',send_way)
        remark = request.forms.get('remark')
        proditems = request.forms.get('proditems')
        proditems = proditems.replace("'","\"")
        proditems = json.loads(proditems)
        trans_ret = transCreate(proditems,address_id,send_way,remark,login_name)
        redirect('/transaction_pay/%s'%trans_ret)

@app.route('/transaction_pay/<nid>')
def transaction_pay(nid):
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        checkret = checkLogin(login_name)
        if checkret == -1:
            return red_writing_2(u'用户尚未登录','/login',u'点击登录', '/register',u'点击注册')
        if checkret == -2:
            return red_writing_1(u'用户不存在', '/register',u'点击注册')      
        trans_ret = tranPay(nid,login_name)
        if trans_ret == -1:
            return red_writing_1(u'只能支付自己的订单', '/',u'返回主页')
        return trans_ret



@app.route('/address_add')
def address_add():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        checkret = checkLogin(login_name)
        if checkret == -1:
            return red_writing_2(u'用户尚未登录','/login',u'点击登录', '/register',u'点击注册')
        if checkret == -2:
            return red_writing_1(u'用户不存在', '/register',u'点击注册')
        address_html = read_file("templates/address_add.html")
        return address_html

@app.route('/api/v1/address_add', method="post")
def address_add():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        checkret = checkLogin(login_name)
        if checkret == -1:
            return red_writing_2(u'用户尚未登录','/login',u'点击登录', '/register',u'点击注册')
        if checkret == -2:
            return red_writing_1(u'用户不存在', '/register',u'点击注册')
        name = request.forms.get('name')
        phone = request.forms.get('phone')
        city = request.forms.get('city')
        address = request.forms.get('address')
        defaults = request.forms.get('defaults')
        add_ret = addressAdd(name,phone,city,address,defaults,login_name)
        if add_ret == -1:
            return red_writing_1(u'填写的数据不能为空', '/address_add',u'返回')
        if add_ret == -2:
            return red_writing_1(u'选择是否设置为默认地址', '/address_add',u'返回')
        if add_ret == -3:
            return red_writing_1(u'手机号格式不正确','/address_add',u'返回')             
        return red_writing_2(u'收货地址添加成功','/address_list',u'收货地址管理', '/shopping_cart',u'返回购物车')

@app.route('/address_list')
def address_list():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        checkret = checkLogin(login_name)
        if checkret == -1:
            return red_writing_2(u'用户尚未登录','/login',u'点击登录', '/register',u'点击注册')
        if checkret == -2:
            return red_writing_1(u'用户不存在', '/register',u'点击注册')
        h = addressList(login_name)  
        return h   

@app.route('/api/v1/address_list', method="post")
def address_list():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        checkret = checkLogin(login_name)
        if checkret == -1:
            return red_writing_2(u'用户尚未登录','/login',u'点击登录', '/register',u'点击注册')
        if checkret == -2:
            return red_writing_1(u'用户不存在', '/register',u'点击注册')
        nid = request.forms.get('defaults')
        ret = addressDefaults(nid,login_name)
        redirect('/address_list')

@app.route('/address_del/<nid>')
def address_del(nid):
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        checkret = checkLogin(login_name)
        if checkret == -1:
            return red_writing_2(u'用户尚未登录','/login',u'点击登录', '/register',u'点击注册')
        if checkret == -2:
            return red_writing_1(u'用户不存在', '/register',u'点击注册')
        del_ret = addressDel(login_name,nid)
        if del_ret == -1:
            return red_writing_1(u'只能删除自己的购物车产品', '/shopping_cart',u'点击返回')
        redirect('/address_list')


# 个人中心
@app.route('/user_list')
def user_list():
        redirect('/address_list')
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
