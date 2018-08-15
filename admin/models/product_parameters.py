#!/usr/local/python3
# -*- coding: UTF-8 -*-

from peewee import *
from models.base import BaseModel
from models.products import Products
from datetime import datetime

class ProductParameters(BaseModel):
    # 产品价格
    price = FloatField(default=.0)
    # 产品折扣价格
    discount = FloatField(default=.0)
    # 规格描述
    description = TextField(null=True)
    # 库存
    num = IntegerField(default = 0)
    # 删除状态(0未删除，-1已删除)
    del_status = IntegerField(default=0)
    # 规格创建时间
    created_time = DateTimeField(default=datetime.now)    
    # 产品参数所属产品
    product = ForeignKeyField(Products, related_name='productparameters_product', on_delete='CASCADE')   
