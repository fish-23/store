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


# login
def checkLogin(name, password):
    if name != ADMINNAME or password != ADMINPASSW:
        return -1
    return 0

# price
def checkPrice(num, price, discount):
    try:
        try:
            num = int(num)
            price = float(price)
            discount = float(discount)
        except Exception as e:
            return -1
        if num<0 or price<0 or discount<0 or price<discount:
            return -1
    except Exception as e:
        log.error(traceback.format_exc())



# 图片存储
def saveImage(name, pic, nid):
    try:
        pic_name, pic_ext = os.path.splitext(pic.filename)
        pic_ext = pic_ext.lower()
        if str(pic_ext) not in ['.jpeg', '.bmp', '.png', '.webp', '.gif', '.jpg']:
            return(-1)       
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
        ret = Products.get(Products.id == nid)
        ret.picaddr = picaddr
        ret.thumbnail = base64_str
        ret.save()
        return 0
    except Exception as e:
        log.error(traceback.format_exc())


# 产品管理
def saveProduct(name, num, price, discount, description, pic, user_name, category):
    try:
        if checkPrice(num, price, discount) == -1:
            return -1
        if name == '':
            return -2
        if pic == None:
            return -4
        owner_id = Users.select(Users.id).where(Users.name == user_name)
        group = Groups.get(Groups.owner == owner_id)
        group_id = group.id
        product = Products.select().where(Products.name == name).count()
        if product > 0:
            return -3
        product = Products.create(
                                 name=name, 
                                 num=num, 
                                 price=price, 
                                 discount=discount,
                                 description=description, 
                                 category=int(category), 
                                 group=group_id
                                 )
        
        lis = []
        product_id = product.id
        lis.append(int(product_id))
        lis.append(int(group_id))
        return lis        
    except Exception as e:
        log.error(traceback.format_exc())

def findProduct(name):
    try:
        owner_id = Users.select(Users.id).where(Users.name == name)
        group = Groups.get(Groups.owner == owner_id)
        group_id = group.id
        ret = Products.select().where(Products.group== group_id).order_by(Products.category,Products.id.desc())
        return ret  
    except Exception as e:
        log.error(traceback.format_exc())

def delProduct(html_nid):
        ret = Products.get(Products.id == html_nid)
        picaddr = ret.picaddr
        ret.delete_instance()
        os.system('rm -rf %s'%picaddr)
        return 0 

def modifyProduct(html_nid):                
        ret = Products.get(Products.id == html_nid)
        return listModifyHtml(ret)

def findParameters(html_nid):
        parameterret = ProductParameters.select().where(ProductParameters.product == html_nid)
        return parameterret

def delParameters(html_nid):
        parametersret = ProductParameters.get(ProductParameters.id == html_nid)
        parametersret.delete_instance()
        return 0
def saveParameters(product_nid, num, price, discount, description):
    try:
        if checkPrice(num, price, discount) == -1:
            return -1
        if description == '':
            return -2
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
        userret = Users.select()
        return userret

def delUser(html_nid):
        userret = Users.get(Users.id == html_nid)
        name = userret.name
        if name == 'admin':
            return -1
        userret.delete_instance() 
        return 0 
