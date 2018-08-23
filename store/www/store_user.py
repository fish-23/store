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
import string
sys.path.append('../')
sys.path.append('/root')
from log import *
from config import *
from PIL import Image
from random import randint
from bottle import *
from store_view import *
from error import *
from url import *
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
from models.payments import *
from models.transactions import *
from models.address import *


# url重定向
def mskeErrRedir(*info):
    try:
        print('777777')        
        print(info)
        long = len(info)
        err_msg = ERR[info[0]]
        url = info[1]
        print(url)
        if long == 2:
            if type(url) == list:
                url_id = url[1]
                url = url[0]
                print('11111111')
                print(url)
                print(url_id)
                urll = URL[url]
                url_msg = URL_MSG[url]
                return red_writing_1(err_msg,urll%url_id,url_msg)
            urll = URL[url]
            url_msg = URL_MSG[url]
            return red_writing_1(err_msg,urll,url_msg)
        if long == 3:
            url2 = info[2]
            if type(url) == list:
                url_id = url[1]
                url = url[0]
                urll = URL[url]
                url_msg = URL_MSG[url]
                if type(url2) == list:
                    url2_id = url2[1]
                    url2 = url2[0]
                    urll2 = URL[url2]
                    url_msg2 = URL_MSG[url2]
                    return red_writing_2(err_msg,urll%url_id,url_msg,urll2%url2_id,url_msg2)
                urll = URL[url]
                url_msg = URL_MSG[url]
                urll2 = URL[url2]
                url_msg2 = URL_MSG[url2]
                return red_writing_2(err_msg,urll%url_id,url_msg,urll2,url_msg2)
            urll = URL[url]
            url_msg = URL_MSG[url]
            if type(url2) == list:
                url2_id = url2[1]
                url2 = url2[0]
                urll2 = URL[url2]
                url_msg2 = URL_MSG[url2]
                return red_writing_2(err_msg,urll,url_msg,urll2%url2_id,url_msg2)
            urll2 = URL[url2]
            url_msg2 = URL_MSG[url2]
            return red_writing_2(err_msg,urll,url_msg,urll2,url_msg2)
        return 0
    except Exception as e:
        log.error(traceback.format_exc())


# 图片检测
def checkPic(pic):
    try:
        if pic == None:
            return -15
        pic_size = pic.file   
        pic_size.seek(0,2)   
        pic_size = pic_size.tell()
        if pic_size > 1048000:
            return -16
        pic_distinguish = pic.file
        bValid = True
        try:
            Image.open(pic_distinguish).verify()
        except:
            bValid = False 
        if bValid == False:
            return -17
        pic_name, pic_ext = os.path.splitext(pic.filename)
        pic_ext = pic_ext.lower()
        if str(pic_ext) not in ['.jpeg', '.bmp', '.png', '.webp', '.gif', '.jpg']:
            return -18
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
        ret = Users.get(Users.id == nid,Users.del_status == 0)
        ret.avaturaddr = picaddr
        ret.avatur = base64_str
        ret.save()
        return 0
    except Exception as e:
        log.error(traceback.format_exc())


# ip检测
def checkIp():
    try:
        ipaddr = request.headers.get('X-Real-IP3')
        time_now = int(time.time())
        dbip = Ips.select().where(Ips.ipaddr == ipaddr)
        if dbip.count() == 0:
            Ips.create(ipaddr=ipaddr, sendsms_time=time_now)
            lis = []
            lis.append(ipaddr)
            lis.append(time_now)
            return lis
        dbip = Ips.get(Ips.ipaddr == ipaddr)
        dbnum = dbip.num
        dbsendtime = dbip.sendsms_time
        checktime = time_now - dbsendtime
        if checktime > 86400:
            Ips.update(sendsms_time=time_now, num=0).where(Ips.ipaddr == ipaddr).execute()
        if dbnum > 4:
            return -11
        lis = []
        lis.append(ipaddr)
        lis.append(time_now)
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
            return -9
        phoneprefix = ['130','131','132','133','134','135','136','137','138','139','150','151', \
                       '152','153','156','158','159','170','183','182','181','185','186','187','188','189']
        if len(cellphone) != 11 or cellphone.isdigit() != True or cellphone[:3] not in phoneprefix:
            return -10
        return 0
    except Exception as e:
        log.error(traceback.format_exc())


