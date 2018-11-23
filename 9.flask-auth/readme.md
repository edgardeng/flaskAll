# Flask-Auth

## Auth2

### OAuth2 Server
> An OAuth2 server concerns how to grant the authorization and how to protect the resource.[Reference](https://flask-oauthlib.readthedocs.io/)



## Auth Restful API

### 用户数据库
使用 Flask-SQLAlchemy 来构建用户数据库模型并且存储到数据库中。 对于每一个用户，username 和 password_hash 将会被存储:

```
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
```
    
> 用户的原始密码将不被存储，密码在注册时被散列后存储到数据库中。\。

#### 密码散列 Hash
> 使用 PassLib 库，一个专门用于密码散列的 Python 包。其中custom_app_context 是一个易于使用的基于 sha256_crypt 的散列算法。

User 用户模型需要增加两个新方法来增加密码散列和密码验证功能:
```python
from passlib.apps import custom_app_context as pwd_context

    class User(db.Model):
        # ...

        def hash_password(self, password):
            self.password_hash = pwd_context.encrypt(password)

        def verify_password(self, password):
            return pwd_context.verify(password, self.password_hash)
```
            
hash_password() 存储明文密码的散列。当一个新用户注册到服务器或者当用户修改密码的时候，这个函数将被调用。

verify_password() 验证明文密码
散列算法是单向函数，能够用于根据密码生成散列，但是无法根据生成的散列逆向猜测出原密码。

### 用户注册

一个客户端可以使用 POST 请求到 /api/users 上注册一个新用户。
请求的主体必须是一个包含 username 和 password 的 JSON 格式的对象。
```python
@app.route('/api/users', methods = ['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
    user = User(username = username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'username': user.username }), 201, {'Location': url_for('get_user', id = user.id, _external = True)}

```

参数 username 和 password 是从请求中携带的 JSON 数据中获取。

响应的主体是一个表示用户的 JSON 对象，201 状态码以及一个指向新创建的用户的 URI 的 HTTP 头信息：Location。

一个用户注册的请求，发送自 curl:
```
$ curl -i -X POST -H "Content-Type: application/json" -d '{"username":"miguel","password":"python"}' http://127.0.0.1:5000/api/users
```
> 注意地是在真实的应用中这里可能会使用安全的的 HTTP (譬如：HTTPS)。如果用户登录的凭证是通过明文在网络传输的话，任何对 API 的保护措施是毫无意义的。

### 基于密码的认证
假设存在一个资源通过一个 API 暴露给那些必须注册的用户。即URL: /api/resource 能够访问到。

使用 HTTP 基本身份认证，让 Flask-HTTPAuth 扩展来为我们做。通过添加 login_required 装饰器:

```python
from flask.ext.httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@app.route('/api/resource')
@auth.login_required
def get_resource():
    return jsonify({ 'data': 'Hello, %s!' % g.user.username })
```

Flask-HTTPAuth 需要给予更多的信息来验证用户的认证，
Flask-HTTPAuth有着许多的选项，取决于应用程序实现的安全级别。

Flask-HTTPAuth 将会在需要验证 username 和 password 对的时候调用这个verify_password 回调函数:
```python
@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True
```

用curl 请求只允许注册用户获取的保护资源:
```python
    $ curl -u miguel:python -i -X GET http://127.0.0.1:5000/api/resource
```


### 基于令牌的认证

每次请求必须发送 username 和 password 不方便，客户端要存储不加密的认证凭证，且在每次请求中发送。

使用令牌来验证请求，客户端应用程序使用认证凭证交换了认证令牌。

令牌是具有有效时间，过了有效时间后，令牌变成无效，需要重新获取新的令牌。

Flask 使用类似的方式处理 cookies 的。这个实现依赖于一个叫做 itsdangerous 的库。

```
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class User(db.Model):
    # ...

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user
```
        
generate_auth_token() 方法生成一个以用户 id 值为值，’id’ 为关键字的字典的加密令牌。令牌中同时加入了一个过期时间，默认为十分钟(600 秒)。


API 需要一个获取令牌的新函数，这样客户端才能申请到令牌:
```
@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })
```
    
注意：这个函数是使用了 auth.login_required 装饰器，也就是说需要提供 username 和 password。

```python
@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
```

curl 请求能够获取一个认证的令牌:
```
$ curl -u miguel:python -i -X GET http://127.0.0.1:5000/api/token
$ curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzg1NjY5MDU1fQ.eyJpZCI6MX0.XbOEFJkhjHJ5uRINh2JA1BPzXjSohKYDRT472wGOvjc:unused -i -X GET http://127.0.0.1:5000/api/resource
```

