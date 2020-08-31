#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2020-08-31
@author: edgardeng

-- demo for flask with rabbitMQ (flask-1.1.2 , flask-apscheduler-1.11.0  )

"""
import json

from flask import Flask,render_template, jsonify, redirect, request
import pika
import uuid


def rabbit_connection():
  user_pwd = pika.PlainCredentials('test', '123456')
  params = pika.ConnectionParameters(host='localhost',
                                     port=5672,
                                     virtual_host='test',
                                     credentials=user_pwd)
  connection = pika.BlockingConnection(params)
  return connection


app = Flask(__name__)
#   app = Flask(__name__, instance_relative_config=True, instance_path=_default_instance_path)
# app.config.from_pyfile('dev.py')
# app.register_blueprint(rabbit.rabbit_blueprint, url_prefix='/rabbit')
orders = []
fruits = ['apple', 'pear', 'others']
fruits_ok = ['apple', 'pear']
QUEUE_FRUIT_ORDER = 'queue_fruit_order'


@app.route('/')
def index():
  return render_template('index.html', fruits=fruits, orders=orders)


@app.route('/', methods=['POST'])
def order_add():
  if not request.json or 'name' not in request.json:
    return jsonify({'msg': 'no form data'})
  print(type(request.json), request.json)
  order = request.json
  add_order(name=order['name'], count=order['count'])
  return render_template('index.html', funcs=fruits, jobs=orders)


def add_order(**kwargs):
  id = str(uuid.uuid1())[:8]
  order = {
    'id': id,
    'name': kwargs['name'],
    'count': kwargs['count'],
    'status': 'created' # created, producing, complete, cancelled
  }
  connection = rabbit_connection()
  channel = connection.channel()
  channel.queue_declare(QUEUE_FRUIT_ORDER)
  channel.basic_publish(exchange='', routing_key=QUEUE_FRUIT_ORDER, body=json.dumps(order))
  print(' [x] Sent %r' % order)
  connection.close()

def callback_add_order(ch, method, properties, body):
    print(' [x] Received %r' % body)
    # time.sleep(2)
    print('callback done')
    ch.basic_ack(delivery_tag=method.delivery_tag)  # use basic_ak() when no_ack ==False
  # if order['name'] not in fruits_ok:
  #   order['status'] = 'cancelled' # 无法生产
  # else:
  #   # 加入生产消息队列
  #   pass
  # orders.append(order) # 加入内存


# async def hello_world_usage():
#   connection = rabbit_connection()
#   channel = connection.channel()
#   channel.queue_declare(QUEUE_FRUIT_ORDER)
#   channel.basic_consume(QUEUE_FRUIT_ORDER, callback_add_order, False)
#   # print(' [*] Waiting for messages. To exit press CTRL+C')
#   await channel.start_consuming()


if __name__ == '__main__':
  app.run()


# '''视图函数 - rabbit.py'''
# from flask import Blueprint
# from flask_restful import Resource
#
# from extensions import fpika
# from tasks import task0
#
# from . import Api

# '''视图函数 - rabbit.py'''
#
# rabbit_blueprint = Blueprint('rabbit', __name__)
# rabbit_api = Api(rabbit_blueprint)
#
#
# class Producer(Resource):
#   def get(self):
#     print('Producer')
#     channel = fpika.channel()
#     channel.queue_declare(queue='test')
#     channel.basic_publish(exchange='', routing_key='test', body='hello pika')
#     # 将通道还给池
#     # return_broken_channel 在该框架下使用解决队列堵塞问题，详见下方分析
#     fpika.return_broken_channel(channel)
#     fpika.return_channel(channel)
#     return 'Producer'
#
#
# rabbit_api.add_resource(Producer, '/Producer')
