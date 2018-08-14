#!/usr/local/python3
# -*- coding: UTF-8 -*-

from models.base import *
from models.users import *
from models.products import *
from models.categories import *
from models.groups import *
from models.product_parameters import *
from models.settings import *
from models.ips import *
from models.shopping_cart import *

import sys
sys.path.append('/root')
from config import *
from db_static import *


def createTables():
    tables = [
         Users,
         Products,
         Categories,
         Groups,
         ProductParameters,
         Settings,
         Ips,
         ShoppingCart
         ] 
    db.create_tables(tables)

def insertData():
    # categories
    categories_first = Categories.get_or_create(
                   name = '系统',
                   description = '系统'
                   )
    
    categories_second = Categories.get_or_create(
                   name = '公司',
                   description = '公司',
                   parent_name = '系统',
                   parent_id = 1
                   )
    
    categories_third = Categories.get_or_create(
                   name = '产品',
                   description = '产品',
                   parent_name = '系统',
                   parent_id = 1
                   )
    
    # users
    new_users = Users.get_or_create(
             name = ADMINNAME, 
             cellphone = '18312345678', 
             nickname = '管理员', 
             password = ADMINPASSWMD,
             birthday = '2018-08', 
                   )

    # groups
    new_groups = Groups.get_or_create(
             name = 'fish', 
             phone = '18312345678', 
             description = '公司',
             address = '陕西',
             owner = 1,
             category = 2
                   )
    
    # setting_data
    Settings.insert_many(SETTING_DATA).execute()
    
    # category_data
    Categories.insert_many(CATEGORY_DATA).execute()   
        
if __name__ == '__main__':
    createTables()
    insertData()
