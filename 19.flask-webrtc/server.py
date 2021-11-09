from flask import Flask, render_template
import socketio
import eventlet.wsgi
sio = socketio.Server(cors_allowed_origins='*', ping_timeout=35)
app = Flask(__name__)
ROOM = 'ROOM'


@app.route('/')
def index():
    return render_template('index.html', room='default')


@sio.event
def connect(sid, environ):
    print('Connected', sid)
    sio.emit('ready', room=ROOM, skip_sid=sid)
    sio.enter_room(sid, ROOM)


@sio.event
def disconnect(sid):
    sio.leave_room(sid, ROOM)
    print('Disconnected', sid)


@sio.event
def data(sid, data):
    print('Message from {}: {}'.format(sid, data))
    sio.emit('data', data, room=ROOM, skip_sid=sid)


if __name__ == '__main__':
    # app.run('0.0.0.0', 5001 )
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 5001)), app)
