#!/usr/local/python3
# -*- coding: UTF-8 -*-

import traceback
import time,datetime
import sys
import base64
import io
import os
import asyncio
import hashlib
import re
sys.path.append('../')
sys.path.append('/root')
from log import *
from config import *
from PIL import Image
from random import randint
from bottle import *
from store_view import *
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

from models.base import *
from models.users import *
from models.products import *
from models.product_parameters import *
from models.settings import *
from models.categories import *
from models.groups import *
from models.ips import *
from models.shopping_cart import *

# 图片检测
def checkPic(pic):
    try:
        if pic == None:
            return -1
        pic_size = pic.file   
        pic_size.seek(0,2)   
        pic_size = pic_size.tell()
        if pic_size > 1048000:
            return -2
        pic_distinguish = pic.file
        bValid = True
        try:
            Image.open(pic_distinguish).verify()
        except:
            bValid = False 
        if bValid == False:
            return -3
        pic_name, pic_ext = os.path.splitext(pic.filename)
        pic_ext = pic_ext.lower()
        if str(pic_ext) not in ['.jpeg', '.bmp', '.png', '.webp', '.gif', '.jpg']:
            return -4
        return 0
    except Exception as e:
        log.error(traceback.format_exc())


# 图片存储
def saveImage(name, pic, nid):
    try:
        pic_name, pic_ext = os.path.splitext(pic.filename)
        pic_ext = pic_ext.lower()
        pic.filename = ''.join(('%s_pic'%name, pic_ext))
        pic.save(PATHPWDU,overwrite=True)
        picname = pic.filename
        picaddr = PATHPWDU + picname
        return recordImage(picaddr,pic, nid) 
    except Exception as e:
        log.error(traceback.format_exc())

def recordImage(picaddr,pic, nid):
    try:
        pic = pic.file
        img = Image.open(pic)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        imge = img.resize((130,90))
        # 缩略图转base64
        output_buffer = io.BytesIO()
        imge.save(output_buffer, format='JPEG')      
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data)
        # 存缩略图
        ret = Users.get(Users.id == nid)
        ret.avaturaddr = picaddr
        ret.avatur = base64_str
        ret.save()
        return 0
    except Exception as e:
        log.error(traceback.format_exc())


# ip检测
def checkIp():
    try:
        print('checkip')
        ipaddr = request.headers.get('X-Real-IP3')
        time_now = int(time.time())
        print('time_now is', time_now)
        dbip = Ips.select().where(Ips.ipaddr == ipaddr)
        if dbip.count() == 0:
            Ips.create(ipaddr=ipaddr, sendsms_time=time_now)
            return ipaddr
        dbip = Ips.get(Ips.ipaddr == ipaddr)
        dbnum = dbip.num
        dbsendtime = dbip.sendsms_time
        checktime = time_now - dbsendtime
        if checktime > 86400:
            Ips.update(sendsms_time=time_now, num=0).where(Ips.ipaddr == ipaddr).execute()
        if dbnum > 4:
            return -1
        lis = []
        lis.append(ipaddr)
        log.info('store_user.py checkip %s'%time_now)
        lis.append(time_now)
        log.info('store_user.py checkip %s'%lis)
        return lis
    except Exception as e:
        log.error(traceback.format_exc())


# 发送短信
async def send_sms(phone,sms_num):
    ssender = SmsSingleSender(SMSAPPID, SMSAPPKEY)
    params = [str(sms_num), "30"]
    try:
        result = ssender.send_with_param(86, str(phone),TEMPLATE_ID, params)
    except HTTPError as e:
        return -1
    except Exception as e:
        return -1
    return 0


# 检测手机号
def checkCellphone(cellphone):
    try:
        selectphone = Users.select().where(Users.cellphone == cellphone).count()
        if selectphone != 0:
            return -1
        phoneprefix = ['130','131','132','133','134','135','136','137','138','139','150','151', \
                       '152','153','156','158','159','170','183','182','181','185','186','188','189']
        if len(cellphone) != 11 or cellphone.isdigit() != True or cellphone[:3] not in phoneprefix:
            return -2
        return 0
    except Exception as e:
        log.error(traceback.format_exc())


# 回调函数
def done_callback(futu):
    return 'end'


# 用户名密码检测
def checkPasswd(name,password,password2):
    try:
        dbusers = Users.select().where(Users.name == name)
        if dbusers.count() != 0:
            return -1
        if password != password2:
            return -2
        if len(name) < 6 or name.isspace() == True:
            return -3
        if len(password) < 6 or password.isspace() == True:
            return -3
    except Exception as e:
        log.error(traceback.format_exc())

# register
async def sendInfo(ipaddr):
    try:
        dbip = Ips.get(Ips.ipaddr == ipaddr)
        dbnum = dbip.num
        num = dbnum + 1
        dbip.num = num
        dbip.save()
    except Exception as e:
        log.error(traceback.format_exc())


def registerSendSms(cellphone,ipaddr):
    try:
        sms_num = randint(100000,999999)
        loop = asyncio.get_event_loop()
        takes = [send_sms(cellphone,sms_num), sendInfo(ipaddr)]
        gathers = asyncio.wait(takes)
        futu = asyncio.ensure_future(gathers)
        futu.add_done_callback(done_callback)
        loop.run_until_complete(futu)
        print('return is', futu.result())
        return sms_num
    except Exception as e:
        log.error(traceback.format_exc()) 

def checkRegCookie(info):
    if info == None:
        return -1 

