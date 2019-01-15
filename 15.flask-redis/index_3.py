# example for redis& cache in flask
from flask import Flask, render_template
from flask_caching import Cache
import random

app = Flask(__name__)
redis_config = {
  'CACHE_TYPE': 'redis',
  'CACHE_REDIS_HOST': 'localhost',
  'CACHE_REDIS_PORT': 6379,
  'CACHE_REDIS_DB': '0',
  'CACHE_REDIS_PASSWORD': ''
}
cache = Cache(config=redis_config)
cache.init_app(app)
with app.app_context():
    cache.clear()


@app.route("/")
@cache.cached(timeout=20)
def index():
    name = get_random_name()
    return render_template('index.html', name=name)


@cache.memoize(timeout=30)
def get_random_name():
    name = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 6))
    return name


if __name__ == '__main__':
    app.run()
