﻿#!/usr/local/python3
# -*- coding: UTF-8 -*-

import time,datetime
import io
import traceback
from PIL import Image
import sys
sys.path.append('/root')
from log import *
from models.payments import *
from models.transactions import *


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
    try:
        fd = open(file_name, "r")
        ct = str(fd.read())
        fd.close()
        return ct
    except Exception as e:
        log.error(traceback.format_exc())


# 产品管理
def listHtml(ret):
    try:
        h = u'<html><body>'
        display_space = '&nbsp'*6
        log.info('1111111111')
        log.info(ret)
        for i in ret:
            html_nid = i.id
            html_name = i.name
            html_price = i.price
            html_discount  = i.discount 
            html_num  = i.num
            html_description  = i.description
            html_picaddr  = i.picaddr 
            html_thumbnail = i.thumbnail
            html_category = i.category.name                  
            html_createdtime  = i.created_time 
            html_createdtime = str(html_createdtime)
            html_createdtime = html_createdtime[:10]
            h = h + '<font>' + '产品分类：' + html_category + '</font>' + display_space
            h = h + '<font>' + '产品名称：' + html_name + '</font>' + display_space
            h = h + '<font>' + '产品价格：' + str(html_price) + '</font>' + display_space
            h = h + '<font>' + '折扣价格：' + str(html_discount) + '</font>' + '<br>'
            h = h + '<br>' +  '<font>' + '库存余量：' + str(html_num) + '</font>' + display_space                  
            h = h + '<font>' + '产品详情：' + html_description + '</font>' +  '<br>'
            h = h + '<br>' + '产品缩略图：' + '<img src="data:image/jpg;base64,%s"/>'%html_thumbnail + '<br>'
            h = h + '<br>' + '<a href="/parameters_list/' + str(html_nid) + u'">产品规格</a>' + display_space
            h = h + '<a href="/product_del/' + str(html_nid) + u'">删除</a>' + display_space 
            h = h + '<a href="/product_modify/' + str(html_nid) + u'">修改</a ><br>'+'<br>'
        welcome = u'<fieldset><legend><h2>产品列表</h2></legend>'
        entry_time = '<br>' + u'进入时间:' + display_space +'%s'%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        add_link = u'<a href="/product_add">点击添加</a ><body></html>'
        index_link = u'<a href="/">点击返回主页</a ><body></html>'+ '<br>'
        h = welcome+ h + '<br>' + add_link + display_space + index_link + entry_time
        return h
    except Exception as e:
        log.error(traceback.format_exc())

def listModifyHtml(ret):
    try:
        html_name = ret.name
        html_price = ret.price
        html_discount  = ret.discount
        html_num  = ret.num
        html_description  = ret.description
        picaddr = ret.picaddr
        category = ret.category.name
        display_space = '&nbsp'*6                  
        h = '<html><body>'
        h = h + '<form action="/api/v1/product_modify" method="post" enctype="multipart/form-data">'  
        h = h + '<font color="red">'+ u'产品分类：' + category + display_space                    
        h = h + '<font color="red">'+ u'产品名称：' + html_name + display_space                            
        h = h + '<font color="red">'+ u'产品价格：' + str(html_price) + '<br>'                    
        h = h + '<br>' +  '<font color="red">'+ u'折扣价格：' + str(html_discount) + display_space
        h = h + '<font color="red">'+ u'库存余量：' + str(html_num) + display_space                  
        h = h + '<font color="red">'+ u'产品详情：' + html_description + '<br>'
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
    except Exception as e:
        log.error(traceback.format_exc())

def parametersHtml(findret, product_nid):
    try:
        h = u'<html><body>'
        display_space = '&nbsp'*6
        for i in findret:
            html_nid = i.id
            html_price = i.price 
            html_discount  = i.discount
            html_description  = i.description 
            html_num  = i.num
            html_createdtime  = i.created_time
            html_createdtime = str(html_createdtime)
            html_createdtime = html_createdtime[:10]
            h = h + '<font>' + '规格描述：' + str(html_description) + '</font>' + display_space
            h = h + '<font>' + '规格价格：' + str(html_price) + '</font>' + display_space
            h = h + '<font>' + '折扣价格：' + str(html_discount) + '</font>' + display_space
            h = h + '<font>' + '规格库存：' + str(html_num) + '</font>' + display_space
            h = h + '<font>' + '创建时间：' + html_createdtime + '</font>' + display_space
            h = h + '<font>' + '<a href="/parameters_del/' + str(html_nid) + u'">删除</a>' + '<br>'
        welcome = u'<fieldset><legend><h2>规格列表</h2></legend>'
        entry_time = u'进入时间:' + display_space +'%s'%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        add_link = '<br>' + u'<a href="/parameters_add/' + str(product_nid) + u'">点击添加</a ><body></html>' + display_space
        product_link = u'<a href="/product_list_admin">点击返回产品列表</a ><body></html>' + display_space
        index_link =  u'<a href="/">点击返回主页</a ><body></html>' + '</br>'
        h = welcome+ h  + '<br>' + add_link + product_link + index_link + entry_time
        return h
    except Exception as e:
        log.error(traceback.format_exc())

