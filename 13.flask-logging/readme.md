# Logging

> 使用Python标准模块在Flask做日志输出

## 

### 简单使用

```python
import logging  # 引入logging模块

logging.debug("logging debug")
logging.info("logging info")
logging.warning("logging warning")
logging.error("logging error")
logging.critical("logging critical")

```

### 1. 日志级别

默认生成的root logger的level是logging.WARNING,低于该级别的就不输出了

级别排序:CRITICAL > ERROR > WARNING > INFO > DEBUG

debug : 打印全部的日志,详细的信息,通常只出现在诊断问题上

info : 打印info,warning,error,critical级别的日志,确认一切按预期运行

warning : 打印warning,error,critical级别的日志,一个迹象表明,一些意想不到的事情发生了,或表明一些问题在不久的将来(例如。磁盘空间低”),这个软件还能按预期工作

error : 打印error,critical级别的日志,更严重的问题,软件没能执行一些功能

critical : 打印critical级别,一个严重的错误,这表明程序本身可能无法继续运行

### 2. 基本配置

使用配置`logger.baseConfig([**kwargs])`,示例：
```python
logfmt = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
logfile = './log.txt'
logging.basicConfig(level=logging.INFO, format=logfmt, 
  filename=logfile, filemode='w')
```

可用参数：
* filename 指定日志文件名；
* filemode：和file函数意义相同，指定日志文件的打开模式，'w'或者'a'；
* format：指定输出的格式和内容，format可以输出很多有用的信息，
* datefmt: 指定日期时间格式
* level 设置rootlogger的日志级别
* strean 指定的stream创建StreamHandler。可输出到sys.stderr，sys.stdout

format参数可使用的格式化：

* %(name)s: Logger的名字
* %(levelno)s: 打印日志级别的数值
* %(levelname)s: 打印日志级别名称
* %(pathname)s: 日志输出函数模块的完整路径。其实就是sys.argv[0]
* %(filename)s: 日志输出函数模块的文件名
* %(funcName)s: 打印日志的当前函数
* %(lineno)d: 调用日志输出函数的语句所在的代码行
* %(created)f: 当前时间
* %(relativeCreated)d: 输出日志时，自logger创建以来的时间
* %(asctime)s: 字符串时间的当前时间
* %(thread)d: 打印线程ID
* %(threadName)s: 打印线程名称
* %(process)d: 打印进程ID
* %(message)s: 打印日志信息

datefmt的日期格式化：

* %Y 年份的长格式，1999
* %y 年份的短格式，99
* %m 月份，01-12
* %d 日期，01-31
* %H 小时，0-23
* %w 星期，0-6。周日开始
* %M 分钟，00-59
* %S 秒，00-59


#### 使用相关函数进行配置
```python
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
```


logging中包含的handler主要有如下几种，

|handler名称| ：位置；|作用|
|:----|:----|:----|
|StreamHandler：|logging.StreamHandler；|日志输出到流，可以是sys.stderr，sys.stdout或者文件|
|FileHandler：|logging.FileHandler；|日志输出到文件|
|BaseRotatingHandler：|logging.handlers.BaseRotatingHandler；|基本的日志回滚方式|
|RotatingHandler：|logging.handlers.RotatingHandler；|日志回滚方式，支持日志文件最大数量和日志文件回滚|
|TimeRotatingHandler：|logging.handlers.TimeRotatingHandler；|日志回滚方式，在一定时间区域内回滚日志文件|
|SocketHandler：|logging.handlers.SocketHandler；|远程输出日志到TCP/IP sockets|
|DatagramHandler：|logging.handlers.DatagramHandler；|远程输出日志到UDP sockets|
|SMTPHandler：|logging.handlers.SMTPHandler；|远程输出日志到邮件地址|
|SysLogHandler：|logging.handlers.SysLogHandler；|日志输出到syslog|
|NTEventLogHandler：|logging.handlers.NTEventLogHandler；|远程输出日志到Windows NT/2000/XP的事件日志|
|MemoryHandler：|logging.handlers.MemoryHandler；|日志输出到内存中的指定buffer|
|HTTPHandler：|logging.handlers.HTTPHandler；|通过"GET"或者"POST"远程输出到HTTP服务器|

