# Flask-Restful-API & Form

## Flask的请求-响应循环
Flask 从客户端收到请求时，要让视图函数能访问一些对象，这样才能处理请求。请求对象，封装了客户端发送的 HTTP 请求。
 
为了避免大量可有可无的参数把视图函数弄得一团糟，Flask 使用上下文临时把某些对象变为全局可访问。

```python
from flask import request

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent') 
    return '<p>Your browser is %s</p>' % user_agent
```
在多线程服务器中，多个线程同时处理不同客户端发送的不同请求时， 每个线程看到的 request 对象必然不同。
Falsk 使用上下文让特定的变量在一个线程中全局 可访问，与此同时却不会干扰其他线程。
线程是可单独管理的最小指令集。进程经常使用多个活动线程，有时还会共 享内存或文件句柄等资源。多线程 Web 服务器会创建一个线程池，再从线 程池中选择一个线程用于处理接收到的请求。

__Flask上下文全局变量__

current_app  当前激活程序的程序实例
g           处理请求时用作临时存储的对象。每次请求都会重设这个变量 
request     请求对象，封装了客户端发出的 HTTP 请求中的内容
session     用户会话，用于存储请求之间需要“记住”的值的词典
  
Flask 在分发请求之前激活(或推送)程序和请求上下文，请求处理完成后再将其删除。程 序上下文被推送后，就可以在线程中使用 current_app 和 g 变量。类似地，请求上下文被 推送后，就可以使用 request 和 session 变量。如果使用这些变量时我们没有激活程序上 下文或请求上下文，就会导致错误。如果你不知道为什么这 4 个上下文变量如此有用，先 别担心，后面的章节会详细说明。
下面这个 Python shell 会话演示了程序上下文的使用方法:
```
>>> from hello import app
>>> from flask import current_app >>> current_app.name
    Traceback (most recent call last):
     ...
     RuntimeError: working outside of application context
>>> app_ctx = app.app_context()
>>> app_ctx.push()
>>> current_app.name
     'hello'
>>> app_ctx.pop()
```
在这个例子中，没激活程序上下文之前就调用 current_app.name 会导致错误，但推送完上 下文之后就可以调用了。注意，在程序实例上调用 app.app_context() 可获得一个程序上 下文。

### 请求调度
程序收到客户端发来的请求时，要找到处理该请求的视图函数。为了完成这个任务，Flask 会在程序的 URL 映射中查找请求的 URL。URL 映射是 URL 和视图函数之间的对应关系。 Flask 使用 app.route 修饰器或者非修饰器形式的 app.add_url_rule() 生成映射。

 (venv) $ python
     >>> from hello import app
     >>> app.url_map
     Map([<Rule '/' (HEAD, OPTIONS, GET) -> index>,
<Rule '/static/<filename>' (HEAD, OPTIONS, GET) -> static>, <Rule '/user/<name>' (HEAD, OPTIONS, GET) -> user>])
/ 和 /user/<name> 路由在程序中使用 app.route 修饰器定义。/static/<filename> 路由是 Flask 添加的特殊路由，用于访问静态文件。第 3 章会详细介绍静态文件。
URL 映射中的 HEAD、Options、GET 是请求方法，由路由进行处理。Flask 为每个路由都指 定了请求方法，这样不同的请求方法发送到相同的 URL 上时，会使用不同的视图函数进 行处理。HEAD 和 OPTIONS 方法由 Flask 自动处理，因此可以这么说，在这个程序中，URL 映射中的 3 个路由都使用 GET 方法。

### 请求钩子
在请求开始时，我们可能需要创建数据库连接或者认证发起请求的用户。
为了避免在每个视图函数中都使用重复的代码， Flask 提供了注册通用函数的功能，注册的函数可在请求被分发到视图函数之前或之后 调用。

Flask 支持以下 4 种钩子

* before_first_request:注册一个函数，在处理第一个请求之前运行。
* before_request:注册一个函数，在每次请求之前运行。
* after_request:注册一个函数，如果没有未处理的异常抛出，在每次请求之后运行。
* teardown_request:注册一个函数，即使有未处理的异常抛出，也在每次请求之后运行。

在请求钩子函数和视图函数之间共享数据一般使用上下文全局变量 g。例如，before_ request 处理程序可以从数据库中加载已登录用户，并将其保存到 g.user 中。随后调用视 图函数时，视图函数再使用 g.user 获取用户。

### 响应
Flask 调用视图函数后，会将其返回值作为响应的内容。
HTTP 协议需要的不仅是作为请求响应的字符串。HTTP 响应中一个很重要的部分是状态码，Flask 默认设为 200。 如果视图函数返回的响应需要使用不同的状态码，那么可以把数字代码作为第二个返回值，添加到响应文本之后。

视图函数返回一个 400 状态码，表示请求无效:
```
     @app.route('/')
     def index():
         return '<h1>Bad Request</h1>', 400
```
         
