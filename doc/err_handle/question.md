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
           
           
