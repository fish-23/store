#!/usr/local/python3
# -*- coding: UTF-8 -*-

from models.base import *
from models.users import *
from models.products import *
from models.categories import *
from models.groups import *
from models.product_parameters import *
from models.settings import *

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
         Settings
         ] 
    db.create_tables(tables)

def insertData():
    # categories
    categories_first = Categories.create(
                   name = '系统',
                   description = '系统'
                   )
    
    categories_second = Categories.create(
                   name = '公司',
                   description = '公司',
                   parent_name = '系统',
                   parent_id = 1
                   )
    
    categories_third = Categories.create(
                   name = '产品',
                   description = '产品',
                   parent_name = '系统',
                   parent_id = 1
                   )
    
    # users
    new_users = Users.create(
             name = ADMINNAME, 
             cellphone = '18312345678', 
             nickname = '管理员', 
             password = ADMINPASSWMD,
             birthday = '2018-08', 
                   )

    # groups
    print('1111111111111111111111111111111111')
    new_groups = Groups.create(
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
