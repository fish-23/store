#!/usr/local/python3
# -*- coding: UTF-8 -*-

import os
import hashlib

# mysql
MYUSER = '数据库用户名'
MYPASSWORD = '数据库密码'
MYHOST = '127.0.0.1'
MYDATABASE = '数据库库名(admin)'
MYDATABASES = '数据库库名(store)'

# 腾讯云SMS
SMSAPPID =  '腾讯云SMS ID'
SMSAPPKEY = '腾讯云SMS 秘钥'
TEMPLATE_ID = '短信模板ID'
PHONE = ['调试用的手机号']

# 图片存储
PATHRUN = os.getcwd()
PATHPWD = os.path.join(PATHRUN, 'static/products/') #产品图片地址
PATHPWDU = os.path.join(PATHRUN, 'static/users/')  # 用户头像地址

# admin
ADMINNAME = 'admin 账号'
ADMINPASSW = 'admin 密码'
ADMINPASSWMD = hashlib.md5(ADMINPASSW.encode("utf8")).hexdigest()