```python
# 日志回滚的使用
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
#定义一个RotatingFileHandler，最多备份3个日志文件，每个日志文件最大1K
rHandler = RotatingFileHandler("log.txt",maxBytes = 1*1024,backupCount = 3)
rHandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rHandler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

logger.addHandler(rHandler)
logger.addHandler(console)

logger.info("Start print log")
logger.debug("Do something")
logger.warning("Something maybe fail.")
logger.info("Finish")
# 会出现 3 个备份文件
```

日志滚动和删除
```python
import logging
from logging.handlers import TimedRotatingFileHandler

def backroll():
    #日志打印格式
    log_fmt = '%(asctime)s - File:%(filename)s,-line: %(lineno)s %(levelname) -Msg: %(message)s'
    formatter = logging.Formatter(log_fmt)

    #创建TimedRotatingFileHandler对象
    log_file_handler = TimedRotatingFileHandler(filename="ds_update", when="M", interval=2, backupCount=2)
    #log_file_handler.suffix = "%Y-%m-%d_%H-%M.log"
    #log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")
    log_file_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger()
    log.addHandler(log_file_handler)
    #循环打印日志
    log_content = "test log"
    count = 0
    while count < 30:
        log.error(log_content)
        time.sleep(20)
        count = count + 1
    log.removeHandler(log_file_handler)
```

filename：日志文件名的prefix；

when：是一个字符串，用于描述滚动周期的基本单位，字符串的值及意义如下： 
“S”: Seconds 
“M”: Minutes 
“H”: Hours 
“D”: Days 
“W”: Week day (0=Monday) 
“midnight”: Roll over at midnight
interval: 滚动周期，单位有when指定，比如：when=’D’,interval=1，表示每天产生一个日志文件
backupCount: 表示日志文件的保留个数
    

### 3. 捕获traceback

```python
import logging
logger = logging.getLogger(__name__)
try:
    open("sklearn.txt","rb")
except (SystemExit,KeyboardInterrupt):
    raise
except Exception:
    logger.error("Faild to open sklearn.txt from logger.error",exc_info = True)
logger.info("Finish")

```

### 4.多模块使用logging
主模块mainModule.py，
```python

import logging
import subModule
logger = logging.getLogger("mainModule")
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)

logger.addHandler(handler)
logger.addHandler(console)


logger.info("creating an instance of subModule.subModuleClass")
a = subModule.SubModuleClass()
logger.info("calling subModule.subModuleClass.doSomething")
a.doSomething()
logger.info("done with  subModule.subModuleClass.doSomething")
logger.info("calling subModule.some_function")
subModule.som_function()
logger.info("done with subModule.some_function")

```

子模块subModule.py，
```python
import logging

module_logger = logging.getLogger("mainModule.sub")
class SubModuleClass(object):
    def __init__(self):
        self.logger = logging.getLogger("mainModule.sub.module")
        self.logger.info("creating an instance in SubModuleClass")
    def doSomething(self):
        self.logger.info("do something in SubModule")
        a = []
        a.append(1)
        self.logger.debug("list a = " + str(a))
        self.logger.info("finish something in SubModuleClass")

def som_function():
    module_logger.info("call function some_function")
```

### 5. 使用Yaml进行配置

通过YAML文件进行配置，比JSON看起来更加简介明了，
```yaml
version: 1
disable_existing_loggers: False
formatters:
        simple:
            format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
handlers:
    console:
            class: logging.StreamHandler
            level: DEBUG
            formatter: simple
            stream: ext://sys.stdout
    info_file_handler:
            class: logging.handlers.RotatingFileHandler
            level: INFO
            formatter: simple
            filename: info.log
            maxBytes: 10485760
            backupCount: 20
            encoding: utf8
    error_file_handler:
            class: logging.handlers.RotatingFileHandler
            level: ERROR
            formatter: simple
            filename: errors.log
            maxBytes: 10485760
            backupCount: 20
            encoding: utf8
loggers:
    my_module:
            level: ERROR
            handlers: [info_file_handler]
            propagate: no
root:
    level: INFO
    handlers: [console,info_file_handler,error_file_handler]
```

通过YAML加载配置文件，然后通过logging.dictConfig配置logging，
```python
def setup_logging(default_path = "logging.yaml",default_level = logging.INFO,env_key = "LOG_CFG"):
    path = default_path
    value = os.getenv(env_key,None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path,"r") as f:
            config = yaml.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level = default_level)

if __name__ == "__main__":
    setup_logging(default_path = "logging.yaml")
    
```

## 参考

* [Python Logging](https://docs.python.org/2/library/logging.html)