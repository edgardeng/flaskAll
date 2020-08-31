'''
 @date: 2020-08-31
 @author: edgardeng

-- demo to use RabbitMQ in Python (pika-1.1.0)

'''

import pika
import time


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

  def callback(ch, method, properties, body):
    print(' [x] Received %r' % body)
    time.sleep(2)
    print('callback done')
    ch.basic_ack(delivery_tag=method.delivery_tag)  # use basic_ak() when no_ack ==False

  channel.basic_consume(QUEUE_HELLO_WORLD, callback, False)
  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()


def work_queues_usage():
  connection = rabbit_connection()
  channel = connection.channel()
  channel.queue_declare(QUEUE_TASK_QUEUE, durable=True)

  def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)

  channel.basic_qos(prefetch_count=1)
  channel.basic_consume(queue=QUEUE_TASK_QUEUE, on_message_callback=callback)
  print(' [*] Waiting for messages. To exit press CTRL+C')
  channel.start_consuming()


def publish_subscribe_usage():
  connection = rabbit_connection()
  channel = connection.channel()
  channel.exchange_declare(exchange=EXCHANGE_PUBLISH_SUBSCRIBE, exchange_type='fanout')
  result = channel.queue_declare(queue='', exclusive=True)
  queue_name = result.method.queue
  print(queue_name)
  channel.queue_bind(exchange=EXCHANGE_PUBLISH_SUBSCRIBE, queue=queue_name)  # bind a queue to exchange
  print(' [*] Waiting for logs. To exit press CTRL+C')

  def callback(ch, method, properties, body):
    print(" [x] %r" % body)

  channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
  channel.start_consuming()


def direct_exchange_usage():
  connection = rabbit_connection()
  channel = connection.channel()
  channel.exchange_declare(exchange=EXCHANGE_DIRECT, exchange_type='direct')
  result = channel.queue_declare(queue='', exclusive=True)
  queue_name = result.method.queue
  severities = ['error']  # ['info', 'warning','error']
  for severity in severities:
    channel.queue_bind(exchange=EXCHANGE_DIRECT, queue=queue_name, routing_key=severity)

  def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

  channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

  print(' [*] Waiting for logs. To exit press CTRL+C')
  channel.start_consuming()

def topic_usage():
  connection = rabbit_connection()
  channel = connection.channel()
  channel.exchange_declare(exchange=EXCHANGE_TOPIC, exchange_type='topic')
  result = channel.queue_declare('', exclusive=True)
  queue_name = result.method.queue
  # ['#', 'kern.*', '*.critical',]
  binding_keys = ['kern.*']
  for binding_key in binding_keys:
    channel.queue_bind(exchange=EXCHANGE_TOPIC, queue=queue_name, routing_key=binding_key)
  print(' [*] Waiting for logs. To exit press CTRL+C')
  def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))
  channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
  channel.start_consuming()


def fib(n):
  if n == 0:
    return 0
  elif n == 1:
    return 1
  else:
    return fib(n - 1) + fib(n - 2)


def rpc_usage():
  connection = rabbit_connection()
  channel = connection.channel()
  channel.queue_declare(queue=QUEUE_RPC)

  def on_request(ch, method, props, body):
    n = int(body)
    print(" [.] fib(%s)" % n)
    response = fib(n)
    # print('[RPC] publish :', props.reply_to, props.correlation_id)
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

  channel.basic_qos(prefetch_count=1)
  channel.basic_consume(queue=QUEUE_RPC, on_message_callback=on_request)

  print(" [x] Awaiting RPC requests")
  channel.start_consuming()


if __name__ == '__main__':
  # hello_world_usage() # rabbitMQ
  # publish_subscribe_usage()
  # direct_exchange_usage()
  topic_usage()
  # rpc_usage()
