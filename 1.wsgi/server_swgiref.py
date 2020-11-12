"""
use wsgiref to build a wsgi server
desc: WSGI服务器实现
"""

from wsgiref.simple_server import make_server


def hello(environ, start_response):
    """ 创建一个符合WSGI标准的一个HTTP处理函数, TA接收两个参数：
       environ：一个包含所有HTTP请求信息的dict对象；
       start_response：一个发送HTTP响应的函数。
    """

    status = "200 OK"
    response_headers = [('Content-Type', 'text/html')]
    start_response(status, response_headers)
    print('*'*30, environ)
    # 通过environ可以获取http请求的所有信息，
    path = environ['PATH_INFO'][1:] or 'hello'
    # http响应的数据都可以通过start_response, 加上函数的返回值作为body
    return [b'<h1> %s </h1>' % path.encode()]


if __name__ == '__main__':
    server = make_server('localhost', 8001, hello)
    print('Serving HTTP on port 8001...')
    server.serve_forever()
