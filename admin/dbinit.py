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
    Base.metadata.create_all(engine)

def insertData():
    # categories_first
    session = DBSession()
    categories_first = Categories(
                   name = '系统',
                   description = '系统'
                   )
    session.add(categories_first)
    session.commit()
    session.close()
    
    # categories_second
    session = DBSession()
    categories_second = Categories(
                   name = '公司',
                   description = '公司',
                   parent_name = '系统',
                   parent_id = 1
                   )
    session.add(categories_second)
    session.commit()
    session.close()
    
    # categories_third
    session = DBSession()
    categories_third = Categories(
                   name = '产品',
                   description = '产品',
                   parent_name = '系统',
                   parent_id = 1
                   )
    session.add(categories_third)
    session.commit()
    session.close()
    
    # users
    session = DBSession()
    new_users = Users(
             name = ADMINNAME, 
             phone = '18312345678', 
             nickname = '管理员', 
             password = ADMINPASSWMD,
             birthday = '2018-08', 
                   )
    session.add(new_users)
    session.commit()
    session.close()

    # groups
    session = DBSession()
    new_groups = Groups(
             name = 'fish', 
             phone = '18312345678', 
             description = '公司',
             address = '陕西',
             users_id = 1,
             categories_id = 2
                   )
    session.add(new_groups)
    session.commit()
    session.close()
     
    # setting_data
    session = DBSession()
    session.add_all(SETTING_DATA)
    session.commit()    
    session.close()
    
    # category_data
    session = DBSession()
    session.add_all(CATEGORY_DATA)
    session.commit()    
    session.close()    
        
if __name__ == '__main__':
    createTables()
    insertData()
