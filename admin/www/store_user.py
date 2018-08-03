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


# login
def checkLogin(name, password):
    if name != ADMINNAME or password != ADMINPASSW:
        return -1
    return 0


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
        imge = img.resize((100,70))
        # 存缩略图
        session = DBSession()
        ret = session.query(Products).filter(Products.nid == nid).first()
        ret.picaddr = picaddr
        session.commit()
        session.close()
        return 0
    except Exception as e:
        log.error(traceback.format_exc())


# 产品管理
def saveProduct(name, num, price, discount, description, pic, user_name):
    try:
        try:
            num = int(num)
            price = float(price)
            discount = float(discount)
        except Exception as e:
            return -1
        if name == '':
            return -2
        if pic == None:
            return -4
        # 查找用户id
        session = DBSession()
        ret = session.query(Users.nid).filter(Users.name == user_name).first()
        session.commit()
        session.close()
        users_id = ret[0]        
        # 查找产品名
        session = DBSession()
        ret = session.query(Products.name).filter(Products.name == name).first()
        session.commit()
        session.close()
        if ret:
            return -3
        # 增加产品
        session = DBSession()
        new_product = Products(name=name, num=num, price=price, discount=discount,
                               description=description, users_id = users_id)
        session.add(new_product)
        session.commit()
        session.close()
        # 查找产品id
        session = DBSession()
        ret = session.query(Products.nid).filter(Products.name == name).first()
        session.commit()
        session.close()
        nid = ret[0]
        return nid        
    except Exception as e:
        log.error(traceback.format_exc())

def findProduct(name):
    try:
        # 查找用户id
        session = DBSession()
        ret = session.query(Users.nid).filter(Users.name == name).first()
        session.commit()
        session.close()
        users_id = ret[0]
        # 查找产品
        session = DBSession()
        ret =  session.query(Products).filter(Products.users_id == users_id).order_by(Products.nid.desc())
        session.commit()
        session.close()
        if ret == []:
            return -1
        return ret  
    except Exception as e:
        log.error(traceback.format_exc())

def delProduct(html_nid):
        # 查找图片路径
        session = DBSession()
        ret =  session.query(Products.picaddr).filter(Products.nid == html_nid).one()
        session.commit()
        session.close() 
        picaddr = ret.picaddr
        # 删除产品
        session = DBSession()
        session.query(Products).filter(Products.nid == html_nid).delete()
        session.commit()
        session.close()
        # 删除图片                  
        os.system('rm -rf %s'%picaddr)
        return 0 

def modifyProduct(html_nid):                
        # 查找产品信息
        session = DBSession()
        ret =  session.query(Products).filter(Products.nid == html_nid)
        session.commit()
        session.close()
        return listModifyHtml(ret)
