#!/usr/local/python3
# -*- coding: UTF-8 -*-

from peewee import *
from models.base import BaseModel
from datetime import datetime

class Users(BaseModel):
    # 姓名
    name = CharField()
    # 手机号码
    cellphone = CharField(null=True)
    # 昵称
    nickname = CharField(null=True)
    # 密码
    password = CharField()
    # 登录状态
    cookie_num = CharField(null=True)
    # 用户头像
    avatur = TextField(null=True) 
    # 头像地址
    avaturaddr = TextField(null=True)   
    # 余额
    balance = FloatField(default=.0)
    # 积分
    integral = IntegerField(default = 0)
    # 性别
    gender = CharField(null=True)
    # 出生日期
    birthday = CharField(null=True)
    # 最后登录时间
    login_time = DateTimeField(null=True)   
    # 邮件发送时间
    sms_time = DateTimeField(null=True) 
    # 用户创建时间
    created_time = DateTimeField(default=datetime.now) 
