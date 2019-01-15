# Redis

> Redis是一个开源的使用ANSI C语言编写、支持网络、可基于内存亦可持久化的日志型、Key-Value数据库，并提供多种语言的API。

Redis支持存储的value类型相对更多，包括string(字符串)、list(链表)、set(集合)、zset(sorted set --有序集合)和hash（哈希类型）。

这些数据类型都支持push/pop、add/remove及取交集并集和差集及更丰富的操作，而且这些操作都是原子性的。

在此基础上，redis支持各种不同方式的排序。与memcached一样，为了保证效率，数据都是缓存在内存中。

区别的是redis会周期性的把更新的数据写入磁盘或者把修改操作写入追加的记录文件，并且在此基础上实现了master-slave(主从)同步。


## Redis的使用

### Redis命令

Redis 客户端的基本语法: `$ redis-cli`

* 远程登录 `$ redis-cli -h host -p port -a password`

Redis 键命令的基本语法如下： `COMMAND KEY_NAME` 

* 设置健值 `SET key_name redis`
* 获取指定key的值  `GET key_name`
* 删除健值 `DEL key_name`
* 被序列化的值 `DUMP key_name`
* 检查健值存在 `EXISTS key_name`
* 设置过期时间,单位以秒计  `EXPIRE key_name 60`
* UNIX时间戳,设置过期时间 `EXPIREAT key_name 1293840000`
* 设置过期时间,单位以毫秒计 `PEXPIRE key_name 1500`
* 移除key的过期时间，持久保持。 `PERSIST key_name`
* key的剩余的过期时间(毫秒)   `PTTL key_name`
* key的剩余的过期时间(秒)   `TTL key_name`

* 获取所有的key `KEYS *`
* 查找所有符合给定模式的key  `KEYS key_*`
* 服务器的统计信息 `INFO`


### Redis在Python中的使用

1. install `pip install redis`

2. base usage

```python
from redis import Redis
redis = Redis(host='localhost', port=6379, db=0)
redis.set('openCount', 0)
redis.incr('openCount')
redis.get('openCount')

# pipline的使用
pipe = redis.pipeline()
pipe.set('foo', 'bar')
pipe.expireat('foo',111111)
pipe.execute()
```

3. [more api](http://redisdoc.com/)

* keys      所有的key
* dbsize    数据库几条数据
* delete('key')
* save      
* flushdb() 清空数据库
* hset('key','hash_key','hash_value') 添加hash值
* hincrby('key','hash_key', 1) 自增hash值
* hgetall('key') 获取hash值
* hkeys('key') 获取hash值的key

### Flask-Caching的使用

1. install  `pip install flask-caching`

2. base usage

```python
from flask import Flask, render_template
from flask_caching import Cache
app = Flask(__name__)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

@app.route("/")
@cache.cached(timeout=50)
def index():
    
    return render_template('index.html')

@cache.cached(timeout=50, key_prefix='all_comments')
def get_all_comments():
    comments = do_serious_dbio()
    return [x.author for x in comments]

cached_comments = get_all_comments()

```

3. [更多API](https://flask-caching.readthedocs.io/en/latest/)

* clear():清除缓存
* get(key):获取一个键的值，如果值是json格式会自动转化成字典
* set(key,value,timeout):设置一个键值，value可以是字典，会自动转化json格式的字符串
* set_many(key,value,timeout):设置多个键值对
* add(key, value, timeout=None):设置一个键值,如果存在就pass，注意和set的区别
* delete(key)：删除键
* delete_many(k1,k2...):删除多个键值
* get_many(k1,k2...):获取多个键的值
* get_dict(k1,k2...):获取多个键的值,返回一个字典
* has(k):查询是否存在一个键
* inc(self, key, delta=1):将键的值加一
* dec(self, key, delta=1)：将键的值减一
* init_app(app, config=None) : initialize cache with your app object

* memoize(timeout=None, make_name=None, unless=None, forced_update=None) : Use this to cache the result of a function, taking its arguments into account in the cache key.
* delete_memoized(key)