# 用户管理
def userListHtml(userret):
    try:
        h = u'<html><body>'
        display_space = '&nbsp'*6
        for i in userret:
            html_nid = i.id
            html_name = i.name
            html_cellphone = i.cellphone
            html_nickname = i.nickname 
            html_avatur = i.avatur
            html_balance = i.balance 
            html_integral = i.integral 
            html_createdtime  = i.created_time
            html_createdtime = str(html_createdtime)
            html_createdtime = html_createdtime[:10]
            h = h + '<font>' + '昵称：' + html_nickname + '</font>' + display_space
            h = h + '<font>' + '姓名：' + html_name + '</font>' + display_space
            h = h + '<font>' + '电话：' + html_cellphone + '</font>' + display_space
            h = h + '<font>' + '余额：' + str(html_balance) + '</font>' + display_space
            h = h + '<font>' + '积分：' + str(html_integral) + '</font>' + display_space
            h = h + '<font>' + '注册时间：' + html_createdtime + '</font>' + display_space
            h = h + '<font>' + '<a href="/user_del/' + str(html_nid) + u'">删除</a>' + display_space
            h = h + '<font>' + '<a href="/user_recharge/' + str(html_nid) + u'">充值</a>' + '<br>'
        welcome = u'<fieldset><legend><h2>用户列表</h2></legend>'
        entry_time = u'进入时间:' + display_space +'%s'%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        user_link = '<br>' + u'<a href="/user_list/none">点击返回用户列表</a ><body></html>' + display_space
        index_link = u'<a href="/">点击返回主页</a ><body></html>' + '</br>'
        search_link = '<form action="/api/v1/user_list" method="post">'
        search_link = search_link + '<font color="red"><h3>' + '用户名(手机号)：' + '<input type="text" name="name_phone"/>' 
        search_link = search_link + '<input type="submit" value="搜索"/>' + '</h3></font>' +'</form>'
        h = welcome + search_link  + h  + '<br>' + user_link + index_link + entry_time
        return h
    except Exception as e:
        log.error(traceback.format_exc())

def userRechargeHtml(user_info, operate_id):
    try:
        h = '<html><body>'
        h = h + '<form action="/api/v1/user_recharge" method="post" enctype="multipart/form-data">' 
        h = h + '<fieldset>'
        h = h + '<legend>' + ' <h2>' + '余额充值' + ' </h2>' + '</legend>'
        nid = user_info.id
        balance = user_info.balance
        name = user_info.name
        h = h + '<h3>'
        h = h + '<input type="hidden" name="operate_id" value="%s"/>'%operate_id
        h = h + '<input type="hidden" name="nid" value="%s"/>'%nid
        h = h + '<input type="hidden" name="dbbalance" value="%s"/>'%balance
        h = h + '<font color="red">' + '用户名：' + name +'</font>' + '<br>'
        h = h + '<font color="red">' + '可用余额：￥' + str(balance) + '</font>' + '<br>' + '<br>'
        h = h + '<font color="blue">' + '本次充值金额：' + '<input type="text" name="balance"/>' + '</font><br><br>'
        h = h + '<input type="submit" value="充值">'
        h = h + '</h3>'
        h = h + '</body></html>'
        return h
    except Exception as e:
        log.error(traceback.format_exc())


# 邮费管理
def carriageHtml(findret):
    try:
        h = u'<html><body>'
        display_space = '&nbsp'*6
        for i in findret:
            html_nid = i.id
            html_name = i.name
            html_value  = i.value
            html_description = i.description 
            h = h + '<font>' + '包邮界限：' + html_name + '</font>' + display_space
            h = h + '<font>' + '邮费：' + html_value + '</font>' + display_space
            h = h + '<font>' + '<a href="/carriage_del/' + str(html_nid) + u'">删除</a>' + '<br>'
        welcome = u'<fieldset><legend><h2>邮费管理</h2></legend>'
        entry_time = u'进入时间:' + display_space +'%s'%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        add_link = '<br>' + u'<a href="/carriage_add">点击添加</a ><body></html>' + display_space
        index_link = u'<a href="/">点击返回主页</a ><body></html>' + '</br>'
        h = welcome+ h  + '<br>' + add_link + index_link + entry_time
        return h
    except Exception as e:
        log.error(traceback.format_exc())


