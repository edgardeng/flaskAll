# FlaskAll - 1. Hello World

## Index代码(index.py)

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
```
运行: python index.py 。在浏览器访问http://127.0.0.1:5000/ 即可

## Flask Web 运行流程


(1) 执行 python index.py，逐行运行 index.py中的代码。

(2) app = Flask(__name__) 实例化一个Flask 对象，__name__为当前模块名。

(3) @app.route("/") 使用了装饰器，和add_url_rule性质一样。功能是添加endpoint（ ‘/’）和view_func（’index’）的映射关系到view_functions字典中。

(4) if __name__ == '__main__': 保证当前模块是被直接运行，而不是被其他模块导入，然后在运行之后的代码。

(5) app.run(debug=True) 在本地服务器上运行flask 应用，同时传递了debug=True参数。

(6) run(self, host=None, port=None, debug=None, **options)，self就是实例化了的 app，运行run()之后，会设置host = '127.0.0.1', port = 5000。

(7) run()方法中 run_simple(host, port, self, **options) 运行之后会创建一个本地服务器。

(8) 设置默认的_got_first_request = False，表明服务器还没有收到客户端的请求。

(9) run_simple()100多行，那些提示消息（*Running on http://127.0.0.1:5000/ (Press CTRL+C to quit) 等）也是在run_simple()中设置的。重要的是这么一句srv = make_server(...)，在这儿创建了本地服务器。

(10) 根据前面传递的参数，make_server(...)返回了一个单进程单线程的WSGI server，即BaseWSGIServer。BaseWSGIServer继承了HTTPServer；HTTPServer继承了TCPServer；TCPServer继承了BaseServer。不考虑细节，就是创建了本地服务器，同时，本地服务器已经记录了flaskapp信息。

(11) WSGI server的功能：监听指定的端口，收到 HTTP 请求的时候解析为 WSGI 格式，然后调用 app 去执行处理的逻辑。

再看从客户端输入网址，到看到网页响应的过程：

(1) 客户端发送请求到 WSGI server，WSGI server使用__call__ 方法来调用 app处理请求，__call__方法返回了wsgi_app(environ, start_response)，即使用wsgi_app(self, environ, start_response) 处理请求并将处理结果返回到服务器，再返回到客户端。

(2) 从BaseWSGIServer中的定义开始看：
BaseWSGIServer中有行代码是handler = WSGIRequestHandler，即收到客户端的请求后，本地的 WSGI server使用WSGIRequestHandler来处理请求。

(3) WSGIRequestHandler 有个重要的方法是make_environ(self)，返回一个environ字典。可以创建一个供app 运行的环境。

(4) 然后看WSGIRequestHandler 中的 handle_one_request()方法。handle_one_request()中关键的run_wsgi()，看名字，运行wsgi。

(5) WSGIRequestHandler继承自BaseHTTPRequestHandler；BaseHTTPRequestHandler继承自StreamRequestHandler；StreamRequestHandler继承自BaseRequestHandler。

(6) 看wsgi内部的第一个 if语句，如果请求头中'Expect'''中间有'100-continue'，将'HTTP/1.1 100 Continue\r\n\r\n'写入到wfile中。

- headers is an instance of email.message.Message (or a derived class) containing the header information;
- wfile is a file object open for writing.

(7) 不看中间的函数定义，到了最重要的一行execute(self.server.app)，（创建WSGI server时将app作为参数传递并保存在了WSGI server中）这里调用app来处理客户端请求。

(8) WSGI中调用app 会使用到Flask中的__call__方法。

(9) 不看具体处理过程，WSGI server现在完成了接收用户请求，调用flask 应用来处理请求的过程。

然后开始了真正处理一个请求的过程。

(1) 回到Flask类中看__call__方法：
__call__(self, environ, start_response) ，这里的self 是flask应用本身，即实例化的app，environ, start_response 由WSGI server 提供。__call__最后会返回wsgi_app(environ, start_response)，即使用wsgi_app 来处理客户端的请求。

(2) wsgi_app 中：
ctx = self.request_context(environ)首先将environ 封装在了一个请求上下文变量ctx中。请求上下文使用栈结构存储数据，ctx.push() 将environ 压栈放在栈顶。

(3) 关键的一行response = self.full_dispatch_request() 使用 full_dispatch_request() 处理请求，随后返回处理结果：return response(environ, start_response)。

(4)full_dispatch_request() :

Dispatches the request and on top of that performs request pre and postprocessing as well as HTTP exception catching and error handling.
首先是self.try_trigger_before_first_request_functions()
__init__函数中设置了self._got_first_request = False，try_trigger_before_first_request_functions()的最后一行设置了self._got_first_request = True，表明要开始处理请求了。

不分析太多了，full_dispatch_request() 关键是调用dispatch_request() 做真实处理，最后返回finalize_request() 将处理结果变成真正的响应。

(5) dispatch_request()：

Does the request dispatching. Matches the URL and returns the return value of the view or error handler. This does not have to be a response object. In order to convert the return value to aproper response object, call :func: make_response .
① req = _request_ctx_stack.top.request 将请求上下文栈顶的请求赋值给req，(req 会包含请求的详细信息)
②rule = req.url_rule 将req 中的url_rule （’/’）赋值给rule，（请求和flaskapp中代码一致）
③ 在运行@app.route("/") 时将endpoint（ ‘/’）和view_func（’index’）的映射关系到了view_functions字典中。
④如果在flaskapp 代码中找不到输入的 URL，会返回 404 错误。
⑤如果输入的URL在flaskapp 代码有相应的 URL，会返回 flaskapp 对应的视图函数。
⑥上面说的是完整的URL-Viewfunc映射关系，flaskapp 以及 WSGI server 中使用的是endpoint(‘/’, ‘/index’, ‘/about’) -Viewfunc 的映射关系。
⑦总结来说，dispatch_request()判断用户输入的URL在flask应用中有没有相关的定义。如果有，将对应的视图函数的内容返回到full_dispatch_request: rv = self.preprocess_request()。

(6) full_dispatch_request最后会调用finalize_request(rv) 方法将返回结果转换成一个真正的响应。

(7) finalize_request(rv) 代码不复杂，主要就是使用response = self.make_response(rv) 将处理结果变成一个真正的响应（视图函数中字符串变成html形式），最后return response，这个响应会返回到full_dispatch_request，然后返回到wsgi_app。

(8) 以上wsgi_app 完成了一个请求处理的过程，最后return response(environ, start_response) 将处理结果返回给 WSGI server，WSGI server再返回给客户端（浏览器），浏览器中显示了2017-08-21，即flaskapp中index视图函数的返回值。
