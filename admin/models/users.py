#!/usr/local/python3
# -*- coding: UTF-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import*
from models.base import *
import datetime

class Users(Base):
    # 表的名字:
    __tablename__ = 'users'
    # id
    nid = Column(Integer, primary_key=True, autoincrement=True)
    # 姓名
    name = Column(String(20))
    # 电话
    phone = Column(String(20), unique=True)
    # 昵称
    nickname = Column(String(20))
    # 密码
    password = Column(String(20))
    # 登录状态
    cookie_num = Column(String(20))
    # 用户头像
    avatur = Column(Text)
    # 余额
    balance = Column(Float)
    # 积分
    integral = Column(Integer)
    # 性别
    gender = Column(String(20))
    # 出生日期
    birthday = Column(String(20))
    # 最后登录时间
    login_time = Column(DateTime)    
    # 用户创建时间
    created_time = Column(DateTime, default=datetime.datetime.now())
    # 关系
    groups = relationship("Groups", backref="users")

    def __repr__(self):
        output = "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" \
                 %(self.nid, self.name, self.phone, self.nickname,\
                 self.password, self.cookie_num, self.avatur, self.balance,\
                 self.integral, self.gender, self.birthday, self.login_time, self.created_time)
        return output