# 订单管理
def transHtml(trans_info):
    try:
        h = '<html>'
        if trans_info.count():
            trans_id = [i.id for i in trans_info]
            for item in trans_id:
                trans_ret = Transactions.get(Transactions.id == item)
                created_time = trans_ret.created_time
                time_stamp = int(created_time.timestamp())
                now_time = int(time.time())
                if trans_ret.trade_status == 1:
                    if (now_time -time_stamp) > 7200:
                        continue                
                total_price = trans_ret.total_price
                carriage = trans_ret.carriage
                trade_id = trans_ret.trade_id
                users_name = trans_ret.users.name
                nid = trans_ret.id
                h = h + '<font color="blue"><h3>'
                h = h + '<font>' + '编号：' + str(nid) + '</font>' + display_space
                h = h + '<font>' + '用户：' + users_name + '</font>' + display_space
                h = h + '<font>' + '总价：￥' + str(total_price) + '</font>' + display_space
                h = h + '<font>' + '订单创建时间：' + str(created_time) + '</font>' + display_space
                h = h + '<a href="/trans_details/' + str(item) + u'">详情</a>' 
                h = h + '</font></h3>'
        else:
            h = '<font color="red"><h3>' + '没有相应的订单' + '</font></h3>'
        welcome = u'<fieldset><legend><h2>订单管理</h2></legend>'
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        entry_time = '<h3>' + u'进入时间:' + display_space +'%s'%(time_now) + '</h3>'        
        index_link = u'<a href="/">进入主页</a ><body></html>'+ '</h3>'
        trans_link = '<h3>' + u'<a href="/trans_list">进入订单管理</a ><body></html>' + display_space    
        h = welcome + h + trans_link + index_link + entry_time
        return h
    except Exception as e:
        log.error(traceback.format_exc())

def transDetailsHtml(trans_info):
    try:
        h = '<html>'
        total_price = trans_info.total_price
        users_name = trans_info.users.name
        nid = trans_info.id
        created_time = trans_info.created_time
        carriage  = trans_info.carriage
        address = trans_info.address
        remark = trans_info.remark
        pay_way = '余额'
        send_way = '快递'
        h = h + '<font color="red"><h3>' + '订单信息' + '</font></h3>'
        h = h + '<font color="blue"><h3>'
        h = h + '编号：' + str(nid) + display_space
        h = h + '用户：' + users_name + display_space
        h = h + '总价：￥' + str(total_price) + display_space
        h = h + '订单创建时间：' + str(created_time) + '<br>'
        h = h + '配送方式' + send_way  + display_space
        h = h + '支付方式' + pay_way + display_space
        h = h + '收货地址' + address
        h = h + '</font></h3>'
        h = h + '<font color="red"><h3>' + '买家留言：' + remark + '</font></h3>'
        h = h + '<font color="red"><h3>' + '产品信息' + '</font></h3>'
        payments_info = Payments.select().where(Payments.transactions == nid,Payments.del_status == 0)
        for item in payments_info:
            name = item.products.name
            thumbnail = item.products.thumbnail
            num = item.num
            discount = item.parameters.discount
            description = item.parameters.description
            h = h + '<font color="blue"><h3>'
            h = h + '<img src="data:image/jpg;base64,%s"/>'%thumbnail + display_space
            h = h + '商品名称：' + name + '</font>' + display_space
            h = h + '价格：￥' + str(discount) + display_space
            h = h + '规格描述：' + description + display_space
            h = h + '购买数量：' + str(num) 
            h = h + '</font></h3><br>'        
        welcome = u'<fieldset><legend><h2>订单详情</h2></legend>'
        time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        entry_time = '<h3>' + u'进入时间:' + display_space +'%s'%(time_now) + '</h3>'        
        index_link = u'<a href="/">进入主页</a ><body></html>'+ '</h3>'
        trans_link = '<h3>' + u'<a href="/trans_list">进入订单管理</a ><body></html>' + display_space    
        h = welcome + h + trans_link + index_link + entry_time
        return h
    except Exception as e:
        log.error(traceback.format_exc())
