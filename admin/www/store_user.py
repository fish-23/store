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


# 图片存储
def saveImage(name, pic):
    try:
        pic_name, pic_ext = os.path.splitext(pic.filename)
        pic_ext = pic_ext.lower()
        if str(pic_ext) not in ['.jpeg', '.bmp', '.png', '.webp', '.gif', '.jpg']:
            return(-1)
        
        pic.filename = ''.join(('%s_pic'%name, pic_ext))
        pic.save(PATHPWD,overwrite=True)
        picname = pic.filename
        picaddr = PATHPWD + picname
        return recordImage(picaddr,pic) 
    except Exception as e:
        log.error(traceback.format_exc())

def recordImage(picaddr,pic):
    try:
        pic = pic.file
        img = Image.open(pic)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        imge = img.resize((100,70))
        # 存储
        session = DBSession()
        new_product = Products(picaddr = picaddr, users_id = 1)
        session.add(new_product)       
        session.commit()
        session.close()
        # 查id
        session = DBSession()          
        ret = session.query(Products.nid).filter(Products.picaddr == picaddr).first()          
        session.commit()
        session.close() 
        # 查询结束 
        nid = ret[0] 
        lis = []
        lis.append(picaddr)
        lis.append(ret)      
        return lis
    except Exception as e:
        log.error(traceback.format_exc())

def saveproduct(name, num, price, discount, description):
    try:
        print(price)
        print(type(price))
        price = int(price)
        print(type(price)) 
        try:
            num = int(num)
            print('1111111')
            price = float(price)
            print('2222222222')
            discount = float(discount)
            print('33333333333333')
        except Exception as e:
            return -1
        session = DBSession()
        new_product = Products(picaddr = picaddr, users_id = 1)
        session.add(new_product)
        session.commit()
        session.close()
    except Exception as e:
        log.error(traceback.format_exc())
 
