"""
pip install Flask-SocketIO -i https://mirrors.aliyun.com/pypi/simple (Flask-SocketIO-5.1.1 )

"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.event
def my_event(message):
    print('my_event', message)
    emit('my_response', {'data': 'got it!'})


if __name__ == '__main__':
    socketio.run(app, '0.0.0.0', 5002, debug=True)
