# Flask的数据库使用

## Flask-MongoEngine

> MongoDB 是一个文档型数据库，是 NoSQL (not only SQL) 的一种，具有灵活、易扩展等诸多优点。
  MongoEngine 是一个用来操作 MongoDB 的 ORM 框架. 如果你不知道什么是 ORM，可以参考 Flask-SQLAlchemy。
  
安装
```
    $ pip install flask-mongoengine
```

配置, 在使用之前，请确保 mongo 服务已经开启。
```python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'test',
    'host': '127.0.0.1',
    'port': 27017
}

db = MongoEngine(app)
```
在 app.config 的 MONGODB_SETTINGS 字典中配置了数据库、主机和端口。
如果数据库需要身份验证，那我们需要在该字典中添加 username 和 password 参数.

在应用初始化前配置数据库，比如使用工厂方法，可以类似这样做：
```
from flask import Flask
from flask_mongoengine import MongoEngine
db = MongoEngine()

...

app = Flask(__name__)
app.config.from_pyfile('config.json')
db.init_app(app)
```

## Flask-MongoEngine的使用

### 定义数据模型
```
from datetime import datetime

class Todo(db.Document):
    meta = {
        'collection': 'todo',
        'ordering': ['-create_at'],
        'strict': False,
    }

    task = db.StringField()
    create_at = db.DateTimeField(default=datetime.now)
    is_completed = db.BooleanField(default=False)
    
```

### 数据的操作

#### 查询数据

查询所有数据使用 all() 方法
todos = Todo.objects().all()
查询满足某些条件的数据
task = 'cooking'
todo = Todo.objects(task=task).first()
其中，first() 方法会取出满足条件的第 1 条记录。
添加数据
添加数据使用 save() 方法
todo1 = Todo(task='task 1', is_completed=False)
todo1.save()
数据排序
排序使用 order_by() 方法
todos = Todo.objects().order_by('create_at')
更新数据
更新数据需要先查找数据，然后再更新
task = 'task 1'
todo = Todo.objects(task=task).first()  # 先查找
if not todo:
    return "the task doesn't exist!"

todo.update(is_completed=True)   # 再更新
删除数据
删除数据使用 delete() 方法：先查找，再删除
task = 'task 6'
todo = Todo.objects(task=task).first()  # 先查找
if not todo:
    return "the task doesn't exist!"

todo.delete()   # 再删除
分页
分页可结合使用 skip() 和 limit() 方法
skip_nums = 1
limit = 3

todos = Todo.objects().order_by(
    '-create_at'
).skip(
    skip_nums
).limit(
    limit
)
使用 paginate() 方法
def view_todos(page=1):
    todos = Todo.objects.paginate(page=page, per_page=10)