from flask import Flask, render_template
import socketio
import eventlet.wsgi
import json

sio = socketio.Server(cors_allowed_origins='*', ping_timeout=35)
app = Flask(__name__)
ROOM = 'ROOM'

rooms = {}


@app.route('/')
def index():
    return render_template('multiple.html', room='default')


def broadcastTo(rooms, event, msg, sid):
    print("broadcastTo: %s ,%s" % (rooms, msg))
    if not rooms:
        print("no room")
        return
    sio.emit(event, msg, room=rooms, skip_sid=sid)


@sio.event
def connect(sid, environ):
    print("new connection, connection id: %s\n" % sid)


@sio.on('join-room')
def join(sid, room):
    room = json.loads(room)
    user = room.get('userId')
    name = room.get('roomName')
    print("join-room, user: %s, room: %s\n" % (user, name))
    sio.enter_room(sid, name)
    rooms[sid] = name
    broadcastTo(name, "user-joined", user, sid)


@sio.on('leave-room')
def leave(sid, room):
    room = json.loads(room)
    user = room.get('userId')
    name = room.get('roomName')
    print("leave-room, user: %s, room: %s\n" % (user, name))
    sio.leave_room(sid, name)
    rooms.pop(sid)
    broadcastTo(name, "user-left", user, sid)


@sio.event
def broadcast(sid, msg):
    print('broadcast', sid)
    room = rooms.get(sid)
    broadcastTo(room, "broadcast", msg, sid)


@sio.event
def disconnect(sid):
    print('Disconnected', sid)


@sio.event
def error(sid, err):
    print('error', err)


@sio.event
def data(sid, data):
    print('Message from {}: {}'.format(sid, data))
    sio.emit('data', data, room=ROOM, skip_sid=sid)


if __name__ == '__main__':
    # app.run('0.0.0.0', 5001 )
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 5001)), app)
