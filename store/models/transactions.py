#!/usr/local/python3
# -*- coding: UTF-8 -*-

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.groups import Groups
from datetime import datetime

class Transactions(BaseModel):
    # 商品总价
    total_price = FloatField()
    # 运费
    carriage = FloatField()
    # 支付方式(1微信 2支付宝 3余额)
    pay_way = IntegerField(null=True)
    # 配送方式(快递  货到付款)
    send_way = CharField()
    # 购买类型(1普通产品，2积分产品)
    buy_types = IntegerField(default = 1)
    # 订单id
    trade_id = CharField(unique=True)
    # 删除状态(0未删除，-1已删除)
    del_status = IntegerField(default=0)
    # 订单状态(1待付款, 2已付款, 3待收货, 4已收货, 5待发货, 6已发货, 7退款中, 8退款完成)
    trade_status = IntegerField()
    # 描述
    description = TextField(null=True)
    # 收货信息(收货人 + 手机号 + 地址 + 邮编)
    address = TextField()
    # 备注
    remark = TextField(null=True)
    # 订单所属商铺
    groups = ForeignKeyField(Groups, related_name='trans_groups')
    # 订单所属用户
    users = ForeignKeyField(Users, related_name='users_groups')
    # 创建时间
    created_time = DateTimeField(default=datetime.now)
