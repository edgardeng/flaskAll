# RabbitMQ

> 消息队列（MQ）是一种应用程序对应用程序的通信方法。MQ是消费-生产者模型的一个典型的代表，一端往消息队列中不断写入消息，而另一端则可以读取队列中的消息

RabbitMQ是一个在AMQP基础上完成的，可复用的企业消息系统，遵循Mozilla Public License开源协议

AMQP （Advanced Message Queue Protocol） 一个提供统一消息服务的应用层标准高级消息队列协议。是应用协议的一个开发标准，为面向消息的中间件。
基于此协议，客服端与消息中间件可传递消息，并不受客服端/中间件不同产品，不同开发语言邓条件的限制


      
## 安装

### Linux安装RabbitMQ

1.安装 Erlang 环境
    a. 安装GCC GCC-C++ Openssl等模块 `yum -y install make gcc gcc-c++ kernel-devel m4 ncurses-devel openssl-devel `
    b. 安装ncurses `yum -y install ncurses-devel`
    c. 安装erlang环境
```
wget http://erlang.org/download/otp_src_18.2.1.tar.gz
tar xvfz otp_src_18.2.1.tar.gz 
./configure 
make install
```

2. 安装RabbitMQ

    a. 下载rabbitmq-server `wget http://www.rabbitmq.com/releases/rabbitmq-server/v3.6.9/rabbitmq-server-generic-unix-3.6.9.tar.xz`

    b. 对于下载xz包进行解压，首先先下载xz压缩工具：`yum install xz`

    c. 对rabbitmq包进行解压：
        `xz -d xz -d rabbitmq-server-generic-unix-3.6.9.tar.xz`
        `tar -xvf rabbitmq-server-generic-unix-3.6.9.tar`
    
    d. 移动至/usr/local/下 改名rabbitmq：
        `cp -r rabbitmq_server-3.6.9 /usr/local/rabbitmq`

    e. 解压后直接可以使用, 设置路径 
        `export PATH=/usr/local/rabbitmq/sbin:$PATH`
        `source /etc/profile`   
         
3. MQ的管理
    * 启动后台管理 `rabbitmq-plugins enable rabbitmq_management`
    * 后台运行 `rabbitmq-server -detached`
    * 端口设置，可供外部访问 `iptables -I INPUT -p tcp --dport 15672 -j ACCEPT`

4. 添加用户和权限
    > 默认网页guest用户是不允许访问的，需要增加一个用户修改一下权限

    * 添加用户: `rabbitmqctl add_user admin admin `

    * 添加权限: `rabbitmqctl set_permissions -p "/" admin ".*" ".*" ".*" `

    * 修改用户角色: `rabbitmqctl set_user_tags admin administrator `

5. RabbitMQ的简单指令

    * 启动服务：rabbitmq-server -detached【 /usr/local/rabbitmq/sbin/rabbitmq-server  -detached 】
    * 重启服务：rabbitmq-server restart
    * 关闭服务：rabbitmqctl stop
    * 查看状态：rabbitmqctl status
    * 列出角色：rabbitmqctl list_users
    * 开启某个插件：rabbitmq-plugins enable xxx
    * 关闭某个插件：rabbitmq-plugins disable xxx 

6. 插件的安装

    * 安装消息延迟插件
    
### Docker安装RabbitMQ

1. docker pull rabbitmq:management (拉取镜像)

2. docker run -d -p 5672:5672 -p 15672:15672 --name rabbitM rabbitmq:management

3. 访问管理界面  http://[宿主机IP]:15672 (rabbitmq:latest 没有管理界面)
   默认guest/guest
   
4. 关闭容器: docker stop rabbitM

5. 启动容器: docker stop rabbitM


## RabbitMQ 的管理

### 用户 Users

进入 http://localhost:15672/#/users 进行设置

用户权限（级别）
|TAG| 名称|说明|
|Admin|超级管理员|查看所有信息|
|Monitoring|监控者|可登陆控制台，查看节点信息，|
|Policymaker|策略制定者|可登陆控制台，制定策略，无法查看节点|
|Management|普通管理员|仅能登陆控制台|
|Impersonator| - |:----|
|None|其他|无法登录控制台，一般提供者，消费者|


### 虚拟主机 vhost

> 相当于数据库中库的概念

进入 http://localhost:15672/#/vhosts 查看

可添加vhost，点击某个vhost，可修改vhost的权限