# 回调函数
def done_callback(futu):
    return 'end'


# 用户名密码检测
def checkPasswd(name,password,password2):
    try:
        log.info(name)
        log.info(len(name))
        dbusers = Users.select().where(Users.name == name)
        if dbusers.count() != 0:
            return -1
        if password != password2:
            return -2
        import re
        re_check = re.compile(u'[\u4e00-\u9fa5]+')
        check_ret = re_check.search(name)
        if check_ret:
            return -4
        if len(name) < 6 or name.isspace() == True:
            return -3
        if len(password) < 6 or password.isspace() == True:
            return -3
    except Exception as e:
        log.error(traceback.format_exc())


# 查找用户id
def userId(login_name):
    try:
        user_info = Users.get(Users.name == login_name)
        user_id = user_info.id
        return user_id 
    except Exception as e:
        log.error(traceback.format_exc())


# 列表生成
def lisAppend(cellphone,sms_num,send_time):
    try:
        lis = []
        lis.append(cellphone)
        lis.append(sms_num)
        lis.append(send_time)
        return lis
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
        return -13 

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
            return -4
        if passwdret == -2:
            return -7
        if passwdret == -3:
            return -8
        if passwdret == -4:
            return -39
        nickret = checkNickBirth(nickname,birthday,send_sms,dbsend_sms,dbsend_time) 
        if nickret == -1:
            return -12
        if nickret == -2:
            return -19
        if nickret == -3:
            return -20
        if nickret == -4:
            return -21
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
            return -5
        dbusers = Users.select().where(Users.name == name)
        if dbusers.count() == 0:
            return -3
        dbusers = Users.get(Users.name == name)
        dbname = dbusers.name
        dbpassword = dbusers.password
        password = hashlib.md5(password.encode('utf8')).hexdigest()
        if dbname != name or dbpassword != password:
            return -6
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
                productret = Products.select().where(Products.category == i,Products.del_status==0)
            else:
                productret =Products.select().where(Products.category==i,Products.del_status==0 ,Products.name % '%{}%'.format(name))
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
        productret = Products.get(Products.id == nid,Products.del_status==0)
        parameterret = ProductParameters.select().where(ProductParameters.product == nid,ProductParameters.del_status==0)
        return productDetailsHtml(productret, parameterret)
    except Exception as e:
        log.error(traceback.format_exc())

def checkDetailsInfo(shopping_cart,product_id,parameter_id,buy_num,login_name):
    try:
        if buy_num == '':
            return -22
        if  buy_num.isnumeric() == False:
            return -23
        if int(buy_num)<1 or int(buy_num)>100:
            return -23
        if parameter_id == None:
            return -24
        #if order_now == '立即购买':
            #return -5
        if str(shopping_cart) == '加入购物车':
            return shoppingCartAdd(product_id,parameter_id,buy_num,login_name)
        return 0
    except Exception as e:
        log.error(traceback.format_exc())


# shopping_cart
def shoppingCartAdd(product_id,parameter_id,buy_num,login_name):
    try:
        shopping_info = ShoppingCart.select().where(ShoppingCart.product_parameters==parameter_id)
        user_id = userId(login_name)
        if shopping_info.count() == 0:
            ShoppingCart.create(num=buy_num, product_parameters=parameter_id, 
                                product=product_id,users=user_id)
        else:
            num_info = ShoppingCart.get(ShoppingCart.product_parameters==parameter_id)
            db_num = num_info.num
            num = int(db_num) + int(buy_num)
            num_info.num = num
            num_info.save()
        return 2
    except Exception as e:
        log.error(traceback.format_exc())

