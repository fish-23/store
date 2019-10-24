### 1，Python3 安装软件
      解答：python3 -m pip install sqlalchemy
### 2，Python3 通过 mysql-connector 连接数据库报错 No module named 'mysql'
      解答：python3 -m pip  install mysql-connector==2.1.4
### 3，TabError: inconsistent use of tabs and spaces in indentation
      解答：假设一个tab为8个空格，现在有两行代码，一行缩进用8个空格，一行缩进用tab，看起来缩进一致，但是会报错
### 4，Image.open(） 报错   AttributeError: 'FileUpload' object has no attribute 'read'
      解答：看open方法解释：You can use either a string (representing the filename) or a file object as the file argument. 
            In the latter case, the file object must implement read, seek, and tell methods, and be opened in binary mode.
            [官网地址](http://effbot.org/imagingbook/image.htm#image-open-function)
            bottle接收的图片(pic) 类型(<class 'bottle.FileUpload'>)  处理成file object  pic.file 然后调用open函数，成功
            <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=198x190 at 0x7F33B26313C8>
### 5，修改 .html文件后，用浏览器调用接口没变化
      解答：浏览器清除 自动填写的表单数据，重新调用，成功
### 6，用Image处理后生成的缩略图，如何保存到数据库
      解答：先将图片转化成二进制流，然后用base64进行编码后，就可以存入数据库
            [参考文档](https://www.jianshu.com/p/2ff8e6f98257)
### 7，将bytes64编码的图片，用html展示
      解答：'<img src="data:image/jpg;base64,%s"/>'%html_thumbnail
### 8，request.environ,get('X-Real-IP') 获取不到用户的ip地址
      解答：浏览器在请求服务器的时候，在HTTP头上会携带用户ip，现在没有获取到ip，证明在打印之前的某一步出错，没有获取到用户ip。
            先用 nc -l 命令监听项目中途经过的端口(443端口被nginx监听，需要杀死nginx用nc监听)，看是否有错误，测试证明，所有端口都没有错误
            那问题就是bottl接收数据时出错，去官网看bottle如何接收数据 [官网地址](http://www.bottlepy.org/docs/dev/index.html)
            上面的代码是获取uwsgi的环境变量，获取http头的话，用request.headers.get('X-Real-IP')
### 9，python 获取图片文件的大小
      解答：方法一：获取具体路径下文件的大小 os.path.getsize('./static/products/apple_pic.png')
            方法二：获取file对象的大小  pic = request.files.get('pic')   pic = pic.file   pic.seek(0,2)   size = pic.tell()
### 10，python 辨别图片真假
      解答：方法一：imghdr模块，读取固定路径图片  pic = imghdr.what('./static/apple_pic.png')  print(pic)  # png
            方法二：第三方库pillow，读取固定路径图片 bValid = True  try:mage.open('./static/potato_pic.jpg').verify()
                  except:bValid = False  print(bValid)  # True
            方法三：第三方库pillow，读取file对象 pic = pic.file  bValid = True  try:Image.open(pic).verify() 
                  except:bValid = False  print(bValid)  # True
### 11，peewee.InternalError: (1054, "Unknown column 't2.id' in 'where clause'")
      解答：在查询语句中去掉外键关联的id
### 12，peewee中店铺表和用户表用外键关联，什么时候用.id 什么时候不用
      解答：（1）通过店铺id查用户信息时，不用.id  user_info = Users.select().where(Users.groups == groups_id) 这对应的是店铺表id这一列
             (2) 通过用户信息，获取店铺id时，要用.id  user_info = Users.get(Users.name == login_name)
                (1) group_id = user_info.groups  这样获取的结果，打印出来是1，类型是<Model: Users> 它代表的是店铺表id=1对应的信息
                (2) group_id = user_info.groups.id 这样获取的结果，打印出来是1，类型是<int> 他表示的是店铺表这条信息对应的id
### 13，varchar类型选择
      解答：设置字段类型为varchar类型时，向这个字段存数据，最多只能存储50个英文字符
### 14，两个表什么时候用外键关联，什么时候用字段存id进行联系
      解答：这个要看两个表的关系。如果主表变化，从表也需要变化，用外键。如果从表不需要变化，用字段
            例如，产品和产品规格两个表，当产品删除时，产品规格也应被删除，这两个表用外键，删除设置成主表删除从表删除
            例如，订单和收货信息两张表，收获信息被删除，已完成的订单不受影响，这时候，就应该在订单表中用字段存收货信息的id
### 15，在支付信息永久保存的情况下，如何设计支付详情表
      解答：通过设置外键关联，没法保证支付信息的完整性(例如真正意义上的删除产品)。通过设置字段来存储信息，太过冗余，而且后续操作很受限制
            参考淘宝京东的商品下柜，当产品需要删除时，通过一个字段改变状态，而不是真正意义上的删除
### 16，字符串和字典的转化
      解答：str = '{'price': 70.0, 'lis': [{'cart_nid': 1, 'product_id': 1}, {'cart_nid': 2, 'product_id': 2]}'
            str = str.replace("'","\")
            dic = json.loads(str)
### 17，MySQL删除数据库时无响应
      解答：执行show full processlist观察state和info两列，查看有哪些线程在运行。经过查询发现之前远程删除的时候由于网络中断，锁表了。
            所以导致再次登录的时候删除操作无响应。这时候只要使用kill命令+对应线程前面id，将线程结束掉，就可以正常删除了。
            [参考文档](https://blog.csdn.net/cccheer/article/details/60480199)
### 18，检测字符串中是否有汉字
      解答：Python isalnum() 方法    检测汉字返回的是True  用此方法无法检测
            import re
            re_check = re.compile(u'[\u4e00-\u9fa5]+')
            check_ret = re_check.search(name)
            if check_ret:
                return '有汉字'
### 19，后台运行程序
      解答：nohup python3 store.py &
