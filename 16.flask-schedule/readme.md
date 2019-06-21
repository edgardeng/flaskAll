# Flask Schedule

## Flask-APScheduler
> a Flask extension supported for the [APScheduler](https://github.com/agronholm/apscheduler) which is a Task scheduling library for Python.

### how to use

```python
from flask import Flask
from flask_apscheduler import APScheduler
class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__:job1',
            'args': (1, 2),
            'trigger': 'interval',
            'seconds': 10
        }
    ]

def job1(a, b):
    print(str(a) + ' ' + str(b))


if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(Config())

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    
    app.run()
```

### APScheduler Job

### add job

date 日期触发: 一次性指定日期 

* run_date (datetime|str) – 作业的运行日期或时间 
* timezone (datetime.tzinfo|str) – 指定时区 

```python
# 2016-12-12运行一次job_function
scheduler.add_job(job_function, 'date', run_date=date(2016, 12, 12), args=['text'])
# 2016-12-12 12:00:00运行一次job_function
scheduler.add_job(job_function, 'date', run_date=datetime(2016, 12, 12, 12, 0, 0), args=['text'])
```

interval 间隔调度

* weeks (int) – 间隔几周 
* days (int) – 间隔几天 
* hours (int) – 间隔几小时 
* minutes (int) – 间隔几分钟 
* seconds (int) – 间隔多少秒 
* start_date (datetime|str) – 开始日期 
* end_date (datetime|str) – 结束日期 
* timezone (datetime.tzinfo|str) – 时区 

```python
# 每两个小时调一下job_function
sched.add_job(job_function, 'interval', hours=2)
```

Cron 触发

* year (int|str) – 年，4位数字 
* month (int|str) – 月 (范围1-12) 
* day (int|str) – 日 (范围1-31) 
* week (int|str) – 周 (范围1-53) 
* day_of_week (int|str) – 周内第几天或者星期几 (范围0-6 或者 mon,tue,wed,thu,fri,sat,sun) 
* hour (int|str) – 时 (范围0-23) 
* minute (int|str) – 分 (范围0-59) 
* second (int|str) – 秒 (范围0-59) 
* start_date (datetime|str) – 最早开始日期(包含) 
* end_date (datetime|str) – 最晚结束时间(包含) 
* timezone (datetime.tzinfo|str) – 指定时区 
```python
# job_function将会在6,7,8,11,12月的第3个周五的1,2,3点运行
sched.add_job(job_function, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')
# 截止到2016-12-30 00:00:00，每周一到周五早上五点半运行job_function
sched.add_job(job_function, 'cron', day_of_week='mon-fri', hour=5, minute=30, end_date='2016-12-31')

```

#### 使用装饰器

```python
@scheduler.task('interval', id='do_job_1', seconds=30, misfire_grace_time=900)
def job1():
    print('Job 1 executed')


# cron examples
@scheduler.task('cron', id='do_job_2', minute='*')
def job2():
    print('Job 2 executed')
    
@scheduler.task('cron', id='do_job_3', week='*', day_of_week='sun')
def job3():
    print('Job 3 executed')
```

### pause a job

```python
scheduler.pause_job(id)
```

### resume a job
```python
scheduler.resume_job(id)
```

### remove a job
```python
scheduler.remove_job(id)
```