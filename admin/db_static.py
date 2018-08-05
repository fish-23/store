#!/usr/local/python3
# -*- coding: UTF-8 -*-

from models.categories import *
from models.settings import *

# categories
CATEGORY_DATA = [Categories(name ='水果', description ='水果', parent_name ='产品', parent_id =3),
            Categories(name ='蔬菜', description ='蔬菜', parent_name ='产品', parent_id =3)
            ]

# settings
SETTING_DATA = [Settings(name =100, value =10, description ='运费', groups_id=1)
           ]        
