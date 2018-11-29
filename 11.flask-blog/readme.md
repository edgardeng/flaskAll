# Flask Blog

> Flask Web Program


## Auth

### 使用Flask-Login认证用户

在虚拟环境中安装这个扩展: `(venv) $ pip install flask-login`

User 模型必须实现的用户方法
* is_authenticated()  如果用户已经登录，必须返回 True，否则返回 False
* is_active()         如果允许用户登录，必须返回 True，否则返回 False, 如果要禁用账户，可以返回 False
* is_anonymous()      对普通用户必须返回 False
* get_id()            返回用户的唯一标识符，使用 Unicode 编码字符串

UserMixin类，包含这些方法的默认实现，且能满足大多数需求。
修 改后的 User 模型如示例 8-6 所示。
示例 app/models.py中的 User 模型，支持用户登录 
```python
from flask.ext.login import UserMixin
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
```

Flask-Login 在程序的工厂函数中初始化，app/__init__.py:
```python
from flask.ext.login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    # ...
    login_manager.init_app(app)
```

LoginManager 对象的 session_protection 属性可以设为 None、'basic' 或 'strong' 的不同的安全等级
'strong' 时，Flask-Login 会记录客户端 IP 地址和浏览器的用户代理信息，如果发现异动就登出用户。

最后，Flask-Login要求程序实现一个回调函数，使用指定的标识符加载用户。

在app/models.py:加载用户的回调函数 
```python
from . import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

加载用户的回调函数接收以 Unicode 字符串形式表示的用户标识符。如果能找到用户，这 个函数必须返回用户对象;否则应该返回 None。


#### 保护路由
保护路由只让认证用户访问使用 login_required 修饰器。
```python`
from flask.ext.login import login_required

@app.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'
``

#### 添加登录表单
app/auth/forms.py:登录表单
```python
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email
class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in') submit = SubmitField('Log In')

```
登录页面的模板保存在 auth/login.html 文件中。

Base.html中的导航条使用 Jinja2 条件语句，登录状态分别显示 “Sign In”或“Sign Out”链接。
```html
<ul class="nav navbar-nav navbar-right">
{% if current_user.is_authenticated() %}
<li><a href="{{ url_for('auth.logout') }}">Sign Out</a></li> {% else %}
<li><a href="{{ url_for('auth.login') }}">Sign In</a></li> {% endif %}
</ul>
```
变量 current_user 由 Flask-Login 定义，且在视图函数和模板中自动可用。 is_authenticated() 方法可用来判断当前用户是否已经登录。

#### 登入用户
视图函数 login() 
```python
from flask import render_template, redirect, request, url_for, flash 
from flask.ext.login import login_user
from . import auth
from ..models import User
from .forms import LoginForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index')) 
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)
```

登录模板以渲染表单
```html
{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}

{% block page_content %} 
<h1>Login</h1>
<div class="col-md-4">
     {{ wtf.quick_form(form) }}
</div>
{% endblock %}
```

#### 登出用户 
app/auth/views.py:
```python
from flask.ext.login import logout_user, login_required

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.') 
return redirect(url_for('main.index'))

```

## extension

* [flask-bootstrap](https://travis-ci.org/mbr/flask-bootstrap) packages [Bootstrap](http://getbootstrap.com)

* [flask-script](https://flask-script.readthedocs.io/en/latest/) support for writing external scripts

* [Flask-SQLAlchemy]() Adds SQLAlchemy support

* [Flask-Login]()
