﻿#!/usr/local/python3
# -*- coding: UTF-8 -*-
import time,datetime

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

def listHtml(ret):
    h = u'<html><body>'
    display_space = '&nbsp'*6
    for i in ret:
        html_nid = i.nid
        html_name = i.name
        html_price = i.price
        html_discount  = i.discount 
        html_num  = i.num
        html_description  = i.description
        html_picaddr  = i.picaddr                   
        html_createdtime  = i.created_time 
        html_createdtime = str(html_createdtime)
        html_createdtime = html_createdtime[:10]                  
        h = h + '<font>' + '产品名称：' + html_name + '</font>' + display_space
        h = h + '<font>' + '产品价格：' + str(html_price) + '</font>' + display_space
        h = h + '<font>' + '折扣价格：' + str(html_discount) + '</font>' + '<br>'
        h = h + '<br>' +  '<font>' + '库存余量：' + str(html_num) + '</font>' + display_space                  
        h = h + '<font>' + '产品详情：' + html_description + '</font>' +  '<br>'
        h = h + '<br>' + '产品缩略图：' + '<img src="./static/products/apple_pic.png" width="128" height="128" />' + '<br>'
        h = h + '<br>' + '<a href="/product_del/' + str(html_nid) + u'">删除</a>' + display_space 
        h = h + '<a href="/product_modify/' + str(html_nid) + u'">修改</a ><br>'
    welcome = u'<fieldset><legend><h2>产品列表</h2></legend>'
    entry_time = '<br>' + u'进入时间:' + display_space +'%s'%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    add_link = u'<br> <a href="/product_add">点击添加</a ><body></html>'
    index_link = u'<a href="/">点击返回主页</a ><body></html>'+ '<br>'
    h = welcome+ h + add_link + display_space + index_link + entry_time
    return h

def listModifyHtml(ret):
        html_name = ret.first().name
        html_price = ret.first().price
        html_discount  = ret.first().discount
        html_num  = ret.first().num
        html_description  = ret.first().description
        picaddr = ret.first().picaddr
        users_id = ret.first().users_id                  
        display_space = '&nbsp'*6                  
        h = '<html><body>'
        h = h + '<form action="/api/v1/product_modify" method="post" enctype="multipart/form-data">'                      
        h = h + '<font color="red">'+ u'产品名称：' + html_name + display_space                            
        h = h + '<font color="red">'+ u'产品价格：' + str(html_price) + display_space                    
        h = h + '<font color="red">'+ u'折扣价格：' + str(html_discount)  + '<br>'                         
        h = h + '<br>' +  '<font color="red">'+ u'库存余量：' + str(html_num) + display_space                  
        h = h + '<font color="red">'+ u'产品详情：' + html_description + '<br>'
        h = h + '<input type="hidden" name="users_id" value="%s"/>'%users_id 
        h = h + '<input type="hidden" name="picaddr" value="%s"/>'%picaddr + '<br>'
        h = h + '<p>' + '<font color=rgb(0,0,255)>' + '产品名称：' + '<input type="text" name="name"/>' + '</p>'
        h = h + '<p>' + '产品价格：' + '<input type="text" name="price"/>' + '</p>'                                 
        h = h + '<p>' + '折扣价格：' + '<input type="text" name="discount"/>' + '</p>'               
        h = h + '<p>' + '库存余量：' + '<input type="text" name="num"/>' + '</p>'                    
        h = h + '<p>' + '产品详情：' + '<input type="text" name="description"/>' + '</p>'
        h = h + '<p>' + '产品缩略图：' + '<input type="file" name="pic" />' + '</p>'
        h = h + '<p>' + '<input type="submit" value="修改"/>' + '</p>'        
        h = h + '</body></html>'
        return h
