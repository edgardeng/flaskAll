# Celery 
> Celery是一个简单、灵活且可靠的，处理大量消息的分布式系统，专注于实时处理的异步任务队列，同时也支持任务调度。

## Celery的介绍

### Celery的架构
> 由三部分组成，
![](http://static.open-open.com/lib/uploadImg/20150314/20150314100608_187.png)

* 消息中间件（message broker）
> Celery本身不提供消息服务，但是可以方便的和第三方提供的消息中间件集成。包括，RabbitMQ, Redis等等

* 任务执行单元（worker）
> Worker是Celery提供的任务执行的单元，worker并发的运行在分布式的系统节点中。

* 任务执行结果存储（task result store）组成。
> 存储Worker执行的任务的结果
Celery支持以不同方式存储任务的结果，包括AMQP, redis，memcached, mongodb，SQLAlchemy, Django ORM，Apache Cassandra, IronCache 等。

另外， Celery还支持不同的并发和序列化的手段

并发：Prefork, Eventlet, gevent, threads/single threaded

序列化：pickle, json, yaml, msgpack. zlib, bzip2 compression， Cryptographic message signing 等等

###  使用场景

* 异步任务：将耗时操作任务提交给Celery去异步执行，比如发送短信/邮件、消息推送、音视频处理等等

* 定时任务：定时执行某件事情，比如每天数据统计

###  优点

* Simple(简单)
> 使用和维护都非常简单，并且不需要配置文件。

* Highly Available（高可用）
> woker和client会在网络连接丢失或者失败时，自动进行重试。并且有的brokers 也支持“双主”或者“主／从”的方式实现高可用。

* Fast（快速）
> 单个的Celery进程每分钟可以处理百万级的任务，并且只需要毫秒级的往返延迟（使用 RabbitMQ, librabbitmq, 和优化设置时）

* Flexible（灵活）
> Celery几乎每个部分都可以扩展使用，自定义池实现、序列化、压缩方案、日志记录、调度器、消费者、生产者、broker传输等等。

## Celery在python中的使用


1. 创建celery对象和异步任务

```python
import celery
import time
backend='redis://127.0.0.1:6379/1'
broker='redis://127.0.0.1:6379/2'
cel=celery.Celery('test',backend=backend,broker=broker)
@cel.task
def send_email(name):
  print("向%s发送邮件..."%name)
  time.sleep(5)
  print("向%s发送邮件完成"%name)
  return "ok"
```
2. 开启celery `celery worker -A celery_task -l info`

3. 执行任务

```
from celery_task import send_email
result = send_email.delay("yuan")
print(result.id)
```

4. 查看任务执行结果
```
from celery.result import AsyncResult
from celery_task import cel
result_id ='c6ddd5b7-a662-4f0e-93d4-ab69ec2aea5d'
async_result=AsyncResult(id=result_id, app=cel)

if async_result.successful():
  result = async_result.get()
  print(result)
  # result.forget() # 将结果删除
elif async_result.failed():
  print('执行失败')
elif async_result.status == 'PENDING':
  print('任务等待中被执行')
elif async_result.status == 'RETRY':
  print('任务异常后正在重试')
elif async_result.status == 'STARTED':
  print('任务已经开始被执行')
```

### 定时任务

#### 方式一 不重复时间

```python
# 方式一 定时（某个时间）
v1 = datetime(2020, 9, 1, 10, 9, 5) #
v2 = datetime.utcfromtimestamp(v1.timestamp()) # 转成标准时间
result = send_email.apply_async(args=["One Timestamp",], eta=v2)
print(result.id)

# 方式二 定时（当前时间+时间值）
ctime = datetime.now() # 当前时间
utc_ctime = datetime.utcfromtimestamp(ctime.timestamp()) # 默认用utc时间
task_time = utc_ctime + timedelta(seconds=10) # 当前时间 往后推一定的时间
result2 = send_email.apply_async(args=["Current + timedelta"], eta=task_time)
print(result2.id)
```

#### 方式二 间隔时间，重复执行
> 需执行 ` celery beat -A schedule_demo ` +  `celery -A schedule_demo worker -l info`
> 或者合并执行 `celery -A schedule_demo worker -l info -B`

方法一：

```python
@cel.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
  from schedule_demo.task1 import send_a_email
  # Calls test('hello') every 10 seconds.
  sender.add_periodic_task(10.0, send_a_email.s('hello'), name='add every 10')

  # Calls test('world') every 30 seconds
  sender.add_periodic_task(30.0, send_a_email.s('world'), expires=10)

  # Executes every Monday morning at 7:30 a.m.
  sender.add_periodic_task(
    crontab(hour=47, minute=10, day_of_week=1),
    send_a_email.s('Happy Mondays!'),
  )
```

方法二：

```python
cel.conf.beat_schedule = {
  # 名字随意命名
  'task_name_schedule_at': {
    'task': 'schedule_demo.task1.send_a_email', # 执行tasks1下的send_a_email函数
    # 每隔2秒执行一次
    # 'schedule': 1.0,
    'schedule': crontab(minute="*/2"),  # '*/1': 每分钟， '*/2': 每2分钟
    # 'schedule': timedelta(seconds=6), # 每隔6s发一次
    # 传递参数
    'args': (' 张三A ',)
  },
}
```
[schedule的配置方法](https://docs.celeryproject.org/en/stable/reference/celery.schedules.html#celery.schedules.crontab)

## Reference
    * [中文文档](http://docs.jinkan.org/docs/celery/)
