#!/usr/bin/python
# -*- coding: UTF-8 -*-

display_space = '&nbsp' + '&nbsp' + '&nbsp' + '&nbsp' + '&nbsp' + '&nbsp'

def red_writing(msg):
	return u'<html><font color="red"><h3>%s</h3></font></html>'%(msg)

def red_writing_1(msg,addr,msg2):
	return u'<html><font color="red"><h3>%s</h3></font></html><br> <a href="%s"><h3>%s</h3></a>'%(msg,addr,msg2)

def red_writing_2(msg,addr,msg2,addr2,msg3):
        # red_writing_2(u'用户名不能为空','/login',u'点击重新登录','/todo',u'点击进入todo主页')
	return u'<font color="red"><h3>%s</h3></font><br> <a href="%s"><h3>%s</h3></a> <a href="%s"><h3>%s</h3></a>'%(msg,addr,msg2,addr2,msg3)

def red_writing_3(msg,addr,msg2,addr2,msg3,addr3,msg4):
	return u'<html><font color="red"><h3>%s</h3></font></html><br> <a href="%s"><h3>%s</h3></a> \
                 <a href="%s"><h3>%s</h3></a> <a href="%s"><h3>%s</h3></a>'%(msg,addr,msg2,addr2,msg3,addr3,msg4)

def hyperlink(addr,msg):
	return u'<a href="%s"><h4>%s</h4></a>'%(addr,msg)

def hyperlink_3(addr,msg,addr2,msg2,addr3,msg3):
	return u'<a href="%s"><h3>%s</h3></a> <a href="%s"><h3>%s</h3></a> <a href="%s"><h3>%s</h3></a>'%(addr,msg,addr2,msg2,addr3,msg3)

def read_file(file_name):
	fd = open(file_name, "r")
	ct = str(fd.read())
	fd.close()
	return ct
