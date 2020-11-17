from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


class MiddleWare(object):
    def __init__(self, w_app):
        self.old_wsgi_app = w_app

    def __call__(self, environ, start_response):
        print('before call')
        obj = self.old_wsgi_app(environ, start_response)
        print('after call')
        return obj


if __name__ == '__main__':
    app.wsgi_app = MiddleWare(app.wsgi_app)
    app.run()  # 执行 werkzeug 的run_simple
    """
    请求到来后
    1 执行 app.__call__
    2 调用app.wsgi_app 方法
    """
