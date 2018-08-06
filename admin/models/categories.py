#!/usr/local/python3
# -*- coding: UTF-8 -*-

from peewee import *
from models.base import BaseModel

class Categories(BaseModel):
    name = CharField()
    description = TextField()
    parent_name = CharField(null = True)
    parent = ForeignKeyField('self', null=True, related_name='children')
