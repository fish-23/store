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
from models.categories import *
from models.groups import *


# register
def checkCellphone(cellphone):
    try:
        selectphone = Users.select().where(User.cellphone == cellphone).count()
        if selectphone != 0:
            return -1
        phoneprefix = ['130','131','132','133','134','135','136','137','138','139','150','151', \
                       '152','153','156','158','159','170','183','182','181','185','186','188','189']
        if len(cellphone) != 11 or cellphone.isdigit() != True or cellphone[:3] not in phoneprefix:
            return -2
        return 0
    except Exception as e:
        log.error(traceback.format_exc())

        
