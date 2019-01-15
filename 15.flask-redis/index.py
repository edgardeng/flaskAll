# example for redis in flask
from flask import Flask
from redis import Redis

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

redis = Redis(host='localhost', port=6379, db=0)
if not redis.get('openCount'):
    redis.set('openCount', 0)


@app.route('/')
def index():
    redis.incr('openCount')
    count = str(redis.get('openCount'), encoding='utf-8')
    return '<h2>网页被打开 第 ' + count + '次 </h2>'


if __name__ == '__main__':
    app.run()
