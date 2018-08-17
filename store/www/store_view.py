#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import traceback
import time,datetime
sys.path.append('../')
sys.path.append('/root')
from log import *
from config import *


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

# register
def registerHtml(cellphone, send_sms):
    try:
        h = '<html><body>'
        h = h + '<form action="/api/v1/register_add" method="post" enctype="multipart/form-data">' 
        h = h + '<fieldset>'
        h = h + '<legend>' + ' <h1>' + '用户注册' + ' </h1>' + '</legend>'
        h = h + '<input type="hidden" name="dbsend_sms" value="%s"/>'%send_sms
        h = h + '<input type="hidden" name="cellphone" value="%s"/>'%cellphone
        h = h + '<p>' + '用户名：' + '<input type="text" name="name"/>' + '</p>' 
        h = h + '<p>' + '密码：' + '<input type="text" name="password"/>' + '</p>'
        h = h + '<p>' + '确认密码：' + '<input type="text" name="password2"/>' + '</p>'      
        h = h + '<p>' + '昵称：' + '<input type="text" name="nickname"/>' + '</p>'
        h = h + '<p>' + '出生日期：' + '<input type="text" name="birthday"/>' + '</p>'      
        h = h + '<p>' + '性别' + '<td colspan="2">' + '<select name="gender">' 
        h = h + '<option value="男" selected="selected">' + '男' + '</option>'
        h = h + '<option value="女">' + '女' + ' </option>' + '</select>' + '</p>'
        h = h + '<p>' + '用户头像：' + '<input type="file" name="avatur" />' + '</p>'
        h = h + '<p>' + '短信验证码：' + '<input type="text" name="send_sms"/>' + '</p>'
        h = h + '<p>' + '<input type="submit" value="提交"/>' + '</p>'
        h = h + '</body></html>'
        return h
    except Exception as e:
        log.error(traceback.format_exc())


# 产品管理
def productListHtml(ret,categories_name):
    try:
        h = u'<html><body>'
        h = h + '<font color="red">' + '<h3>' + '产品分类：%s'%categories_name + '</h3>'  + '</font>'
        for i in ret:
            html_nid = i.id
            html_name = i.name
            html_discount  = i.discount
            html_thumbnail = i.thumbnail
            html_category = i.category.name
            h = h + '<h4>' +'<img src="data:image/jpg;base64,%s"/>'%html_thumbnail + display_space
            h = h + '<font>' + '名称：' + html_name + '</font>' + display_space
            h = h + '<font>' + '价格：' + str(html_discount) + '</font>' + display_space
            h = h + '<a href="/product_details/' + str(html_nid) + u'">产品详情</a>' + '</h4>'
        h = h + '<br>'
        return h                
    except Exception as e:
        log.error(traceback.format_exc())

def productListJoinHtml(h):
    try:
        welcome = u'<fieldset><legend><h2>产品列表</h2></legend>'
        entry_time = '<br>' + u'进入时间:' + display_space +'%s'%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+'</h4>'
        index_link = '<h4>' + u'<a href="/">点击返回主页</a ><body></html>' + '<br>'
        search_link = '<form action="/api/v1/product_list" method="post">'
        search_link = search_link + '<font color="red"><h3>' + '产品名：' + '<input type="text" name="name"/>' 
        search_link = search_link + '<input type="submit" value="搜索"/>' + '</h3></font>' +'</form>' 
        h = welcome + search_link + h + index_link + entry_time
        return h
    except Exception as e:
        log.error(traceback.format_exc())

def productDetailsHtml(productret,parameterret):
    try:
        h = u'<html><body>'
        h = h + '<form action="/api/v1/product_details" method="post" enctype="multipart/form-data">'
        h = h + '<font color="red">' + '<h3>' + '产品信息' + '</h3>'  + '</font>'
        html_nid = productret.id
        html_name = productret.name
        html_price = productret.price
        html_discount  = productret.discount
        html_num  = productret.num
        html_description  = productret.description
        html_thumbnail = productret.thumbnail
        html_category = productret.category.name
        h = h + '<h4>' + '<input type="hidden" name="html_nid" value="%s">'%html_nid
        h = h + '<font>' + '产品分类：' + html_category + '</font>' + display_space
        h = h + '<font>' + '产品名称：' + html_name + '</font>' + display_space
        h = h + '<font>' + '产品详情：' + html_description + '</font>' +  '<br>'
        h = h + '<br>' + '产品缩略图：' + '<img src="data:image/jpg;base64,%s"/>'%html_thumbnail + '</h4>' + '<br>' 
        h = h + '<font color="red">' + '<h3>' + '规格信息' + '</h3>'  + '</font>'       
        for i in parameterret:
            nid = i.id
            price = i.price
            discount  = i.discount
            num  = i.num
            description  = i.description
            h = h + '<h4>'
            h = h + '<font>' + '规格选择：' + '<input type="Radio" name="parameter" value="%s">'%nid + display_space
            h = h + '<font>' + '价格：' + str(discount) + '</font>' + display_space
            h = h + '<font>' + '库存：' + str(num) + '</font>' + display_space 
            h = h + '<font>' + '描述：' + description + '</font>' + display_space 
        welcome = u'<fieldset><legend><h2>产品详情</h2></legend>'
        entry_time = '<br>' + u'进入时间:' + display_space +'%s'%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+'</h4>'
        cart_info = '<input type="submit" name="cart" value="加入购物车"/>' + '<br>' + '<br>'
        buy_info = '<input type="submit" name="buy" value="立即购买"/>'
        num_info= '<br>' + '<br>' + '<br>' +'购买数量：' + '<input type="text" name="buynum">' + '<br>'
        index_link = u'<a href="/">点击返回主页</a ><body></html>'+ '<br>'
        product_link = u'<a href="/product_list/none">点击返回产品列表</a ><body></html>' + display_space
        h = welcome + h + num_info + buy_info + display_space + cart_info + product_link  + index_link + entry_time
        return h
    except Exception as e:
        log.error(traceback.format_exc())


