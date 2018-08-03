#!/usr/local/python3
# -*- coding: UTF-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import*
from models.base import *
from models.users import *
import datetime

class Products(Base):
    # 表的名字:
    __tablename__ = 'products'
    # id
    nid = Column(Integer, primary_key=True, autoincrement=True)
    # 产品名
    name = Column(String(20))
    # 产品价格
    price = Column(Float)
    # 折扣价格
    discount = Column(Float)
    # 产品缩略图
    thumbnail = Column(Text)
    # 原图地址
    picaddr = Column(Text)
    # 产品详情
    description = Column(Text)
    # 库存
    num = Column(Integer)
    # 用户表
    users_id = Column(Integer, ForeignKey('users.nid'))
    # 产品创建时间
    created_time = Column(DateTime, default=datetime.datetime.now())
    def __repr__(self):
        output = "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" \
                 %(self.nid, self.name, self.price, self.discount, self.created_time,\
                 self.thumbnail, self.picaddr, self.description, self.num, self.users_id)
        return output
Base.metadata.create_all(engine)
