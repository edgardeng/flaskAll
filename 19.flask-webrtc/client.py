# -*- coding: utf-8 -*-
# @author: dengxixi
# @date:   2021-11-03
# @file:   Use python-socketio to connect a server
# python-socketio-5.4.1
#
import random
import socketio

# standard Python
sio = socketio.Client()

# asyncio
# sio = socketio.AsyncClient()


@sio.event
def message(msg):
    print(name, msg, type(msg))
    return 'OK', 123


@sio.event
def connect():
    print("I'm connected!")


@sio.event
def connect_error(data):
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


# @sio.on('my message')
# def on_message(data):
#     print('I received a message!')
# sio.emit('my message', {'foo': 'bar'})


def send_message(msg):
    sio.emit('message', msg)  # The data can be of type str, bytes, dict, list or tuple.


def join(room):
    sio.emit('create_or_join', room)


@sio.event
def my_event(sid, data):
    # handle the message
    return "OK", 123


if __name__ == '__main__':
    import sys

    room = sys.argv[1]
    name = sys.argv[2]
    sio.connect('http://localhost:5000')
    print('I‘m ', sio.sid, name)
    join(room)
    sio.sleep(1)
    for i in range(5):
        send_message((name,  f'hello {i}'))
        sio.sleep(0.5 + random.random()*2)
    sio.disconnect()
    exit()
