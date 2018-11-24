# Flask Program Structure

## Program Structure 项目结构

Flask 程序的基本结构:
```text
|- program_name
    |- app/
         |- templates/
         |- static/
         |- main/
            |- __init__.py
            |- errors.py
            |- forms.py
            |- views.py
    |- __init__.py
    |- email.py
    |- models.py
    |- migrations/
    |- tests/
        |- __init__.py
        |- test*.py
    |- venv/
    |- requirements.txt 
    |- config.py 
    |- manage.py
```

结构有 4 个顶级文件夹:
* app Flask程序包;
* migrations 文件夹包含数据库迁移脚本;
* tests 单元的测试包;
* venv Python虚拟环境包。

创建了一些新文件:
* requirements.txt 列出了所有依赖包，便于在其他电脑中重新生成相同的虚拟环境;
* config.py 存储配置;
* manage.py 用于启动程序以及其他的程序任务

## 配置选项

程序经常需要设定多个配置。比如开发、测试和生产环境要使用不同的数据库。
> 在开源项目中，建议将忽略config.py，提交config.default。使用项目时，复制成config.py，并修改正确的配置


config.py:程序的配置
```python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string' 
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>' 
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    @staticmethod
    def init_app(app):
        pass
        
class DevelopmentConfig(Config): 
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config): TESTING = True
          SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
              'sqlite:///' + os.path.join(basedir, 'data.sqlite')
config = {
    'development': DevelopmentConfig, 
    'testing': TestingConfig, 
    'production': ProductionConfig,
    'default': DevelopmentConfig }
``` 

基类 Config 中包含通用配置，子类分别定义专用的配置。如果需要，你还可添加其他配 置类。

定义 init_app() 类方法，其参数是程序实例，执行对当前环境的配置初始化。该Config中的 init_app() 方法为空。

在这个配置脚本末尾，config 字典中注册了不同的配置环境，而且还注册了一个默认配置 (本例的开发环境)。

## 程序包

程序包用来保存程序的所有代码、模板和静态文件。

### 使用程序工厂函数
在单个文件中开发程序很方便，但却有个很大的缺点，因为程序在全局作用域中创建，所 以无法动态修改配置。运行脚本时，程序实例已经创建，再修改配置为时已晚。这一点对 

单元测试尤其重要，因为有时为了提高测试覆盖度，必须在不同的配置环境中运行程序。

延迟创建程序实例，把创建过程移到可显式调用的工厂函数中。不仅可以给脚本留出配置程序的时间，还能够创建多个程序实例，这些实例有时在 测试中非常有用。
程序的工厂函数在 app 包的构造文件中定义:

```python
from flask import Flask, render_template 
from flask.ext.bootstrap import Bootstrap 
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy 
from config import config
     bootstrap = Bootstrap()
     mail = Mail()
     moment = Moment()
     db = SQLAlchemy()
     
def create_app(config_name):

    app = Flask(__name__) 
    app.config.from_object(config[config_name]) 
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    # 附加路由和自定义的错误页面 
    return app         
```
``

工厂函数返回创建的程序示例，不过要注意，现在工厂函数创建的程序还不完整，因为没 有路由和自定义的错误页面处理程序。这是下一节要讲的话题。

### 在蓝本中实现程序功能

在单脚本程序中，程序实例存在于全局作用域中，路由可以直接使用 app.route 修饰器定义。
现在程序在运行时创建，只有调用 create_app() 之后才能使用 app.route 修饰器，这时定义路由就太晚了。和路由一样，自定义的错误页面处理程序也面临相同的困难，因为错误页面处理程序使用 app. errorhandler 修饰器定义。

Flask 使用蓝本提供了更好的解决方法。
蓝本和程序类似，也可以定义路由。不同的是，在蓝本中定义的路由处于休眠状态，直到蓝本注册到程序上后，路由才真正成为程序的一部分。
使用位于全局作用域中的蓝本时，定义路由的方法几乎和单脚本程序一样。
和程序一样，蓝本可以在单个文件中定义，也可使用更结构化的方式在包中的多个模块中创建。

为了获得最大的灵活性，程序包中创建了一个子包，用于保存蓝本。
创建蓝本 app/main/__init__.py:

```python
 from flask import Blueprint
     main = Blueprint('main', __name__)
     from . import views, errors
```
     
