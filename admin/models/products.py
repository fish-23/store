#!/usr/local/python3
# -*- coding: UTF-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import*
from base import *
import datetime

class Products(Base):
    # 表的名字:
    __tablename__ = 'products'
    # id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 产品名
    name = Column(String(20))
    # 产品价格
    price = Column(Float)
    # 折扣价格
    discount = Column(Float)
    # 产品缩略图
    thumbnail = Column(Text)
    # 产品详情
    description = Column(Text)
    # 库存
    num = Column(Integer)
    # 用户表
    users_id = Column(Integer, ForeignKey('users.id'))
    # 产品创建时间
    created_time = Column(DateTime, default=datetime.datetime.now())
