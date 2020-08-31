import json
import pika
import urllib3
import time

QUEUE_FRUIT_ORDER = 'queue_fruit_order'
fruits_ok = ['apple', 'pear']

def rabbit_connection():
  user_pwd = pika.PlainCredentials('test', '123456')
  params = pika.ConnectionParameters(host='localhost',
                                     port=5672,
                                     virtual_host='test',
                                     credentials=user_pwd)
  connection = pika.BlockingConnection(params)
  return connection


def callback_add_order(ch, method, properties, body):
  order = json.loads(body)
  print(' [x] Received: %r' % order)
  count = int(order['count'])
  url = 'http://127.0.0.1:5000/callback'
  http = urllib3.PoolManager()
  if count < 0 or count > 20:
    order['status'] = 'cancelled'
  elif order['name'] in fruits_ok:
    encoded_data = json.dumps(order).encode('utf-8')
    r = http.request('POST', url, body=encoded_data, headers={'Content-Type': 'application/json'})
    time.sleep(0.5 * count)
    order['status'] = 'complete'
  else:
    order['status'] = 'cancelled'
  # 我们用本地的一个简单html文件来测试
    # 结果返回
  encoded_data = json.dumps(order).encode('utf-8')
  r = http.request('POST', url, body=encoded_data, headers={'Content-Type': 'application/json'})
  ch.basic_ack(delivery_tag=method.delivery_tag)


connection = rabbit_connection()
channel = connection.channel()
channel.queue_declare(QUEUE_FRUIT_ORDER)
channel.basic_consume(QUEUE_FRUIT_ORDER, callback_add_order, False)
# print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
