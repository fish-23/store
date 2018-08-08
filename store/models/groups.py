#!/usr/local/python3
# -*- coding: UTF-8 -*-

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.categories import Categories
from datetime import datetime

class Groups(BaseModel):
    # 店铺名称
    name = CharField(null=True)
    # 描述
    description = TextField(null=True)
    # 缩略图
    thumbnail = TextField(null=True)
    # 地址
    address = TextField(null=True)
    # 服务热线
    phone = CharField(null=True)    
    # 分类
    category = ForeignKeyField(Categories, related_name='category_groups', on_delete='CASCADE')
    # 拥有者
    owner = ForeignKeyField(Users, related_name='owner_groups', on_delete='CASCADE')
    # 公司创建时间
    created_time = DateTimeField(default=datetime.now)  
