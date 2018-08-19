#!/usr/local/python3
# -*- coding: UTF-8 -*-

import traceback
import time,datetime
import sys
import base64
import io
import os
sys.path.append('../')
sys.path.append('/root')
from log import *
from config import *
from PIL import Image
from store_view import *
from models.base import *
from models.users import *
from models.products import *
from models.product_parameters import *
from models.settings import *


# login
def checkLogin(name, password):
    try:
        if name != ADMINNAME or password != ADMINPASSW:
            return -1
        return 0
    except Exception as e:
        log.error(traceback.format_exc())


# price
def checkPrice(num, price, discount):
    try:
        try:
            num = int(num)
            price = float(price)
            discount = float(discount)
        except Exception as e:
            return -1
        if num<1 or price<0.01 or discount<0.01 or price<discount:
            return -2
        if num>9999 or price>9999 or discount>9999:
            return -2
        return 0
    except Exception as e:
        log.error(traceback.format_exc())


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
        pic.save(PATHPWD,overwrite=True)
        picname = pic.filename
        picaddr = PATHPWD + picname
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
        ret = Products.get(Products.id == nid,Products.del_status==0)
        ret.picaddr = picaddr
        ret.thumbnail = base64_str
        ret.save()
        return 0
    except Exception as e:
        log.error(traceback.format_exc())


# 产品管理
def saveProduct(name, num, price, discount, description, user_name, category):
    try:
        checkret = checkPrice(num, price, discount)
        if checkret == -1:
            return -1
        if checkret == -2:
            return -4
        if name == '':
            return -2
        price = round(float(price),2)
        discount = round(float(discount),2)
        owner_id = Users.select(Users.id).where(Users.name == user_name)
        group = Groups.get(Groups.owner == owner_id,Groups.del_status==0)
        group_id = group.id
        product_ret = Products.select().where(Products.name == name)
        product_up = product_ret.where(Products.del_status==0)
        product_down = product_ret.where(Products.del_status==-1)
        print('222222222')
        print(product_down.count())
        if product_up.count() > 0:
            return -3
        if product_down.count() > 0:
            product_add = Products.get(Products.name == name,Products.del_status==-1)
            product_add.name=name
            product_add.num=num
            product_add.price=price
            product_add.discount=discount
            product_add.description=description
            product_add.category=int(category)
            product_add.group=group_id
            product_add.del_status=0
            product_add.save()
            print('444')
        else:
            product_add = Products.create(
                                 name=name, 
                                 num=num, 
                                 price=price, 
                                 discount=discount,
                                 description=description, 
                                 category=int(category), 
                                 group=group_id
                                 )
        print('3333333333333')                       
        lis = []
        product_id = product_add.id
        print('product_id is',product_id)
        lis.append(int(product_id))
        lis.append(int(group_id))
        print('lis is',lis)
        return lis        
    except Exception as e:
        log.error(traceback.format_exc())

def findProduct(name):
    try:
        log.info('1111111')
        log.info(name)
        owner_info = Users.get(Users.name == name)
        owner_id = owner_info.id
        group = Groups.get(Groups.owner == owner_id,Groups.del_status==0)
        group_id = group.id
        ret = Products.select().where(Products.group== group_id,Products.del_status==0)
        ret = ret.order_by(Products.category,Products.id.desc())
        return ret  
    except Exception as e:
        log.error(traceback.format_exc())

def delProduct(html_nid):
    try:
        products_ret = Products.get(Products.id == html_nid,Products.del_status==0)
        products_ret.del_status = -1
        products_ret.save()
        parameter_ret = ProductParameters.select().where(ProductParameters.product == html_nid)
        parameter_ret = parameter_ret.where(ProductParameters.del_status==0)
        if parameter_ret.count() == 0:
            return 0 
        for i in parameter_ret:
            i.del_status = -1
            i.save()
        return 0 
    except Exception as e:
        log.error(traceback.format_exc())

def modifyProduct(html_nid):      
    try:          
        ret = Products.get(Products.id == html_nid,Products.del_status==0)
        return listModifyHtml(ret)
    except Exception as e:
        log.error(traceback.format_exc())

def findParameters(html_nid):
    try:
        parameterret = ProductParameters.select().where(ProductParameters.product == html_nid,ProductParameters.del_status==0)
        return parameterret
    except Exception as e:
        log.error(traceback.format_exc())

def delParameters(html_nid):
    try:
        parametersret = ProductParameters.get(ProductParameters.id == html_nid,ProductParameters.del_status==0)
        parametersret.del_status=-1
        parametersret.save()
        product_id = ProductParameters.get(ProductParameters.id == html_nid).product.id
        log.info('222222222')
        log.info(product_id)
        log.info(type(product_id))
        return product_id
    except Exception as e:
        log.error(traceback.format_exc())

def saveParameters(product_nid, num, price, discount, description):
    try:
        checkret = checkPrice(num, price, discount) 
        if checkret == -1:
            return -1
        if checkret == -2:
            return -3
        if description == '':
            return -2
        price = round(float(price),2)
        discount = round(float(discount),2)
        para_ret =ProductParameters.select().where(ProductParameters.product==product_nid,ProductParameters.description==description)
        para_up = para_ret.where(ProductParameters.del_status==0)
        para_down = para_ret.where(ProductParameters.del_status==-1)
        if para_up.count() > 0:
            return -4
        if para_down.count() > 0:
            para_add = ProductParameters.get(ProductParameters.description==description,ProductParameters.del_status==-1)
            para_add.num=num
            para_add.price=price
            para_add.discount=discount
            para_add.description=description
            para_add.product=product_nid
            para_add.del_status=0
            para_add.save()
        else:    
            ProductParameters.create(
                             num=num,
                             price=price,
                             discount=discount,
                             description=description,
                             product=product_nid
                             )
        return 0
    except Exception as e:
        log.error(traceback.format_exc())


# 用户管理
def findUser(name):
    try:
        userret = Users.select().where(Users.del_status==0)
        return userret
    except Exception as e:
        log.error(traceback.format_exc())

def delUser(html_nid):
    try:
        user_ret = Users.get(Users.id == html_nid,Users.del_status==0)
        name = user_ret.name
        if name == 'admin':
            return -1
        user_ret.del_status = -1
        user_ret.description = 'admin后台删除'
        import datetime
        user_ret.del_time = datetime.datetime.now() 
        user_ret.save() 
        return 0
    except Exception as e:
        log.error(traceback.format_exc())


# 运费管理
def findCarriage(name):
    try:
        carriageret = Settings.select().where(Settings.description == 'carriage')
        return carriageret
    except Exception as e:
        log.error(traceback.format_exc())

def delCarriage(html_nid):
    try:
        carriageret = Settings.get(Settings.id == html_nid)
        carriageret.delete_instance()
        return 0
    except Exception as e:
        log.error(traceback.format_exc())

def saveCarriage(name,value):
    try:        
        checkret =  checkPrice(1,name,value)
        if checkret == -1:
            return -1
        if checkret == -2:
            return -2
        Settings.create(
                     name=name,
                     value=value,
                     description='carriage',
                     groups=1
                     )
        return 0
    except Exception as e:
        log.error(traceback.format_exc())
