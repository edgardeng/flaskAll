# Flask的数据库使用

## PyMongo
> Python 要连接 MongoDB 的 驱动

1. 安装 `pip3 install pymongo`
2. 基本使用
```python
import pymongo
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
 
dblist = myclient.list_database_names()
# dblist = myclient.database_names() 
if "runoobdb" in dblist:
  print("数据库已存在！")
```


## Flask-MongoEngine

> MongoDB 是一个文档型数据库，是 NoSQL (not only SQL) 的一种，具有灵活、易扩展等诸多优点。
  MongoEngine 是一个用来操作 MongoDB 的 ORM 框架. 如果你不知道什么是 ORM，可以参考 Flask-SQLAlchemy。
  
1. 安装 ` pip install flask-mongoengine`

2. 配置, 在使用之前，请确保 mongo 服务已经开启。
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

> 在 app.config 的 MONGODB_SETTINGS 字典中配置了数据库、主机和端口。如果数据库需要身份验证，那我们需要在该字典中添加 username 和 password 参数.

3. [更多信息](https://flask-mongoengine.readthedocs.io/en/latest/)

### Flask-MongoEngine的使用

#### 定义数据模型
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

```python
import Todo
todos = Todo.objects().all() # 查询所有数据使用 all() 方法
todo = Todo.objects(task='task').first() # 查询满足某些条件的数据
todo1 = Todo(task='task 1', is_completed=False)
todo1.save() # 添加数据
todos = Todo.objects().order_by('create_at') # 数据排序

todo = Todo.objects(task='task').first()  # 先查找
todo.update(is_completed=True)   # 再更新
todo.delete()   # 再删除
# 分页
todos = Todo.objects().order_by( '-create_at').skip(skip_nums).limit(limit)
# 使用 paginate() 方法
todos = Todo.objects.paginate(page=1, per_page=10)
```

A表插入数据：

var a={value:"1"}

var b={value:"2"}    
var c={value:"9"}    
var d={value:"10"}  

db.A.save(a)
db.A.save(b)         
db.A.save(c)    
db.A.save(d) 
db.A.save(b)
db.A.save(c)
db.A.save(d)

db.A.find() { "_id" : ObjectId("565eb6d14eae52027fb3e313"), "value" : "1" } { "_id" : ObjectId("565eb6d24eae52027fb3e314"), "value" : "2" } { "_id" : ObjectId("565eb6d24eae52027fb3e315"), "value" : "9" } { "_id" : ObjectId("565eb6d24eae52027fb3e316"), "value" : "10" } 
B表插入数据： 
> var Ba={Apid:[new DBRef('A',ObjectId("565eb6d24eae52027fb3e314"))],value:3}                         
> db.B.save(Ba)   
var Ba={Apid:[new DBRef('A',ObjectId("565eb6d24eae52027fb3e314"))],value:4}   
db.B.insert(Ba)                                                               
var Ba={Apid:[new DBRef('A',ObjectId("565eb6d24eae52027fb3e314"))],value:7}   
db.B.insert(Ba)                                                               
var Ba={Apid:[new DBRef('A',ObjectId("565eb6d24eae52027fb3e314"))],value:8}   
db.B.insert(Ba) WriteResult({ "nInserted" : 1 }) 
> var Ba={Apid:[new DBRef('A',ObjectId("565eb6d24eae52027fb3e314"))],value:4}   
> db.B.insert(Ba)                                                               
WriteResult({ "nInserted" : 1 }) > var Ba={Apid:[new DBRef('A',ObjectId("565eb6d24eae52027fb3e314"))],value:7}   
> db.B.insert(Ba)                                                               
WriteResult({ "nInserted" : 1 }) 
> var Ba={Apid:[new DBRef('A',ObjectId("565eb6d24eae52027fb3e314"))],value:8}   
> db.B.insert(Ba)  WriteResult({ "nInserted" : 1 }) 
> db.B.find(); { "_id" : ObjectId("565eb7514eae52027fb3e317"), "Apid" : [ DBRef("A", ObjectId("565eb6d24eae52027fb3e314")) ], "value" : 3 } { "_id" : ObjectId("565eb7514eae52027fb3e318"), "Apid" : [ DBRef("A", ObjectId("565eb6d24eae52027fb3e314")) ], "value" : 4 } { "_id" : ObjectId("565eb7514eae52027fb3e319"), "Apid" : [ DBRef("A", ObjectId("565eb6d24eae52027fb3e314")) ], "value" : 7 } { "_id" : ObjectId("565eb7524eae52027fb3e31a"), "Apid" : [ DBRef("A", ObjectId("565eb6d24eae52027fb3e314")) ], "value" : 8 } C表数据： 
> var Ca={Bpid:[new DBRef('B',ObjectId("565eb7514eae52027fb3e318"))],value:5}                         
> db.C.save(Ca)                                                                 var Ca={Bpid:[new DBRef('B',ObjectId("565eb7514eae52027fb3e318"))],value:6}   db.C.save(Ca) WriteResult({ "nInserted" : 1 }) 
> var Ca={Bpid:[new DBRef('B',ObjectId("565eb7514eae52027fb3e318"))],value:6}   > db.C.save(Ca)  WriteResult({ "nInserted" : 1 }) 
> db.C.find() { "_id" : ObjectId("565eb7a04eae52027fb3e31b"), "Bpid" : [ DBRef("B", ObjectId("565eb7514eae52027fb3e318")) ], "value" : 5 } { "_id" : ObjectId("565eb7a14eae52027fb3e31c"), "Bpid" : [ DBRef("B", ObjectId("565eb7514eae52027fb3e318")) ], "value" : 6 } 关联查询： 
> var a = db.B.findOne({"value":4}) 
> a.Apid.forEach(function(ref){printjson(db[ref.$ref].findOne({"_id":ref.$id}));}) { "_id" : ObjectId("565eb6d24eae52027fb3e314"), "value" : "2" } 
> db.A.findOne({"_id":db.B.findOne().Apid[0].$id}) { "_id" : ObjectId("565eb6d24eae52027fb3e314"), "value" : "2" } 

