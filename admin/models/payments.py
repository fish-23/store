#!/usr/local/python3
# -*- coding: UTF-8 -*-

from peewee import *
from models.base import BaseModel
from models.products import Products
from models.product_parameters import ProductParameters
from models.transactions import Transactions
from datetime import datetime

class Payments(BaseModel):
    # 购买数量
    num = IntegerField()
    # 产品名
    products = ForeignKeyField(Products, related_name='payments_products')
    # 产品规格id
    parameters = ForeignKeyField(ProductParameters, related_name='payments_parameters')
    # 订单
    transactions = ForeignKeyField(Transactions, related_name='payments_trans')
    # 删除状态(0未删除，-1已删除)
    del_status = IntegerField(default=0)
    # 删除时间
    del_time = = DateTimeField(null=True)
    # 描述
    description = TextField(null=True)
    # 购买时间
    created_time = DateTimeField(default=datetime.now)
