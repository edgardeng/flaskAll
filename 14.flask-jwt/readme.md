# JWT in Flask Web

## JWT 

> JSON Web Token（JWT）是目前最流行的跨域身份验证解决方案。

### 1.跨域身份验证

Internet服务无法与用户身份验证分开。一般过程如下。

1.用户向服务器发送用户名和密码。

2.验证服务器后，相关数据（如用户角色，登录时间等）将保存在当前会话中。

3.服务器向用户返回session_id，session信息都会写入到用户的Cookie。

4.用户的每个后续请求都将通过在Cookie中取出session_id传给服务器。

5.服务器收到session_id并对比之前保存的数据，确认用户的身份。


### 2. JWT的原则

JWT的原则是在服务器身份验证之后，将生成一个JSON对象并将其发送回用户，如下所示。
```json
{
  "UserName": "test",
  "Role": "Admin",
  "Expire": "2018-08-08 20:15:56"
}
```


之后，当用户与服务器通信时，客户在请求中发回JSON对象。服务器仅依赖于这个JSON对象来标识用户。为了防止用户篡改数据，服务器将在生成对象时添加签名（有关详细信息，请参阅下文）。

服务器不保存任何会话数据，即服务器变为无状态，使其更容易扩展。

### 3. JWT的数据结构

JWT的三个部分: JWT头、有效载荷和签名

JWT头部分是一个描述JWT元数据的JSON对象，通常如下所示。
`{"alg": "HS256","typ": "JWT"}`

在上面的代码中，alg属性表示签名使用的算法，默认为HMAC SHA256（写为HS256）；typ属性表示令牌的类型，JWT令牌统一写为JWT。

有效载荷部分，是JWT的主体内容部分，也是一个JSON对象，包含需要传递的数据。 
JWT指定七个默认字段供选择。

iss：发行人

exp：到期时间

sub：主题

aud：用户

nbf：在此之前不可用

iat：发布时间

jti：JWT ID用于标识该JWT

除以上默认字段外，我们还可以自定义私有字段，如下例：

{

"sub": "1234567890",

"name": "chongchong",

"admin": true

}

请注意，默认情况下JWT是未加密的，任何人都可以解读其内容，因此不要构建隐私信息字段，存放保密信息，以防止信息泄露。

JSON对象也使用Base64 URL算法转换为字符串保存。

3.3签名哈希

签名哈希部分是对上面两部分数据签名，通过指定的算法生成哈希，以确保数据不会被篡改。

首先，需要指定一个密码（secret）。该密码仅仅为保存在服务器中，并且不能向用户公开。然后，使用标头中指定的签名算法（默认情况下为HMAC SHA256）根据以下公式生成签名。

HMACSHA256(base64UrlEncode(header) + "." + base64UrlEncode(payload),

secret)

在计算出签名哈希后，JWT头，有效载荷和签名哈希的三个部分组合成一个字符串，每个部分用"."分隔，就构成整个JWT对象。

3.4 Base64URL算法

如前所述，JWT头和有效载荷序列化的算法都用到了Base64URL。该算法和常见Base64算法类似，稍有差别。

作为令牌的JWT可以放在URL中（例如api.example/?token=xxx）。 Base64中用的三个字符是"+"，"/"和"="，由于在URL中有特殊含义，因此Base64URL中对他们做了替换："="去掉，"+"用"-"替换，"/"用"_"替换，这就是Base64URL算法，很简单把。

### 4. JWT的用法

客户端接收服务器返回的JWT，将其存储在Cookie或localStorage中。客户端将在与服务器交互中都会带JWT。

## Flask-JWT

> Flask-JWT
Add basic JWT features to your Flask application.

1. install

`pip install Flask-JWT`

2. Quickstart

```python

from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'abcxyz'),
    User(2, 'user2', 'abcxyz'),
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

jwt = JWT(app, authenticate, identity)

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity

if __name__ == '__main__':
    app.run()
```

3. 更多API https://flask-jwt.readthedocs.io/en/latest/


## flask-jwt-extended

1. install `pip install flask-jwt-extended`

2. base usage
```pythonfrom flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


# Provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token, and you can return
# it to the caller however you choose.
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


# Protect a view with jwt_required, which requires a valid access token
# in the request to access.
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run()
```
3.[更多API](https://flask-jwt-extended.readthedocs.io/en/latest/)

## PyJWT

> PyJWT是一个用来编码和解码JWT（JSON Web Tokens）的Python库

1. install `pip install pyjwt`

2. base usage
```python
import jwt
encoded_jwt = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')
# 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg'

jwt.decode(encoded_jwt, 'secret', algorithms=['HS256'])
# {'some': 'payload'}
```

3. [more api](https://pyjwt.readthedocs.io/en/latest/)