视图函数返回的响应,接受第三个参数，一个由首部(header)组成的字典，可以添加到 HTTP 响应中。一般情况下并不需要这么做。

如果不想返回由 1 个、2 个或 3 个值组成的元组，Flask 视图函数还可以返回 Response 对象。
make_response() 函数可接受 1 个、2 个或 3 个参数(和视图函数的返回值一样)，并返回一个 Response 对象。
有时我们需要在视图函数中进行这种转换，然后在响应对象上调 用各种方法，进一步设置响应。下例创建了一个响应对象，然后设置了 cookie:

```
from flask import make_response
     @app.route('/')
     def index():
         response = make_response('<h1>This document carries a cookie!</h1>')
         response.set_cookie('answer', '42')
         return response
```
         
#### 重定向
重定向，这种特殊响应，没有页面文档，只告诉浏览器一个新地址用 以加载新页面。
重定向响应可以使用 3 个值形式的返回值生成，也可在 Response 对象中设定, Flask还提 供了 redirect() 辅助函数:

```
from flask import redirect
     @app.route('/')
     def index():
return redirect('http://www.example.com')
```

还有一种特殊的响应由 abort 函数生成，用于处理错误。

动态参数 id 对应的用户不存在，就返回状态码 404:

```
from flask import abort
@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello, %s</h1>' % user.name
``` 

注意，abort 不会把控制权交还给调用它的函数，而是抛出异常把控制权交给 Web服务器

## Flask中的路由

> 路由处理URL和函数之间关系的程序。

路由URL的规则：

1.如果路由中的URL规则是有斜杠结尾的，但是用户请求的时候URL结尾没有斜杠，则会自动将用户重定向到带有斜杠的页面。

2.如果路由中的URL规则结尾不带斜杠的，但是用户请求时带了斜杠，那么就会返回404错误响应。

3.还可以为同一个视图函数，定义多个URL规则：

```python
@app.route('/')
def index():
    pass
 
@app.route('/<username>')
def show_user(username):
    pass
 
@app.route('/post/<int:post_id>')
def show_post(post_id):
    pass
  
@app.route('/users/', defaults={'page':1})
@app.route('/users/page/<int:page>', defaults={'page':1})
def show_users(page):
    pass
```

## REST
六条设计规范定义了一个 REST 系统的特点:

* 客户端-服务器: 客户端和服务器之间隔离，服务器提供服务，客户端进行消费。

* 无状态: 从客户端到服务器的每个请求都必须包含理解请求所必需的信息。换句话说， 服务器不会存储客户端上一次请求的信息用来给下一次使用。

* 可缓存: 服务器必须明示客户端请求能否缓存。

* 分层系统: 客户端和服务器之间的通信应该以一种标准的方式，就是中间层代替服务器做出响应的时候，客户端不需要做任何变动。

* 统一的接口: 服务器和客户端的通信方法必须是统一的。

* 按需编码: 服务器可以提供可执行代码或脚本，为客户端在它们的环境中执行。这个约束是唯一一个是可选的。

### 一个 RESTful 的 web service

REST 架构的最初目的是适应万维网的 HTTP 协议。

RESTful web services 概念的核心就是“资源”。 资源可以用 URI 来表示。
客户端使用 HTTP 协议定义的方法来发送请求到这些 URIs

HTTP 标准的方法有如下:
```
==========  =====================  ==================================
HTTP 方法   行为                   示例
==========  =====================  ==================================
GET         获取资源的信息         http://example.com/api/orders
GET         获取某个特定资源的信息 http://example.com/api/orders/123
POST        创建新资源             http://example.com/api/orders
PUT         更新资源               http://example.com/api/orders/123
DELETE      删除资源               http://example.com/api/orders/123
==========  ====================== ==================================
```

本例中的相关代码
```python

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({'users': users})


@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = list(filter(lambda t: t['id'] == user_id, users))
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})


@app.route('/api/user', methods=['POST'])
def add_user():
    # print(request.json)
    if not request.json or not 'name' in request.json:
        abort(400)
    index = users[-1]['id'] + 1 if len(users) > 0 else 1
    user = {
        'id': index,
        'name': request.json['name'],
        'email': request.json.get('email', '')
    }
    users.append(user)
    return jsonify({'user': user}), 200


@app.route('/api/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = list(filter(lambda t: t['id'] == user_id, users))
    print(user)
    print(request.json)
    if len(user) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' not in request.json:
        abort(400)
    if 'email' not in request.json:
        abort(400)
    user[0]['name'] = request.json.get('name', user[0]['name'])
    user[0]['email'] = request.json.get('email', user[0]['email'])
    return jsonify({'user': user[0]})


@app.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = list(filter(lambda t: t['id'] == user_id, users))
    if len(user) == 0:
        abort(404)
    users.remove(user[0])
    return jsonify({'result': True})
    
```

## 更多参考

* [flask-restful](http://www.pythondoc.com/flask-restful/)
