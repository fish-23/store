#!/usr/local/python3
# -*- coding: UTF-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import*
from models.base import *

class Categories(Base):
    # 表的名字:
    __tablename__ = 'categories'
    # id
    nid = Column(Integer, primary_key=True, autoincrement=True)
    # 名字
    name = Column(String(50))
    # 描述
    description = Column(Text)
    # parent
    parent_id = Column(Integer, ForeignKey('categories.nid'))
