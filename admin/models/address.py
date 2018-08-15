#!/usr/local/python3
# -*- coding: UTF-8 -*-

from peewee import *
from models.base import BaseModel
from models.users import Users
from datetime import datetime

class Adress(BaseModel):
    # 姓名
    name = CharField()
    # 电话
    phone = CharField()
    # 省市区
    city = TextField()
    # 地址
    adress = TextField()
    # 邮编
    postcode = CharField(null=True)
    # 所属用户
    users = ForeignKeyField(Users, related_name='adress_users', on_delete='CASCADE')
    # 创建时间
    created_time = DateTimeField(default=datetime.now)