def cartInfo(login_name):         
    try:
        user_id = userId(login_name)
        cart_info = ShoppingCart.select().where(ShoppingCart.users == user_id).order_by(ShoppingCart.product)
        carriage_info = Settings.get(Settings.description == 'carriage')
        return cartHtml(cart_info,carriage_info)
    except Exception as e:
        log.error(traceback.format_exc())

def cartDel(login_name,nid):
    try:
        user_id = userId(login_name)
        cart_info = ShoppingCart.get(ShoppingCart.id == nid)
        cart_user = cart_info.users.id
        if int(user_id) != int(cart_user):
            return -27
        cart_info.delete_instance()
        return 0 
    except Exception as e:
        log.error(traceback.format_exc())


# 订单确认
def transConfirm(proditems,login_name):
    try:
        user_id = userId(login_name)
        address_ret = Address.select().where(Address.users == user_id)
        if address_ret.count() == 0:
            return -32
        address_ret = address_ret.where(Address.defaults == 1)
        if address_ret.count() == 0:
            return -33
        lis = proditems['lis']
        if lis == []:
            return -22
        return transConfirmHtml(address_ret,proditems)        
    except Exception as e:
        log.error(traceback.format_exc())
             
def saveTrade(proditems,address,send_way,user_id,remark):
    try:
        import uuid
        trade_id = uuid.uuid4().hex
        total_price = proditems['total_price']
        carriage = proditems['carriage']
        print(send_way)
        tran = Transactions.create(total_price = total_price,
                            carriage = carriage,
                            send_way = send_way,
                            address = address,
                            buy_types = 1,       
                            trade_id = trade_id,      
                            trade_status=1,
                            groups = 1,                                  
                            users = user_id,
                            remark = remark
                             )
        return tran
    except Exception as e:
        log.error(traceback.format_exc())

def savePayments(proditems,trans_id):
    try:
        product_lis = proditems['lis']
        for i in product_lis:
            product_id = i['product_id']
            parameter_id = i['parameter_id']
            num = i['num']      
            pay = Payments.create(num = num,
                               products = product_id,
                               parameters = parameter_id,                              
                               transactions = trans_id
                                )
        return pay
    except Exception as e:
        log.error(traceback.format_exc())

def cartClear(trans_id):
    try:
        trans_ret = Transactions.get(Transactions.id == trans_id)
        payments_ret = Payments.select().where(Payments.transactions == trans_id)
        for i in payments_ret:
            product_id = i.products.id
            cart_ret = ShoppingCart.select().where(ShoppingCart.product==product_id,ShoppingCart.users==trans_ret.users.id).count()
            if cart_ret:
                cart_ret = ShoppingCart.get(ShoppingCart.product==i.products.id,ShoppingCart.users==trans_ret.users.id)
                cart_ret.delete_instance()
        return 0
    except Exception as e:
        log.error(traceback.format_exc())

# 订单创建
def transCreate(proditems,address_id,send_way,remark,login_name):
    try:
        user_id = userId(login_name)
        if address_id == None:
            address_id = Address.get(Address.users == user_id,Address.defaults == 1).id
        if send_way == None:
            send_way = '快递'
        remark = remark.strip()
        address = Address.get(Address.id == address_id)
        address = "收货人:%s,手机号:%s,收货地址:%s" % (address.name,address.phone,address.city+address.address)
        trans_info = saveTrade(proditems,address,send_way,user_id,remark)
        trans_id = trans_info.id
        pay_info = savePayments(proditems,trans_id)
        return trans_id
    except Exception as e:
        log.error(traceback.format_exc())    

# 订单详情
def tranDetails(nid,login_name):
    try:
        user_id = userId(login_name)
        trans_ret = Transactions.get(Transactions.id == nid)
        tran_user_id = trans_ret.users.id
        if user_id != tran_user_id:
            return -1
        payments_ret = Payments.select().where(Payments.transactions == nid)
        h = tranPayHtml(trans_ret,payments_ret)
        return h
    except Exception as e:
        log.error(traceback.format_exc())

