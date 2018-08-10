#!/usr/local/python3
# -*- coding: UTF-8 -*-

from peewee import *
from models.base import BaseModel
from datetime import datetime

class Ips(BaseModel):
    # ip地址
    ipaddr = CharField(null=True)
    # 发送数量
    num = IntegerField(default = 0)
    # 发送时间
    sendsms_time = IntegerField()
    # ip访问时间
    created_time = DateTimeField(default=datetime.now)  