通过实例化一个 Blueprint 类对象可以创建蓝本。构造函数有两个必须指定的参数: 蓝本的名字和蓝本所在的包或模块。
和程序一样，大多数情况下第二个参数使用 Python 的 __name__ 变量即可。
程序的路由保存在包里的 app/main/views.py 模块中，而错误处理程序保存在 app/main/errors.py 模块中。
导入这两个模块就能把路由和错误处理程序与蓝本关联起来。注意，这些模块在 app/main/__init__.py 脚本的末尾导入，这是为了避免循环导入依赖，因为在 views.py 和 errors.py 中还要导入蓝本main。

蓝本在工厂函数 create_app() 中注册到程序上，app/_init_.py:
```python
def create_app(config_name): 
    # ...
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
```

app/main/errors.py:蓝本中的错误处理程序 
```python
from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
```

在蓝本中编写错误处理程序稍有不同，如果使用errorhandler 修饰器，只有蓝本中的错误才能触发处理程序。要想注册程序全局的错误处理程序，必须使用app_errorhandler。

app/main/views.py:蓝本中定义的程序路由 
```python
from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        # ...
        return redirect(url_for('.index'))
    return render_template('index.html',
                                 form=form, name=session.get('name'),
                                 known=session.get('known', False),
                                 current_time=datetime.utcnow())
```

在蓝本中编写视图函数的不同:
第一，和前面的错误处理程序一样，路由修饰器 由蓝本提供;
第二，url_for() 函数的用法不同。url_for() 函数的第一 个参数是路由的端点名，在程序的路由中，默认为视图函数的名字。

在单脚本程序 中，index()视图函数的URL可使用 url_for('index') 获取。
在蓝本中就不一样了，Flask会为蓝本中的全部端点加上一个命名空间，在不同的蓝本中使用相同的端点名定义视图函数，而不会产生冲突。
命名空间就是蓝本的名字(Blueprint 构造函数的第一个参数)，所以视图函数 index() 注册的端点名是 main.index，其URL使用 url_for('main.index') 获取。

url_for() 的端点简写形式，在蓝本中可以省略蓝本名，如 url_for('. index')。
命名空间是当前请求所在的蓝本。同一蓝本中的重定向可以使用简写形式，但跨蓝本的重定向必须使用带有命名空间的端点名。

## 启动脚本
manage.py: 脚本用于启动程序
```python

#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default') 
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
if __name__ == '__main__':
         manager.run()
         
```
在基于 Unix 的操作系统中可以通过 ./manage.py 执行脚本，而不用使用复杂的 python manage.py。


### 使用Flask-Script支持命令行选项

Flask 的开发 Web 服务器支持很多启动设置选项，但只能在脚本中作为参数传给 app.run()，传递设置选项的理想方式是使用命令行参数。