# 取消订单
def transCancel(trans_id):
    trans_info = Transactions.get(Transactions.id == trans_id,Transactions.del_status == 0)
    trans_info.del_status = -1
    trans_info.trade_status = 0
    import datetime
    time_now = datetime.datetime.now()
    trans_info.del_time = time_now
    trans_info.description = '用户取消订单'
    trans_info.save()
    payments_info = Payments.select().where(Payments.transactions == trans_id,Payments.del_status == 0)
    for i in payments_info:
        i.del_status = -1
        i.del_time = time_now
        i.description = '用户取消订单'
        i.save()
    return 0 


def payTrans(trans_id,user_id):
    try:
        trans_info = Transactions.get(Transactions.id == trans_id)
        total_price = trans_info.total_price
        user_info = Users.get(Users.id == user_id)
        balance = user_info.balance
        if total_price > balance:
            return -1
        balance_ret = balance - total_price
        user_info.balance = balance_ret
        user_info.save()
        trans_info.trade_status = 2
        trans_info.save()
        return 0
    except Exception as e:
        log.error(traceback.format_exc())

# 订单支付
def checkPayCancel(trans_id,trans_cancel,pay,login_name):
    try:
        user_id = userId(login_name)
        if trans_cancel == '取消订单':
            transCancel(trans_id)
            return -29
        if pay == '去支付':
            pay_ret = payTrans(trans_id,user_id)
            if pay_ret == -1:
                return -31
    except Exception as e:
        log.error(traceback.format_exc())

# 订单列表
def tranList(login_name):
    try:
        user_id = userId(login_name)
        trans_info = Transactions.select().where(Transactions.users == user_id,Transactions.del_status == 0)
        return tranListHtml(trans_info,user_id) 
    except Exception as e:
        log.error(traceback.format_exc())


#用户中心
def userList(login_name):
    try:
        user_info = Users.get(Users.name == login_name)
        return userListHtml(user_info)
    except Exception as e:
        log.error(traceback.format_exc())

# 收货地址
def addressAdd(name,phone,city,address,defaults,login_name):
    try: 
        user_id = userId(login_name)
        name = name.strip()
        phone = phone.strip()
        city = city.strip()
        address = address.strip()
        if name=='' or city=='' or address=='':
            return -34
        if defaults == '':
            return -35
        if checkCellphone(phone) == -2:
            return -10
        defaults = int(defaults)
        if defaults == 1:
            address_ret = Address.select().where(Address.users == user_id,Address.defaults == 1)
            if address_ret.count() != 0:
                address_ret = Address.get(Address.users == user_id,Address.defaults == 1)
                address_ret.defaults = 0
                address_ret.save()
        Address.create(name=name, phone=phone, city=city, address=address, defaults=defaults,users=user_id)
        return 0
    except Exception as e:
        log.error(traceback.format_exc())

def addressList(login_name):
    try:
        user_id = userId(login_name)
        address_ret = Address.select().where(Address.users == user_id)
        return addressListHrml(address_ret)
    except Exception as e:
        log.error(traceback.format_exc())

def addressDefaults(nid,login_name):
    try:
        if nid == None:
            return -36
        user_id = userId(login_name)
        count = Address.select().where(Address.users == user_id,Address.defaults == 1).count()
        if count != 0:
              address_ret = Address.get(Address.users == user_id,Address.defaults == 1)
              address_ret.defaults = 0       
              address_ret.save()
        address = Address.get(Address.id == nid)
        address.defaults = 1
        address.save()
    except Exception as e:
        log.error(traceback.format_exc())

def addressDel(login_name,nid):
    try:
        user_id = userId(login_name)
        address_info = Address.get(Address.id == nid)
        address_user = address_info.users.id
        if int(user_id) != int(address_user):
            return -27
        address_info.delete_instance()
        return 0
    except Exception as e:
        log.error(traceback.format_exc())
