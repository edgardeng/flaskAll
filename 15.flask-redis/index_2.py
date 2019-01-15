from flask import Flask, render_template
from flask_caching import Cache
import random

app = Flask(__name__)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)
with app.app_context():
    cache.clear()
    # clear all


@app.route("/")
@cache.cached(timeout=30, key_prefix='view_%s')
def index():
    name = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 5))
    print(name)
    return render_template('index.html', name=name)


@app.route("/two")
@cache.cached(timeout=30, key_prefix='view_%s')
def two():
    name = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', 5))
    print(name)
    return render_template('index.html', name=name)


@app.route("/clear")
def clear():
    cache.delete_many('view_/', 'view_/two')  # 删除缓存
    return render_template('index.html', name='clear')


# @cache.cached(timeout=50, key_prefix='all_comments')
# def get_all_comments():
#     comments = do_serious_dbio() //
#     return [x.author for x in comments]


if __name__ == '__main__':
    app.run()
