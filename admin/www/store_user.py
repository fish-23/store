#!/usr/local/python3
# -*- coding: UTF-8 -*-

import traceback
import time,datetime
import sys
import base64
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
        log.info(pic_ext)
        log.info(type(pic_ext))
        if str(pic_ext) not in ['.jpeg', '.bmp', '.png', '.webp', '.gif', '.jpg']:
            return(-1)
        pic.filename = ''.join(('%s_pic'%name, pic_ext))
        pic.save(PATHPWD,overwrite=True)
        picname = pic.filename
        picaddr = PATHPWD + picname
        return recordImage(picaddr,pic) 
        #pic = pic.file.read()
    except Exception as e:
        log.error(traceback.format_exc())

def recordImage(picaddr,pic):
    try:
        session = DBSession()
        new_product = Products(picaddr = picaddr, users_id = 1)
        session.add(new_product)       
        session.commit()
        session.close()
    except Exception as e:
        log.error(traceback.format_exc()) 