def checkNickBirth(nickname,birthday,send_sms,dbsend_sms,dbsend_time):
    try:
        if len(nickname) < 1 or len(birthday) < 1:
            return -1
        if len(send_sms) != 6 or send_sms.isdigit() != True:
            return -3
        if int(send_sms) != int(dbsend_sms):
            return -2
        nowtime = int(time.time())
        checktime = int(dbsend_time) + 1800
        if checktime < nowtime:
            return -4
        return 0
    except Exception as e:
        log.error(traceback.format_exc())

def SaveInfo(name,password,password2,nickname,birthday,send_sms,gender,info):
    try:
        dbsend_sms = info[1]
        cellphone = info[0]
        dbsend_time = info[2]
        passwdret = checkPasswd(name,password,password2)
        if passwdret == -1:
            return -1
        if passwdret == -2:
            return -2
        if passwdret == -3:
            return -3
        nickret = checkNickBirth(nickname,birthday,send_sms,dbsend_sms,dbsend_time) 
        if nickret == -1:
            return -4
        if nickret == -2:
            return -5
        if nickret == -3:
            return -6
        if nickret == -4:
            return -7
        password = hashlib.md5(password.encode('utf8')).hexdigest()
        userinfo = Users.create( name=name, password=password, nickname=nickname,
                                 birthday=birthday, cellphone=cellphone,gender=gender)
        return userinfo.id
    except Exception as e:
        log.error(traceback.format_exc())


# login
def loginCheck(name, password):
    try:
        if name == '' or password == '':
            return -1
        dbusers = Users.select().where(Users.name == name)
        if dbusers.count() == 0:
            return -2
        dbusers = Users.get(Users.name == name)
        dbname = dbusers.name
        dbpassword = dbusers.password
        password = hashlib.md5(password.encode('utf8')).hexdigest()
        if dbname != name or dbpassword != password:
            return -3
        import datetime
        login_time = datetime.datetime.now()
        cookie_num = name + ';' + '1'
        dbusers.cookie_num = cookie_num
        dbusers.login_time = login_time
        dbusers.save()
        return 0
    except Exception as e:
        log.error(traceback.format_exc())

def checkLogin(login_name):
    try:
        print('1111111')
        print(login_name)
        if login_name == None:
            return -1
        user_ret = Users.select().where(Users.name == login_name)
        if user_ret.count() == 0:
            return -2
        user_ret = Users.get(Users.name == login_name)
        db_cookie_num = user_ret.cookie_num
        db_login_time = user_ret.login_time
        cookie_num = login_name + ';' + '1'
        if db_cookie_num != cookie_num:
            return -1
        time_now = int(time.time())
        db_login_time = str(db_login_time)
        db_login_time = time.strptime(db_login_time, "%Y-%m-%d %H:%M:%S")
        db_login_time = int(time.mktime(db_login_time)) 
        check_time = time_now - db_login_time
        if check_time > 86400:
            user_ret.cookie_num = login_name + ';' + '2'
            user_ret.save()
            return -1
        return 0
    except Exception as e:
        log.error(traceback.format_exc())

# product
def productInfo(name):
    try:
        categories = Categories.select().where(Categories.parent_name == '产品')
        categories_id = [i.id for i in categories]
        categories_name = [i.name for i in categories]
        categories_info = zip(categories_id, categories_name)
        h = ''
        for k in categories_info:
            i = k[0]
            j = k[1]               
            if name =='none':
                productret = Products.select().where(Products.category == i)
            else:
                productret = Products.select().where(Products.category == i, Products.name % '%{}%'.format(name))
                count = productret.count()
                if count == 0:
                    continue
            html = productListHtml(productret,j)
            h = h + html
        return productListJoinHtml(h) 
    except Exception as e:
        log.error(traceback.format_exc())

def productSearch(name):
    try:
        if len(name) == 0:
            return -1 
    except Exception as e:
        log.error(traceback.format_exc())

def productDetails(nid):
    try:
        productret = Products.get(Products.id == nid)
        parameterret = ProductParameters.select().where(ProductParameters.product == nid)
        return productDetailsHtml(productret, parameterret)
    except Exception as e:
        log.error(traceback.format_exc())

def checkDetailsInfo(order_now,shopping_cart,product_id,parameter_id,buy_num,login_name):
    try:
        if buy_num == '':
            return -1
        if  buy_num.isnumeric() == False:
            return -2
        if int(buy_num)<1 or int(buy_num)>100:
            return -2
        if parameter_id == None:
            return -3
        if order_now == '立即购买':
            return -5
        if str(shopping_cart) == '加入购物车':
            return shoppingCartAdd(product_id,parameter_id,buy_num,login_name)
        return 0
    except Exception as e:
        log.error(traceback.format_exc())


# shopping_cart
def shoppingCartAdd(product_id,parameter_id,buy_num,login_name):
    try:
        shopping_info = ShoppingCart.select().where(ShoppingCart.product_parameters==parameter_id)
        user_info = Users.get(Users.name == login_name)
        user_id = user_info.id 
        if shopping_info.count() == 0:
            ShoppingCart.create(num=buy_num, product_parameters=parameter_id, 
                                product=product_id,users=user_id)
        else:
            num_info = ShoppingCart.get(ShoppingCart.product_parameters==parameter_id)
            db_num = num_info.num
            num = int(db_num) + int(buy_num)
            num_info.num = num
            num_info.save()
        return 1
    except Exception as e:
        log.error(traceback.format_exc())
