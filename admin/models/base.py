#!/usr/local/python3
# -*- coding: UTF-8 -*-

import sys
sys.path.append('/root')
from config import *
from peewee import *


db = MySQLDatabase(host = MYHOST, user = MYUSER, passwd = MYPASSWORD, database = MYDATABASES, charset = 'utf8') 
db.connect()

class BaseModel(Model):
    class Meta:
        database = db

