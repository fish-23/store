#!/usr/local/python3
# -*- coding: UTF-8 -*-

from peewee import *
from models.base import BaseModel
from models.categories import Categories
from models.groups import Groups
from datetime import datetime

class Products(BaseModel):
    # 产品名称
    name = CharField(null=True)
    # 产品价格
    price = FloatField(default=.0)
    # 产品折扣价
    discount = FloatField(default=.0)    
    # 产品描述
    description = TextField(null=True)
    # 库存
    num = IntegerField(default = 1)  
    # 产品缩略图
    thumbnail = TextField(null=True)
    # 原图地址
    picaddr = TextField(null=True)   
    # 产品创建时间
    created_time = DateTimeField(default=datetime.now)
    # 所属分类
    category = ForeignKeyField(Categories, related_name='category_products', on_delete='CASCADE')
    # 所属店铺
    group = ForeignKeyField(Groups,related_name='products_groups',on_delete='CASCADE') 
