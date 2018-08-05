#!/usr/local/python3
# -*- coding: UTF-8 -*-

from models.base import *
from models.users import *
from models.products import *
from models.categories import *
import sys
sys.path.append('/root')
from config import *


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
                   name = '产品',
                   description = '产品',
                   parent_id = 1
                   )
    session.add(categories_second)
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
if __name__ == '__main__':
    createTables()
    insertData()
