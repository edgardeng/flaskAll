from flask import Flask, request, session
app = Flask(__name__)
from time import  sleep, ctime
"""
flask 中的上下文
1. 将ctx（requst，session） 放在Local对象上
    - app.py: ctx = self.request_context(environ)
    - ctx.py: _request_ctx_stack.push(ctx)
2. 视图函数的导入： request/session
3. 请求完毕：
    - 获取session
    - 将ctx删除

? flask 有几个LocalStack和Local对象


"""
@app.route('/')
def index():
    print(request.method) # LocalProxy.__getattr__(key='method')
    sleep(2)
    print('end',ctime())

    return '<h1>Hello World!</h1>'

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
