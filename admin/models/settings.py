#!/usr/local/python3
# -*- coding: UTF-8 -*-


from peewee import *
from models.base import BaseModel
from models.groups import Groups

class Settings(BaseModel):
    name = CharField(null=True)
    value = TextField(null=True)
    description = TextField(null=True)
    groups = ForeignKeyField(Groups, related_name='group_settings', on_delete='CASCADE')
