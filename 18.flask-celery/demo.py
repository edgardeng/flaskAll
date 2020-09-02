"""
@date: 2020-09-01
@author: edgardeng

-- demo for flask + celery  + rabbitmq (celery-4.4.7)

"""
from datetime import timedelta, datetime

from celery import Celery

app = Celery(
  'demo',  # 当前模块的名字
  broker='amqp://test:123456@localhost:5672/test'  # 消息队列的url
)


@app.task
def add(x, y):
  print('%r + %r = %r'% (x,y,x+y))
  return x + y


'''
1. 启动celry work $ celery worker -A demo.app -l INFO 
(因为从demo启动，所以Celery对象的名称一定也要是demo)
'''
if __name__ == '__main__':
  add.delay(1, 2)
  add.apply_async(args=(2, 3))
  add.apply_async(args=(4, 3),countdown=10)
  # 从现在起10秒内执行,使用指定eta
  add.apply_async(args=(4, 3),eta=datetime.now() + timedelta(seconds=10))
  # 从现在起一分钟后执行，但在2分钟后过期
  add.apply_async(args=(4, 3),countdown=60, expires=120)
  # 在2天后到期，设置使用datetime对象
  add.apply_async(args=(4, 3),expires=datetime.now() + timedelta(days=2))

  # add.apply_async(args=[arg1, arg2], kwargs={'kwargs': 'x', 'kwargs': 'y'})
  # add.apply_async((arg,), {'kwarg': value})

  # # send_task：任务未在当前进程中注册
  # app.send_task('任务', args=[arg, ], queue='default')
  # # signature用于传递任务调用签名的对象(例如通过网络发送),并且它们也支持calling api
  # add.s(arg1, arg2, kwarg1='x', kwargs2='y').apply_async()
