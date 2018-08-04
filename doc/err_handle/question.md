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
