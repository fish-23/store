#!/usr/local/python3
# -*- coding: UTF-8 -*-


url = {}
url['/'] = '/'
url['login'] = '/login'
url['register'] = '/register'
url['register_add'] = '/register_add'
url['product_details'] = '/product_details/%s'
url['product_list'] = '/product_list/none'
url['shopping_cart'] = '/shopping_cart'
url['address_add'] = '/address_add'
url['address_list'] = '/address_list'
url['transaction_list'] = '/transaction_list'

url_chinese_msg = {}
url_chinese_msg['/'] = '点击返回主页'
url_chinese_msg['login'] = '点击登录'
url_chinese_msg['register'] = '点击注册'
url_chinese_msg['register_add'] = '点击返回'
url_chinese_msg['product_details'] = '点击返回产品详情'
url_chinese_msg['product_list'] = '点击返回产品列表'
url_chinese_msg['shopping_cart'] = '点击进入购物车'
url_chinese_msg['address_add'] = '点击添加收货地址'
url_chinese_msg['address_list'] = '点击管理收货地址'
url_chinese_msg['transaction_list'] = '点击查看个人订单'

URL = url
URL_MSG = url_chinese_msg
