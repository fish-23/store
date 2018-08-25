#!/usr/local/python3
# -*- coding: UTF-8 -*-

from peewee import *
from models.base import BaseModel
from models.users import Users
from datetime import datetime
#  余额明细表
class UserBalance(BaseModel):
    # 操作用户
    user = IntegerField()
    # 所属用户
    owner = ForeignKeyField(Users, related_name='owner_userbalances', on_delete='CASCADE')
    # 变动金额
    variation_balance = FloatField(default=.0)
    # 剩余余额
    reset= FloatField(default=.0)
    # 类别：1代表余额 ， 2代表积分
    category = IntegerField(null=True)
    # 收支类别 1代表收入  2代表支出
    variation_category = IntegerField(null=True)
    #描述
    description = TextField(null=True)
    #时间
    created_time = DateTimeField(default=datetime.now)
