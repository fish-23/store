#!/usr/local/python3
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
from error import *
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
        if type(checkret)==int and checkret!=0:
            if checkret == -10:
                return mskeErrRedir(checkret,'register')     
            return mskeErrRedir(checkret,'login','/')
        ret = checkIp()
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'/')
        sendsmsret = registerSendSms(cellphone,ret[0])
        lis = lisAppend(cellphone,sendsmsret,ret[1])
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
        ret = checkRegCookie(info)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'/register')       
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
        if type(picret)==int and picret!=0:
            return mskeErrRedir(picret,'register_add')
        checkret = SaveInfo(name,password,password2,nickname,birthday,send_sms,gender,info)
        if type(checkret)==int and checkret<0:
            if checkret == -21:
                return mskeErrRedir(checkret,'register')
            return mskeErrRedir(checkret,'register_add')
        nid = checkret 
        saveImage(name, avatur, nid)   
        return mskeErrRedir(1,'login')


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
        if type(loginret)==int and  loginret!=0:
            return mskeErrRedir(loginret,'login','/')
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
        ret =  checkLogin(login_name)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login','register')
        #order_now = request.forms.get('buy')
        shopping_cart = request.forms.get('cart')
        parameter_id = request.forms.get('parameter')
        product_id = request.forms.get('html_nid')
        buy_num = request.forms.get('buynum')
        buy_num = buy_num.strip()
        checkret = checkDetailsInfo(shopping_cart,product_id,parameter_id,buy_num,login_name)
        if type(checkret)==int and checkret!=0:
            if checkret == 2:
                return mskeErrRedir(checkret,'product_list','shopping_cart')
            return mskeErrRedir(checkret,['product_details',product_id])
        return mskeErrRedir(-26,'/') 


# 购物车
@app.route('/shopping_cart')
def shopping_cart():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        ret =  checkLogin(login_name)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login','register')
        h = cartInfo(login_name)
        return h

@app.route('/shopping_cart_del/<nid>')
def shopping_cart_del(nid):
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        ret =  checkLogin(login_name)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login','register')
        del_ret = cartDel(login_name,nid) 
        if type(del_ret)==int and del_ret!=0:
            return mskeErrRedir(del_ret,'shopping_cart')       
        redirect('/shopping_cart')


# 确认订单
@app.route('/api/v1/transaction_confirm', method="post")
def transaction_confirm():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        ret =  checkLogin(login_name)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login','register')
        proditems = request.forms.get('proditems')
        proditems = proditems.replace("'","\"")
        proditems = json.loads(proditems)
        trans_ret = transConfirm(proditems, login_name)
        if type(trans_ret)==int and trans_ret!=0:
            if trans_ret == -25 or trans_ret == -22:
                return mskeErrRedir(trans_ret,'/')
            return mskeErrRedir(trans_ret,'address_add','address_list')
        return trans_ret     
    
# 创建订单
@app.route('/api/v1/transaction_create', method="post")
def transaction_create():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        ret =  checkLogin(login_name)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login','register')
        address_id = request.forms.get('choice')
        send_way = request.forms.get('send_way')
        print('send_way',send_way)
        remark = request.forms.get('remark')
        proditems = request.forms.get('proditems')
        proditems = proditems.replace("'","\"")
        proditems = json.loads(proditems)
        trans_ret = transCreate(proditems,address_id,send_way,remark,login_name)
        cart_clear = cartClear(trans_ret) 
        redirect('/transaction_details/%s'%trans_ret)

# 订单详情
@app.route('/transaction_details/<nid>')
def transaction_details(nid):
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        ret =  checkLogin(login_name)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login','register')
        trans_ret = tranDetails(nid,login_name)
        if trans_ret == -1:
            return red_writing_1(u'只能支付自己的订单', '/',u'返回主页')
        return trans_ret

# 订单列表
@app.route('/transaction_list')
def transaction_list():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        ret =  checkLogin(login_name)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login','register')
        trans_ret = tranList(login_name)
        return trans_ret


# 订单支付
@app.route('/api/v1/pay_ready', method="post")
def transaction_create():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        ret =  checkLogin(login_name)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login','register')
        trans_id = request.forms.get('trans_id')
        trans_cancel = request.forms.get('cancel_trans')
        pay = request.forms.get('pay')
        check_ret = checkPayCancel(trans_id,trans_cancel,pay,login_name)
        if type(check_ret)==int and check_ret!=0:
            return mskeErrRedir(check_ret,'transaction_list','/')
        return mskeErrRedir(3,'transaction_list', '/')


# 收货地址
@app.route('/address_add')
def address_add():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        ret =  checkLogin(login_name)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login','register')
        address_html = read_file("templates/address_add.html")
        return address_html

@app.route('/api/v1/address_add', method="post")
def address_add():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        ret =  checkLogin(login_name)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login','register')
        name = request.forms.get('name')
        phone = request.forms.get('phone')
        city = request.forms.get('city')
        address = request.forms.get('address')
        defaults = request.forms.get('defaults')
        add_ret = addressAdd(name,phone,city,address,defaults,login_name)
        if type(add_ret)==int and add_ret!=0:
            return mskeErrRedir(add_ret,'address_add')
        return mskeErrRedir(4,'address_list', 'shopping_cart')

@app.route('/address_list')
def address_list():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        ret =  checkLogin(login_name)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login','register')
        h = addressList(login_name)  
        return h   

@app.route('/api/v1/address_list', method="post")
def address_list():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        ret =  checkLogin(login_name)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login','register')
        nid = request.forms.get('defaults')
        ret = addressDefaults(nid,login_name)
        if type(ret)==int and ret!=0:
            if ret == -36:
                return mskeErrRedir(ret,'address_add','address_list')
            return mskeErrRedir(ret,'address_list')
        redirect('/address_list')

@app.route('/address_del/<nid>')
def address_del(nid):
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        ret =  checkLogin(login_name)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login','register')
        del_ret = addressDel(login_name,nid)
        if type(del_ret)==int and del_ret!=0:
            return mskeErrRedir(del_ret,'shopping_cart')
        redirect('/address_list')


# 个人中心
@app.route('/user_list')
def user_list():
        login_name = request.get_cookie('login_name', secret = 'asf&*181183')
        ret =  checkLogin(login_name)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login','register')
        ret = userList(login_name)
        return ret


@app.error(404)
def err(err):
        return mskeErrRedir(-37,'/')


@app.error(405)
def err(err):
        return mskeErrRedir(-38,'/')


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
