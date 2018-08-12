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
      解答：<img src="data:image/jpg;base64,%s"/>'%html_thumbnail
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
