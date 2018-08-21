#!/usr/local/python3
# -*- coding: UTF-8 -*-


err_dic = {}

# 用户名密码
err_dic[-1] = '用户尚未登录'
err_dic[-2] = '用户不存在'
err_dic[-3] = '用户名不存在'
err_dic[-4] = '该用户名已存在'
err_dic[-5] = '用户名密码不能为空'
err_dic[-6] = '用户名密码不正确'
err_dic[-7] = '两次密码不一致'
err_dic[-8] = '账号密码格式错误，不能小于6位'
# 手机号，ip，注册
err_dic[-9] = '该手机号已注册'
err_dic[-10] = '手机号格式不正确'
err_dic[-11] = '每个IP每天最多接收5条短信'
err_dic[-12] = '昵称，生日不能为空'
err_dic[-13] = '注册异常，异常的访问方式'
err_dic[-14] = '注册成功'
# 图片，验证码
err_dic[-15] = '图片不能为空'
err_dic[-16] = '图片不能大于1M'
err_dic[-17] = '该文件不是真正的图片'
err_dic[-18] = '图片格式不是常用图片格式'
err_dic[-19] = '验证码错误'
err_dic[-20] = '验证码是六位纯数字'
err_dic[-21] = '验证码超时'
# 商品购买
err_dic[-22] = '购买数量不能为空'
err_dic[-23] = '购买数量只能是纯数字，大于1小于100'
err_dic[-24] = '请选择需要购买的规格'
err_dic[-25] = '购买异常，请联系网站工作人员'
err_dic[-26] = '加入购物车成功'
err_dic[-27] = '只能删除自己的购物车产品'
# 订单
err_dic[-28] = '只能支付自己的订单'
err_dic[-29] = '订单已取消'
err_dic[-30] = '订单支付成功'
err_dic[-31] = '账户余额不足，请联系管理员充值'
# 收货地址
err_dic[-32] = '请添加收货地址'
err_dic[-33] = '请设置默认收货地址'
err_dic[-34] = '填写的数据不能为空'
err_dic[-35] = '选择是否设置为默认地址'
err_dic[-36] = '收货地址添加成功'
# 404，405
err_dic[-37] = '页面不存在'
err_dic[-38] = '访问方式不正确'
