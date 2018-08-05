#!/usr/local/python3
# -*- coding: UTF-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import*
from models.base import *
from models.products import *
import datetime

class ProductParameters(Base):
    # 表的名字:
    __tablename__ = 'product_parameters'
    # id
    nid = Column(Integer, primary_key=True, autoincrement=True)
    # 产品价格
    price = Column(Float)
    # 产品折扣价格
    discount = Column(Float)
    # 规格描述
    description = Column(Text)
    # 库存
    stock = Column(Integer)
    # 产品
    products_id = Column(Integer, ForeignKey('products.nid'))
    # 规格创建时间
    created_time = Column(DateTime, default=datetime.datetime.now())    
    
    def __repr__(self):
        output = "(%s,%s,%s,%s,%s,%s,%s)" \
                 %(self.nid, self.price, self.discount, self.stock, \
                   self.description, self.products_id, self.created_time)
        return output    
