#!/usr/local/python3
# -*- coding: UTF-8 -*-

import traceback
import time,datetime
import sys
import base64
import io
sys.path.append('../')
sys.path.append('/root')
from log import *
from config import *
from PIL import Image
from models.base import *
from models.users import *
from models.products import *


# login
def check_login(name, password):
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
def saveproduct(name, num, price, discount, description, pic):
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
        # 查询name
        session = DBSession()
        ret = session.query(Products.name).filter(Products.name == name).first()
        session.commit()
        session.close()
        if ret:
            return -3
        # 产品增加
        session = DBSession()
        new_product = Products(name=name, num=num, price=price, discount=discount,
                              description=description, users_id = 1)
        session.add(new_product)
        session.commit()
        session.close()
        # 查询id
        session = DBSession()
        ret = session.query(Products.nid).filter(Products.name == name).first()
        session.commit()
        session.close()
        nid = ret[0]
        return nid        
    except Exception as e:
        log.error(traceback.format_exc())
