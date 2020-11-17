"""
Session 流程
1. 请求到达后
    ctx = RequestContext(...)
           - request
           - session = None
    ctx.push() 调用了 ctx.session = SecureCookieSessionInterface.open_session
2. 执行视图函数
3. 请求结束后
    SecureCookieSessionInterface.save_session [将 session存入cookie]

"""
from flask import Flask, sessions, request
app = Flask(__name__)

@app.route('/')
def index():
    # 从ctx获取session （一个特殊的字典）

    sessions['index'] = 'abc'
    return '<h1>Hello World!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
