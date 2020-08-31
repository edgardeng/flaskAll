'''
 @date: 2020-08-31
 @author: edgardeng

-- demo to use RabbitMQ in Python (pika-1.1.0)

'''
import pika
import time
import uuid


QUEUE_HELLO_WORLD = 'hello_world'
QUEUE_TASK_QUEUE = 'task_queue'
EXCHANGE_PUBLISH_SUBSCRIBE = 'exchange_publish_subscribe'
EXCHANGE_DIRECT = 'exchange_direct'
EXCHANGE_TOPIC = 'exchange_topic'
QUEUE_RPC = 'queue_rpc'

def rabbit_connection():
  user_pwd = pika.PlainCredentials('test', '123456')
  params = pika.ConnectionParameters(host='localhost',
                                     port=5672,
                                     virtual_host='test',
                                     credentials=user_pwd)
  connection = pika.BlockingConnection(params)
  return connection


def hello_world_usage():
  connection = rabbit_connection()
  channel = connection.channel()
  channel.queue_declare(QUEUE_HELLO_WORLD)
  message = 'hello world'
  channel.basic_publish(exchange='', routing_key=QUEUE_HELLO_WORLD, body=message)
  print(' [x] Sent %r' % message)
  connection.close()


def work_queues_usage():
  connection = rabbit_connection()
  channel = connection.channel()
  channel.queue_declare(queue=QUEUE_TASK_QUEUE, durable=True)
  # send  msg 5 times
  for i in range(1, 6):
    message = ' Hello World ' + str(i) + ' ' + '.' * i
    channel.basic_publish(
      exchange='',
      routing_key=QUEUE_TASK_QUEUE,
      body=message,
      properties=pika.BasicProperties(
        delivery_mode=2,  # make message persistent
      ))
    print(" [x] Sent %r" % message)
    time.sleep(2)
  # 发送5次消息，如果有2个消费者，则平均分配给他们
  connection.close()


def publish_subscribe_usage():
  connection = rabbit_connection()
  channel = connection.channel()
  channel.exchange_declare(exchange=EXCHANGE_PUBLISH_SUBSCRIBE, exchange_type='fanout')
  for i in range(1, 7):
    message = ' Hello World ' + str(i) + ' ' + '.' * i
    channel.basic_publish(exchange=EXCHANGE_PUBLISH_SUBSCRIBE, routing_key='', body=message)  # send message to exchange
    print(" [x] Sent %r" % message)
    time.sleep(2)
  # 发送5次消息，如果有2个消费者，则平均分配给他们
  connection.close()


def direct_exchange_usage():
  connection = rabbit_connection()
  channel = connection.channel()
  channel.exchange_declare(exchange=EXCHANGE_DIRECT, exchange_type='direct')
  routers = ['info', 'warning', 'error']
  for i in range(1, 6):
    message = routers[i % 3] + ': Hello World ' + str(i) + ' ' + '.' * i
    channel.basic_publish(exchange=EXCHANGE_DIRECT, routing_key=routers[i % 3],
                          body=message)  # send message to exchange
    print(" [x] Sent %r" % message)
    time.sleep(2)
  connection.close()


def topic_usage():
  connection = rabbit_connection()
  channel = connection.channel()
  channel.exchange_declare(exchange=EXCHANGE_TOPIC, exchange_type='topic')
  routers = ['kern.critical', 'critical kernel error']
  for i in range(1, 6):
    message = routers[i % 2] + ': Hello World ' + str(i) + ' ' + '.' * i
    channel.basic_publish(exchange=EXCHANGE_TOPIC, routing_key=routers[i % 2],
                          body=message)  # send message to exchange
    print(" [x] Sent %r" % message)
    time.sleep(2)
  connection.close()


class FibonacciRpcClient(object):

  def __init__(self, connection):
    self.connection = connection
    self.channel = self.connection.channel()
    result = self.channel.queue_declare(queue='', exclusive=True)
    self.callback_queue = result.method.queue
    # print('[FibonacciRpcClient] consumer :', self.callback_queue)
    self.channel.basic_consume(
      queue=self.callback_queue,
      on_message_callback=self.on_response,
      auto_ack=True)

  def on_response(self, ch, method, props, body):
    if self.corr_id == props.correlation_id:
      self.response = body

  def call(self, n):
    self.response = None
    self.corr_id = str(uuid.uuid4())
    self.channel.basic_publish(
      exchange='',
      routing_key=QUEUE_RPC,
      properties=pika.BasicProperties(
        reply_to=self.callback_queue,
        correlation_id=self.corr_id,
      ),
      body=str(n))
    while self.response is None:
      self.connection.process_data_events()
    return int(self.response)


def rpc_usage():
  fibonacci_rpc = FibonacciRpcClient(rabbit_connection())
  print(" [x] Requesting fib(30)")
  response = fibonacci_rpc.call(30)
  print(" [.] Got %r" % response)



if __name__ == '__main__':
  # hello_world_usage()
  # work_queues_usage()
  # publish_subscribe_usage()
  # direct_exchange_usage()
  topic_usage()
  # rpc_usage()