# shopping_cart
def cartHtml(cart_info,carriage_info):        
    try:
        h = u'<html><body>'
        h = h + '<form action="/api/v1/transaction_details" method="post" enctype="multipart/form-data">' + '<h4>'
        display_space = '&nbsp'*6
        lis = []
        price = 0
        money_full = int(carriage_info.name)
        carriage = int(carriage_info.value)
        for i in cart_info:
            dic = {}
            html_nid = i.id
            product_id = i.product.id
            html_name = i.product.name
            html_thumbnail = i.product.thumbnail        
            parameter_id = i.product_parameters.id    
            html_discount = i.product_parameters.discount
            html_description  = i.product_parameters.description
            html_num = i.num
            parameter_price = float(html_discount)*int(html_num)
            price = price + parameter_price
            dic['cart_nid'] = html_nid
            dic['product_id'] = product_id
            dic['parameter_id'] = parameter_id
            dic['name'] = html_name
            dic['thumbnail'] = html_thumbnail
            dic['discount'] = html_discount
            dic['description'] = html_description
            dic['num'] = html_num
            dic['parameter_price'] = parameter_price
            lis.append(dic)
            h = h + '<img src="data:image/jpg;base64,%s"/>'%html_thumbnail + display_space
            h = h + '<font>' + '名称：' + html_name + '</font>' + display_space
            h = h + '<font>' + '价格：' + str(html_discount) + '</font>' + display_space
            h = h + '<font>' + '规格描述：' + html_description + '</font>' + display_space
            h = h + '<font>' + '购买数量：' + str(html_num) + '</font>' + display_space
            h = h + '<a href="/shopping_cart_del/' + str(html_nid) + u'">删除</a>' + '<br>'
        if price > money_full:
            carriage = 0
        else:
            carriage = carriage
        total_price = price + carriage
        dic = {}
        dic['carriage'] = carriage
        dic['price'] = price
        dic['total_price'] = total_price
        dic['shoping_cart'] = 0
        lis.append(dic)
        h = h + '<input type="hidden" name="lis" value="%s">'%lis + '</h4>'
        welcome = u'<fieldset><legend><h2>购物车</h2></legend>'
        entry_time = '<br>' + u'进入时间:' + display_space +'%s'%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + '</h4>'
        product_link = '<h4>' + u'<a href="/product_list/none">产品列表</a ><body></html>'
        price_all = '<br>' + '<br>' +'<font color="red">' +'<h3>' + '商品价格：' + str(price) + '</font>' + display_space
        carriage = '<font color="red">'  + '运费：' + str(carriage) + '</font>' + display_space
        total_price = '<font color="red">'  + '总价：' + str(total_price) + '</font>' + display_space
        payment = '<input type="submit" name="buy" value="去结算"/>'+ '</h3>' + '<br>'
        index_link = u'<a href="/">返回主页</a ><body></html>'+ '<br>'
        h = welcome+ h + price_all + carriage + total_price  + payment + product_link + display_space + index_link + entry_time
        return h        
    except Exception as e:
        log.error(traceback.format_exc())



# address
def addressListHrml(address_ret):
    try:
        h = u'<html><body>'
        h = h + '<form action="/api/v1/address_list" method="post" enctype="multipart/form-data">'
        for i in address_ret:
            html_nid = i.id
            html_name = i.name
            html_phone = i.phone
            html_city  = i.city 
            html_address  = i.address
            html_postcode  = i.postcode
            html_defaults= i.defaults
            address = html_city + ' ' +  html_address
            if int(html_defaults) == 0:
                h = h + '<font>' + '设置为默认地址：' + '<input type="Radio" name="defaults" value="%s">'%html_nid + display_space
            h = h + '<font>' + '姓名：' + html_name + '</font>' + display_space
            h = h + '<font>' + '电话：' + html_phone + '</font>' + '<br>'
            h = h + '<font>' + '收货地址：' + address + '</font>' + display_space
            h = h + '<font>' + '邮政编码：' + html_postcode + '</font>' + display_space
            h = h + '<a href="/address_del/' + str(html_nid) + u'">删除</a>' +  '<br>' + '<br>'
        welcome = u'<fieldset><legend><h2>收货地址管理</h2></legend>'
        entry_time = '<br>' + u'进入时间:' + display_space +'%s'%(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        add_link = u'<a href="/address_add">点击添加</a ><body></html>'
        set_up = '<input type="submit" value="设置"/>'
        index_link = u'<a href="/">点击返回主页</a ><body></html>'+ '<br>'
        h = welcome+ h + set_up  + '<br>' + add_link + display_space + index_link + entry_time
        return h
    except Exception as e:
        log.error(traceback.format_exc())
