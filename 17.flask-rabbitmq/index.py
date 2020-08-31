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
orders = []
fruits = ['apple', 'pear', 'others']
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


@app.route('/callback', methods=['POST'])
def order_callback():
  order = request.json
  print('order_callback', order)
  for i in orders:
    if i['id'] == order['id']:
      orders[orders.index(i)] = order
      # i['status'] = order['status']
      return 'success'
  orders.append(request.json)
  return 'success'


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


# run this after run consumer.py
if __name__ == '__main__':
  app.run()
