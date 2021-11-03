# -*- coding: utf-8 -*-
# @author: dengxixi
# @date:   2021-11-03
# @file:   Use Socket.io to Build a WebRTC Server
# Reference : https://github.com/nanomosfet/WebRTC-Flask-server
# python-socketio-5.4.1


from flask import Flask, render_template, url_for
from flask.logging import create_logger
import socketio
import eventlet.wsgi

sio = socketio.Server()
app = Flask(__name__)
logger = create_logger(app)

connected_particpants = {}


@app.route('/')
def index():
    return render_template('index.html', room='default')


@sio.on('message', namespace='/')
def message(sid, msg):
    print(f'sio.received: {sid}, {msg}')
    sio.emit('message', msg)  # 广播


@sio.on('connect', namespace='/')
def connect(sid, environ, auth):
    print(f'sio.connect: {sid}, {environ}')
    print(auth)


@sio.on('disconnect', namespace='/')
def disconnect(sid):
    print("Received Disconnect message from %s" % sid)
    for room, clients in connected_particpants.items():
        try:
            clients.remove(sid)
            print("Removed %s from %s \n list of left participants is %s" % (sid, room, clients))
        except ValueError:
            print("Remove %s from %s \n list of left participants is %s has failed" % (sid, room, clients))


@sio.on('create_or_join', namespace='/')
def create_or_join(sid, room):
    """
    加入房间
    :param sid:
    :param data:
    :return:
    """
    sio.enter_room(sid, room)
    print(f'Welcome {sid} to {room}')
    sio.emit('join', room)


@app.route('/<room>')
def room(room):
    return render_template('index.html', room=room)


if __name__ == '__main__':
    c = socketio.WSGIApp(sio, app)
    # app.run(host='0.0.0.0', debug=True)
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 5001)), c)
