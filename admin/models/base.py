#!/usr/local/python3
# -*- coding: UTF-8 -*-

import sys
sys.path.append('/root')
from config import *
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import *
import mysql.connector


Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://%s:%s@localhost:3306/%s'%(MYUSER,MYPASSWORD,MYDATABASES), encoding="utf-8")
DBSession = sessionmaker(bind=engine)