[Flask-Script](https://github.com/smurfix/flask-script)为 Flask 程序添加了一个命令行解析器，自带常用选项，也支持自定义命令。[更多参考](https://flask-script.readthedocs.io/en/latest/)

Flask-Script 扩展使用 pip 安装:`(venv) $ pip install flask-script`

在index.py中使用 Flask-Script

```python
    from flask.ext.script import Manager 
    manager = Manager(app)
    # ...
    if __name__ == '__main__':
        manager.run()
```
从 flask.ext.script中引入Manager类，初始化主类的实例。
服务器由 manager.run()启动，启动后就能解析命令行了。即可使用一组基本命令行选项。现在运行`$ python index.py`，会显示一个用法消息.

* 显示帮助信息

shell命令用于在程序的上下文中启动 Python shell 会话。可以使用这个会话中运行维护任务或测试，还可调试异常。
运行 `python index.py runserver ` 将以调 试模式启动 Web 服务器
运行 `(venv) $ python index.py runserver --help` 将获取帮助
运行 `(venv) $ python index.py runserver --host 0.0.0.0 ` Web 服务器可使用 http://a.b.c.d:5000/ 网络中的任一台电脑进行访问，其中“a.b.c.d” 是服务器所在计算机的外网 IP 地址。


##  需求文件
程序中必须包含一个 requirements.txt 文件，用于记录所有依赖包及其精确的版本号。
pip可以使用如下命令自动生成这个文件: `(venv) $ pip freeze >requirements.txt` 
```text
     Flask==0.10.1
     Flask-Bootstrap==3.0.3.1
     Flask-Mail==0.9.0
     Flask-Migrate==1.1.0
     Flask-Moment==0.2.0
     Flask-SQLAlchemy==1.0
     Flask-Script==0.6.6
     Flask-WTF==0.9.4
     Jinja2==2.7.1
     Mako==0.9.1
     MarkupSafe==0.18
     SQLAlchemy==0.8.4
     WTForms==1.0.5
     Werkzeug==0.9.4
     alembic==0.6.2
     blinker==1.3
     itsdangerous==0.23  
```

创建这个虚拟环境的完全副本，执行命令:`(venv) $ pip install -r requirements.txt`

##  单元测试 
tests/test_basics.py:单元测试
```python
import unittest
from flask import current_app 
from app import create_app, db

class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    def test_app_exists(self):
    self.assertFalse(current_app is None)
    def test_app_is_testing(self): 
        self.assertTrue(current_app.config['TESTING'])
```

使用Python标准库中的 unittest 包编写。setUp() 和 tearDown() 方法分别在各测试前后运行，并且名字以 test_ 开头的函数都作为测试执行。

如何使用Python的unittest包，阅读[官方文档](https://docs.python.org/2/library/unittest.html)。

manage.py:启动单元测试的命令
```python
@manager.command
def test():
    # ""Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
```
     
manager.command 修饰器让自定义命令变得简单。修饰函数名就是命令名，函数的文档字符 串会显示在帮助消息中。

单元测试的命令运行:`(venv) $ python manage.py test`

## 数据库的创建

重组后的程序和单脚本版本使用不同的数据库。

应首选从环境变量中读取数据库的 URL，同时还提供了一个默认的 SQLite 数据库做备用。

如果使用 Flask-Migrate 跟踪迁移，创建数据表或者升级到最新版本:`(venv) $ python manage.py db upgrade`


### 使用Flask-Migrate实现数据库迁移
 
在开发程序的过程中，有时需要修改数据库模型，还需要更新数据库。

当数据库表不存在时，Flask-SQLAlchemy 才会根据模型，自动进行创建。

数据库迁移框架能跟踪数据库模式的变化，然后增量式的把变化应用到数据库中。
SQLAlchemy 的主力开发人员编写了一个迁移框架[Alembic](https://alembic.readthedocs.org/en/latest/index.html)。 
Flask 程序 还可使用 [Flask-Migrate](http://flask-migrate.readthedocs.org/en/latest/)扩展。Ta对 Alembic 做了轻量级包装，并集成到 Flask-Script 中。

创建迁移仓库,首先安装 Flask-Migrate:`(venv) $ pip install flask-migrate`

1. 在index.py中配置 Flask-Migrate
```python
from flask.ext.migrate import Migrate, MigrateCommand 
    # ...
    migrate = Migrate(app, db)
    manager.add_command('db', MigrateCommand)
```

MigrateCommand类，可附加到 Flask- Script 的 manager 对象上。在这个例子中，MigrateCommand 类使用 db 命令附加。
在维护数据库迁移之前，要使用 init 子命令创建迁移仓库:

```python
    (venv) $ python index.py db init
```
该命令会创建 migrations 文件夹，所有迁移脚本都存放其中。 
数据库迁移仓库中的文件要和程序的其他文件一起纳入版本控制。

2. 创建迁移脚本
在 Alembic 中，数据库迁移用迁移脚本表示。脚本中有两个函数，分别是 upgrade() 和 downgrade()。
upgrade() 函数把迁移中的改动应用到数据库中，downgrade() 函数则将改动 删除。
Alembic 具有添加和删除改动的能力，因此数据库可重设到修改历史的任意一点。
我们可以使用revision 命令手动创建 Alembic 迁移，也可使用 migrate 命令自动创建。 
手动创建的迁移只是一个骨架，upgrade() 和 downgrade() 函数都是空的，开发者要使用Alembic 提供的 Operations 对象指令实现具体操作。
自动创建的迁移会根据模型定义和数 据库当前状态之间的差异生成 upgrade() 和 downgrade() 函数的内容。
自动创建的迁移不一定总是正确的，有可能会漏掉一些细节。自动生成迁移 脚本后一定要进行检查。
migrate 子命令用来自动创建迁移脚本:` (venv) $ python hello.py db migrate -m "initial migration" `

使用 db upgrade 命令把迁移应用到数据库中: `(venv) $ python hello.py db upgrade`

对第一个迁移来说，其作用和调用 db.create_all() 方法一样。但在后续的迁移中， upgrade 命令能把改动应用到数据库中，且不影响其中保存的数据。

如果你从 GitHub 上克隆了这个程序的 Git 仓库，请删除数据库文件 data. sqlite，然后执行 Flask-Migrate 提供的 upgrade 命令，使用这个迁移框架重新 生成数据库。


## 相关参考

* O'Reilly book [Flask Web Development](http://www.flaskbook.com).



