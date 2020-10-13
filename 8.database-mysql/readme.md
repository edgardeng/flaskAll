# Flask的数据库使用

## 数据库

###  SQL数据库 

关系型数据库把数据存储在表中，表模拟程序中不同的实体。

表中的行定义各列对应的真实数据。表中有个特殊的列，称为主键，其值为表中各行的唯一标识符。表中还可以有称为外键的列，引用同一个表或不同表中某行的主键。
行之间的这种联系称为关系，这是关系型数据库模型的基础。

关系型数据库存储数据很高效，而且避免了重复。将这个数据库中的用户角色重命名也很简单，因为角色名只出现在一个地方。一旦在 roles 表中修改完角色名，所有通过 role_id 引用这个角色的用户都能立即看到更新。
但从另一方面来看，把数据分别存放在多个表中还是很复杂的。
生成一个包含角色的用户列表会遇到一个小问题，因为在此之前要分别从两个表中读取用户和用户角色，再将其联 结起来。关系型数据库引擎为联结操作提供了必要的支持。

### NoSQL数据库

所有不遵循上节所述的关系模型的数据库统称为 NoSQL 数据库。
NoSQL 数据库一般使用 集合代替表，使用文档代替记录。NoSQL 数据库采用的设计方式使联结变得困难，所以大多数数据库根本不支持这种操作。

这种结构的数据库要把角色名存储在每个用户中。如此一来，将角色重命名的操作就变得 很耗时，可能需要更新大量文档。
使用 NoSQL 数据库当然也有好处。数据重复可以提升查询速度。列出用户及其角色的操 作很简单，因为无需联结。

### 使用SQL还是NoSQL
SQL 数据库擅于用高效且紧凑的形式存储结构化数据，需要花费大量精力保证数据的一致性。
NoSQL 数据库放宽了对这种一致性的要求，从而获得性能上的优势。
对中小型程序来说，SQL 和 NoSQL数据库都是很好的选择，而且性能相当。


## Flask-SQLAlchemy

> [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/) 是一个Flask 扩展. SQLAlchemy 是一个很强大的关系型数据库框架。[相关文档](http://www.pythondoc.com/flask-sqlalchemy)

__pip 安装:__
```
(venv) $ pip install flask-sqlalchemy
```

FLask-SQLAlchemy数据库URL
 
* MySQL             mysql://username:password@hostname/database
* Postgres          postgresql://username:password@hostname/database
* SQLite(Unix)      sqlite:////absolute/path/to/database
* SQLite(Windows)   sqlite:///c:/absolute/path/to/database

### SQLAlchemy 的 常见参数
选择项	说明
autoincrement	True 是否自增
primary_key	True 是否是主键
indexE	TRUE 是否是索引
unique	True 是否是唯一
nullable	True 是否允许字段为空
default	默认值
### SQLAlchemy的 字段类型
类型名称	python类型	描述
Integer	int	常规整型，通常为32位
SmallInteger	int	短整型，通常为16位
BigInteger	int或long	精度不受限整型
Float	float	浮点型
Numeric	decimal	定点数
String	str	可变长度字符串
Text	str	可变长度字符串，适合大量文本
Unicode	unicode	可变长度Unicode字符串
Boolean	bool	布尔值
Date	datetime.date	日期类型
Time	datetime.time	时间类型
DateTime	datetime.datetime	日期时间类型
Interval	datetime.timedate	时间间隔
Enum	str	字符列表
PickleType	任意Python对象	自动Pickle序列化
LargeBinary	str	二进制

 
### 配置Flask-SQLAlchemy

> python3中已经不再支持MySQLdb模块，需要安装pymysql:  pip install pymysql

初始化及配置一个简单的 SQLite 数据库
```python
from flask.ext.sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__) app.config['SQLALCHEMY_DATABASE_URI'] =\
'sqlite:///' + os.path.join(basedir, 'data.sqlite') app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
```

初始化及配置一个简单的 Mysql 数据库
```python
from flask_sqlalchemy import SQLAlchemy
import pymysql

#创建flask对象
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://username:password@hostname/database?charset=utf8"

#配置flask配置对象中键：SQLALCHEMY_COMMIT_TEARDOWN,设置为True,应用会自动在每次请求结束后提交数据库中变动
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app) #获取SQLAlchemy实例对象
```

### 定义数据模型
> 模型这表示程序使用的持久化实体。在 ORM 中，模型一般是一个 Python 类，类中的属性对应数据库表中的列。

```python
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    def __repr__(self):
        return '<User %r>' % self.username
```

### mysql 的数据操作

#### 1.创建表
```
db.create_all()
```
#### 2.查询记录,注意查询返回对象，如果查询不到返回None
```
User.query.all() #查询所有
User.query.filter_by(username='admin').first()#条件查询
User.query.order_by(User.username).all()#排序查询
User.query.limit(1).all()#查询1条
User.query.get(id = 123)#精确查询
```

##### 2.1 分页查询

> sqlalchemy中使用query查询，而flask-sqlalchemy中使用basequery查询。所有分页查询不可以再跟first(),all()等
```python

# 1.用offset()设置索引偏移量,limit()限制取出量

db.session.query(User.name).filter(User.email.like('%'+email+'%')).limit(page_size).offset((page_index-1)*page_size)
#filter语句后面可以跟order_by语句

# 2.用slice(偏移量，取出量)函数

db.session.query(User.name).filter(User.email.like('%'+email+'%')).slice((page_index - 1) * page_size, page_index * page_size)
#filter语句后面可以跟order_by语句


# 3.用paginate(偏移量，取出量)函数,用于BaseQuery

user_obj=User.query.filter(User.email.like('%'+email+'%')).paginate(int(page_index), int(page_size),False)
#遍历时要加上items  object_list =user_obj.items

# 4.filter中使用limit

db.session.query(User.name).filter(User.email.like('%'+email+'%') and limit (page_index - 1) * page_size, page_size)
#此处不能再跟order_by语句，否则报错
```

####  3.增加记录
```
admin = User(username='admin', email='admin@example.com')
guest = User(username='guest', email='guest@example.com')
db.session.add(admin)
db.session.add(guest)
db.session.commit()
```

####  4.删除
```
user = User.query.get(id = 123)
db.session.delete(user)
db.session.commit()
```

#### 5. 修改

```python
Users.query.filter_by(id=1).update({'name': name, 'email': email})

```

## Problem

### sqlalchemy的model无法Json格式化

1. 在model中添加序列化函数
```python
class Users(db.Model):

    __tablename__ = 't_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @staticmethod
    def as_dict_list(l):
        return [m.as_dict() for m in l]

    def __repr__(self):
        return '<User %r>' % self.name
        
```
2. 在返回时，执行序列化函数

```python
    all_users = Users.query.all()
    return jsonify({'users': Users.as_dict_list(all_users)})
    
    user = Users.query.filter_by(id=user_id).first()  # 条件查询
    return jsonify({'user': user.as_dict()})
```


