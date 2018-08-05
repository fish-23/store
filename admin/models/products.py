#!/usr/local/python3
# -*- coding: UTF-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import*
from models.base import *
from models.categories import *
from models.groups import *
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
    stock = Column(Integer)
    # 产品创建时间
    created_time = Column(DateTime, default=datetime.datetime.now())
    # 分类
    categories_id = Column(Integer, ForeignKey('categories.nid'))
    # 公司
    groups_id = Column(Integer, ForeignKey('groups.nid'))
    # 关系
    productparameters = relationship("ProductParameters", backref="products")
    
    def __repr__(self):
        output = "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" \
                 %(self.nid, self.name, self.price, self.discount, self.created_time, self.picaddr,\
                 self.thumbnail, self.description, self.stock, self.categories_id, self.groups_id)
        return output
