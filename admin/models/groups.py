#!/usr/local/python3
# -*- coding: UTF-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import*
from models.base import *
import datetime

class Groups(Base):
    # 表的名字:
    __tablename__ = 'groups'
    # id
    nid = Column(Integer, primary_key=True, autoincrement=True)
    # 店铺名称
    name = Column(String(50))
    # 描述
    description = Column(Text)
    # 缩略图
    thumbnail = Column(Text)
    # 地址
    address = Column(Text)
    # 服务热线
    phone = Column(String(20))
    #phone = Column(String(20), unique=True)
    # 拥有者
    users_id = Column(Integer, ForeignKey('users.nid'))
    # 分类
    categories_id = Column(Integer, ForeignKey('categories.nid'))
    # 店铺创建时间
    created_time = Column(DateTime, default=datetime.datetime.now())  
    # 关系
    products = relationship("Products", backref="groups")
    settings = relationship("Settings", backref="groups")

    def __repr__(self):
        output = "(%s,%s,%s,%s,%s,%s,%s,%s,%s)" \
                 %(self.nid, self.name, self.description, self.thumbnail, self.phone, \
                   self.address, self.users_id, self.categories_id, self.created_time)
        return output
