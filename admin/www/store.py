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
        ret = checkLogin(name, ADMINPASSW)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login')
        ipaddr = request.headers.get('X-Real-IP2')
        log.info('admin index ip is %s'%ipaddr)
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
        if type(checkret)==int and checkret!=0:
            return mskeErrRedir(-6,'login')
        response.set_cookie('cookie_name', name, secret = 'asf&*457', domain='admin.fish-23.com', path = '/')
        redirect('/')


# 产品管理
@app.route('/product_list_admin')
def list():
        ipaddr = request.headers.get('X-Real-IP2')
        log.info('admin product_list_admin ip is %s'%ipaddr)
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        ret = checkLogin(name, ADMINPASSW)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login')
        findret = findProduct(name)
        h = listHtml(findret)
        return h          

@app.route('/product_add')
def add():
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        ret = checkLogin(name, ADMINPASSW)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login')
        ipaddr = request.headers.get('X-Real-IP2')
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
        picret = checkPic(pic)
        if type(picret)==int and picret!=0:
            return mskeErrRedir(picret,'product_add')
        proret = saveProduct(name, num, price, discount, description, user_name, category)
        if type(proret)==int and proret!=0:
            return mskeErrRedir(proret,'product_add')
        product_id = proret[0]
        group_id = proret[1]
        picret = saveImage(name, pic, product_id)
        return mskeErrRedir(5,'product_list_admin')
        
@app.route('/product_del/<html_nid>')
def lis_del(html_nid):
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        ret = checkLogin(name, ADMINPASSW)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login')
        delProduct(html_nid)  
        return redirect('/product_list_admin')

@app.route('/product_modify/<html_nid>')
def product_modify(html_nid):
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        ret = checkLogin(name, ADMINPASSW)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login')
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
        return mskeErrRedir(-46,'product_list_admin')

@app.route('/parameters_list/<html_nid>')
def list(html_nid):
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        ret = checkLogin(name, ADMINPASSW)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login')
        findret = findParameters(html_nid)
        product_nid = html_nid
        h = parametersHtml(findret, product_nid)
        return h

@app.route('/parameters_add/<product_nid>')
def add(product_nid):
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        ret = checkLogin(name, ADMINPASSW)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login')
        ipaddr = request.headers.get('X-Real-IP2')
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
        description = description.strip()
        pararet = saveParameters(product_nid, num, price, discount, description)
        if type(pararet)==int and pararet!=0:
            if pararet == -40:
                return mskeErrRedir(pararet,['parameters_add',product_nid])
            return mskeErrRedir(pararet,['product_add',product_nid])
        return mskeErrRedir(6,['parameters_list',product_nid])

@app.route('/parameters_del/<html_nid>')
def lis_del(html_nid):
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        ret = checkLogin(name, ADMINPASSW)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login')
        delret = delParameters(html_nid)
        return redirect('/parameters_list/%s'%delret)


# 用户管理
@app.route('/user_list/<name_phone>')
def list(name_phone):
        ipaddr = request.headers.get('X-Real-IP2')
        log.info('admin user_list ip is %s'%ipaddr)
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        ret = checkLogin(name, ADMINPASSW)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login')
        print(name_phone)
        userret = findUser(name,name_phone)
        h = userListHtml(userret)
        return h

@app.route("/api/v1/user_list", method="post")
def user_list():
        name_phone = request.forms.get('name_phone')
        name_phone = name_phone.strip()
        searchret = userSearchCheck(name_phone)
        if searchret == -1:
           redirect('/user_list/none') 
        redirect('/user_list/%s'%name_phone)


@app.route('/user_del/<html_nid>')
def lis_del(html_nid):
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        ret = checkLogin(name, ADMINPASSW)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login')
        delret = delUser(html_nid)
        if type(delret)==int and delret!=0:
            return mskeErrRedir(delret,'user_list')
        return redirect('/user_list')

@app.route('/user_recharge/<html_nid>')
def lis_del(html_nid):
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        ret = checkLogin(name, ADMINPASSW)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login')
        ret = userRecharge(html_nid,name)
        return ret

@app.route('/api/v1/user_recharge', method='POST')
def apiAdd():
        operate_id = request.forms.get('operate_id')
        nid = request.forms.get('nid')
        balance = request.forms.get('balance')
        dbbalance = request.forms.get('dbbalance')
        ret = rechargeCheck(operate_id,nid,balance,dbbalance)    
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,['user_recharge',nid])
        return mskeErrRedir(8,'user_list')

# 运费管理
@app.route('/carriage_list')
def list():
        ipaddr = request.headers.get('X-Real-IP2')
        log.info('admin carriage_list ip is %s'%ipaddr)
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        ret = checkLogin(name, ADMINPASSW)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login')
        findret = findCarriage(name)
        h = carriageHtml(findret)
        return h
 
@app.route('/carriage_del/<html_nid>')
def lis_del(html_nid):
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        ret = checkLogin(name, ADMINPASSW)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login')
        delret = delCarriage(html_nid)
        return redirect('/carriage_list')

@app.route('/carriage_add')
def add():
        name = request.get_cookie('cookie_name', secret = 'asf&*457')
        ret = checkLogin(name, ADMINPASSW)
        if type(ret)==int and ret!=0:
            return mskeErrRedir(ret,'login')
        ipaddr = request.headers.get('X-Real-IP2')
        log.info('carriage_add ip is %s'%ipaddr)
        caradd_html = read_file('templates/carriage_add.html')
        return caradd_html

@app.route('/api/v1/carriage_add', method='POST')
def apiAdd():
        name = request.forms.get('name')
        value = request.forms.get('value')
        pararet = saveCarriage(name,value)
        if type(pararet)==int and pararet!=0:
            return mskeErrRedir(pararet,'carriage_add')
        return mskeErrRedir(7,'carriage_list')


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
    bottle.run( host='127.0.0.1', port='10070',
                app=StripPathMiddleware(app),
                reloader=True, debug=True
              )
