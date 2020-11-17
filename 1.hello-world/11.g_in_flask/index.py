from flask import Flask

app = Flask(__name__)
"""
AppContext，内部封装：app和g
RequestContext，内部封装：request和session
这两个都是客户的请求到来时创建，请求结束时销毁。。。。。

g：global 

1. g对象是专门用来保存用户的数据的。 
2. g对象在一次请求中的所有的代码的地方，都是可以使用的。(每个请求拥有各自的g,  当前请求内全局可访问，请求完成，清除当前请求g对象。)
3. g 作为 flask 程序全局的一个临时变量,充当者中间媒介的作用,
   通过它传递一些数据，g 保存的是当前请求的全局变量，不同的请求会有不同的全局变量，通过不同的thread id区别

 
2.g对象和session的区别
在我看来，最大的区别是，session对象是可以跨request的，只要session还未失效，不同的request的请求会获取到同一个session，
但是g对象不是，g对象不需要管过期时间，请求一次就g对象就改变了一次，或者重新赋值了一次

"""


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run(debug=True)
