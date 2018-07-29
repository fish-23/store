#!/usr/bin/python
# -*- coding: UTF-8 -*-
import bottle
import os.path
import base64
import io
import struct
from log import *
from PIL import Image
# python3 -m pip install Pillow

app = application = bottle.Bottle()


@app.route('/')
def store():

        #x = request.environ.get('X-Real-IP')
	todo_html = read_file("tmpl/todo.html")
	return todo_html

@app.route('/api/v1/product_add', method='POST')
def store():
        log.info('11111111111')
        print('222222222222')
        # 接收图片文件
        pic = request.files.get('pic')
        # 用os.path.splitext方法把文件名和后缀分离
        name, ext = os.path.splitext(pic.filename)
        # 修改文件名
        pic.filename = ''.join(('123',ext))
        # 保存图片
        pic.save('/root',overwrite=True)
        # 接收前端传来的所有文件，并编码成utf-8
        postValue = bottle.request.POST.decode('utf-8')
        # 取出图片文件(<class 'bottle.FileUpload'>)
        pic = bottle.request.POST.get('pic')
        # 读取文件(bytes 类型)
        pic = pic.file.read()
        # =用在URL、Cookie里面会造成歧义，很多Base64编码后会把=去掉，此时加上=
        pic = base64.b64decode(str(pic) + '='*(4-len(pic)%4))
        # 保存文件
        file=open('/root/789.jpg','wb')
        file.write(pic)
        file.close()

@app.route('/show')
def show():
        return(store_show)     
 
class StripPathMiddleware(object):

    def __init__(self, a):
        self.a = a
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.a(e, h)

if __name__ == '__main__':
    bottle.run( host='127.0.0.1', port='10070',
                app=StripPathMiddleware(app),
                reloader=True, debug=True
              )
