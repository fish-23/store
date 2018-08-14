#!/usr/local/python3
# -*- coding: UTF-8 -*-

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.products import Products
from models.product_parameters import ProductParameters
from datetime import datetime

class ShoppingCart(BaseModel):
    # 购买数量
    num = IntegerField()
    # 产品分类
    product_parameters = ForeignKeyField(ProductParameters, related_name='cart_product_parameters', on_delete='CASCADE')
    # 产品
    product = ForeignKeyField(Products, related_name='cart_products', on_delete='CASCADE')
    # 用户
    users = ForeignKeyField(Users, related_name='cart_users', on_delete='CASCADE')
    # 加入时间
    created_time = DateTimeField(default=datetime.now)

