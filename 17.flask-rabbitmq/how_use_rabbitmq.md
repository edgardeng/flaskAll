# RabbitMQ 教程

## 术语简介

1. Producing：发送消息，发送消息的程序是生产者(producer)

2. Queue: 队列，RabbitMQ的内部对象，用于存储消息。队列不受任何限制，本质上是一个无限缓冲区

3. Consuming: 消费/接收消息。消费者(consumer)是大多数等待接收消息的程序。

    > 多个消费者可以订阅同一个队列，这时队列中的消息会被平均分摊给多个消费者进行处理，而不是每个消费者都收到所有的消息并处理。
      
## RabbitMQ的使用方式

### 1. Hello World  (单个对单个)
![](https://www.rabbitmq.com/img/tutorials/python-one-overall.png)

创建连接工具：

```python
import pika
QUEUE_HELLO_WORLD = 'hello_world'
def rabbit_connection():
  user_pwd = pika.PlainCredentials('test', '123456')
  params = pika.ConnectionParameters(host='localhost',
                                     port=5672,
                                     virtual_host='test',
                                     credentials=user_pwd)
  connection = pika.BlockingConnection(params)
  return connection
```

发布者发送消息

```python
def hello_world_usage():
  connection = rabbit_connection()
  channel = connection.channel()
  channel.queue_declare(QUEUE_HELLO_WORLD)
  message = 'hello world'
  channel.basic_publish(exchange='', routing_key=QUEUE_HELLO_WORLD, body=message)
  print(' [x] Sent %r' % message)
  connection.close()
```

消费者接收消息

```python
def hello_world_usage():
  queue_name = "test_hello_world"
  connection = rabbit_connection()
  channel = connection.channel()
  channel.queue_declare(QUEUE_HELLO_WORLD)

  def callback(ch, method, properties, body):
    print(' [x] Received %r' % body)

  channel.basic_consume(QUEUE_HELLO_WORLD, callback, True)
  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()
```

### 2. Work queues 任务分发(竞争消费者模式)
> [reference doc](https://www.rabbitmq.com/tutorials/tutorial-two-python.html)

![](https://www.rabbitmq.com/img/tutorials/python-two.png)

By default, RabbitMQ will send each message to the next consumer, in sequence.

On average every consumer will get the same number of messages. This way of distributing messages is called round-robin. 

## Message acknowledgment 消息确认
> An ack(nowledgement) is sent back by the consumer to tell RabbitMQ that a particular message had been received, processed and that RabbitMQ is free to delete it.

> Manual message acknowledgments are turned on by default.  默认开启自动确认


```python
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    time.sleep( body.count('.') )
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag) # 手动确认

```

### Message durability 消息持久性

> our tasks will still be lost if RabbitMQ server stops.
> When RabbitMQ quits or crashes it will forget the queues and messages unless you tell it not to. 

1.  queue will survive a RabbitMQ node restart 
    `channel.queue_declare(queue='task_queue', durable=True)`
2. mark our messages as persistent - by supplying a delivery_mode property with a value 
    `channel.basic_publish(exchange='',
                           routing_key="task_queue",
                           body=message,
                           properties=pika.BasicProperties(
                              delivery_mode = 2, # make message persistent
                           ))`

### Fair dispatch 公平调度
>  This uses the basic.qos protocol method to tell RabbitMQ not to give more than one message to a worker at a time. Or, in other words, don't dispatch a new message to a worker until it has processed and acknowledged the previous one. Instead, it will dispatch it to the next worker that is not still busy.
 
`channel.basic_qos(prefetch_count=1)`

### 3. Publish/Subscribe 订阅模式
> deliver a message to multiple consumers.

![](https://www.rabbitmq.com/img/tutorials/exchanges.png)

the full messaging model in Rabbit.
   * producer: is a user application that sends messages.
   * queue is a buffer that stores messages.
   * consumer is a user application that receives messages.

#### Exchanges 交换机
> 生产者在将消息发送给交换机，交换机把消息推到队列中
> the producer can only send messages to an exchange.   On one side it receives messages from producers and the other side it pushes them to queues.

##### exchange types  交换机的几种类型

* fanout
>  broadcasts all the messages it receives to all the queues it knows 群发到所有绑定的queue

* direct 直连: 把消息投递到那些binding key与routing key完全匹配的队列中

* topic  主题: 将消息路由到binding key与routing key模式匹配的队列中

    符号 "#" 匹配一个或多个词
    符号 "*" 匹配一个词

* headers (不常用) 

    根据arguments来routing。

    arguments为一组key-value对，任意设置。

    “x-match”是一个特殊的key，值为“all”时必须匹配所有argument，值为“any”时只需匹配任意一个argument，不设置默认为“all”。

##### Temporary queues 临时队列

To do it we could create a queue with a random name, or, even better - let the server choose a random queue name for us. We can do this by supplying empty queue parameter to queue_declare:

` result = channel.queue_declare(queue='') `

 once the consumer connection is closed, the queue should be deleted.
 `result = channel.queue_declare(queue='', exclusive=True)`

##### Binding 绑定
> That relationship between exchange and a queue is called a binding. 将Exchange与Queue关联起来

`channel.queue_bind(exchange='logs',
                    queue=result.method.queue)`


### 4.Routing 路由模式
选择性的接收消息
![](./pic/rabbitmq-four.png)

#### Binding 绑定
Bindings can take an extra routing_key parameter.

`channel.queue_bind(exchange=exchange_name,
                    queue=queue_name,
                    routing_key='black')`

#### Direct exchange
> a message goes to the queues whose binding key exactly matches the routing key of the message
![](https://www.rabbitmq.com/img/tutorials/direct-exchange.png)


#### Multiple bindings
 bind multiple queues with the same binding key.
 ![](https://www.rabbitmq.com/img/tutorials/direct-exchange-multiple.png)
 

### 5.Topics 主题模式
基于模式(主题)来接收消息

![](https://www.rabbitmq.com/img/tutorials/python-five.png)

__Topic exchange__ 路由模式的交换机

> Messages sent to a topic exchange can't have an arbitrary routing_key - it must be a list of words, delimited by dots. 
通过`.`来隔开单词

However there are two important special cases for binding keys:

* `* (star)` can substitute for exactly one word.
* `# (hash)` can substitute for zero or more words.

> 使用正则表达式进行匹配。其中“#”表示所有、全部的意思；“*”只匹配到一个词。

匹配规则案例：
> 路由键：routings = [ 'happy.work',  'happy.life' , 'happy.work.teacher',  'sad.work',  'sad.life', 'sad.work.teacher' ]

"happy.#"：匹配  'happy.work',  'happy.life' , 'happy.work.teacher'

"work.#"：无匹配

“happy.*”：匹配 'happy.work',  'happy.life'

"*.work"：匹配 'happy.work',  'sad.work'

"*.work.#"：匹配  'happy.work',  'happy.work.teacher',  'sad.work', 'sad.work.teacher' 


### 6.RPC Remote procedure call (RPC) 远程调用
 
请求/回复(RPC) 模式实例
![](./pic/rabbitmq-six.png)

#### Client interface

 sends an RPC request and blocks until the answer is received：
 
```python
fibonacci_rpc = FibonacciRpcClient()
result = fibonacci_rpc.call(4)
print("fib(4) is %r" % result)

```


Bearing that in mind, consider the following advice:

* Make sure it's obvious which function call is local and which is remote.
* Document your system. Make the dependencies between components clear.
* Handle error cases. How should the client react when the RPC server is down for a long time?

#### Callback queue

 In order to receive a response the client needs to send a 'callback' queue address with the request.
 
```python
result = channel.queue_declare(queue='', exclusive=True)
callback_queue = result.method.queue

channel.basic_publish(exchange='',
                      routing_key='rpc_queue',
                      properties=pika.BasicProperties(
                            reply_to = callback_queue,
                            ),
                      body=request)
```

The AMQP 0-9-1 protocol predefines a set of 14 properties that go with a message. Most of the properties are rarely used, with the exception of the following:

* delivery_mode: Marks a message as persistent (with a value of 2) or transient (any other value). You may remember this property from the second tutorial.
* content_type: Used to describe the mime-type of the encoding. For example for the often used JSON encoding it is a good practice to set this property to: application/json.
* reply_to: Commonly used to name a callback queue.
* correlation_id: Useful to correlate RPC responses with requests.


#### Correlation id

![](https://www.rabbitmq.com/img/tutorials/python-six.png)

Our RPC will work like this:

* When the Client starts up, it creates an anonymous exclusive callback queue.
* For an RPC request, the Client sends a message with two properties: reply_to, which is set to the callback queue and correlation_id, which is set to a unique value for every request.
* The request is sent to an rpc_queue queue.
* The RPC worker (aka: server) is waiting for requests on that queue. When a request appears, it does the job and sends a message with the result back to the Client, using the queue from the reply_to field.
* 
The client waits for data on the callback queue. When a message appears, it checks the correlation_id property. If it matches the value from the request it returns the response to the application.
