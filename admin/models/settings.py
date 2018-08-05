#!/usr/local/python3
# -*- coding: UTF-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import*
from models.base import *

class Settings(Base):
    # 表的名字:
    __tablename__ = 'settings'
    # id
    nid = Column(Integer, primary_key=True, autoincrement=True)
    # 名字
    name = Column(String(50))
    # 值
    value = Column(String(50))
    # 描述
    description  = Column(Text)
    # 公司
    groups_id = Column(Integer, ForeignKey('groups.nid'))

    def __repr__(self):
        output = "(%s,%s,%s,%s,%s)" \
                 %(self.nid, self.name, self.value, self.description, self.groups_id)
        return output
