"""
CBV
"""
from flask import Flask, url_for, views

app = Flask(__name__)


class IndexView(views.View):
    methods = ['GET']
    decorators = []  # 装饰器

    def dispatch_request(self):
        print('Index')
        return 'Index'


class IndexView2(views.MethodView):
    methods = ['GET', 'POST']
    decorators = []  # 装饰器作用到所有的视图函数

    def get(self):
        print('getIndex')
        return 'getIndex'

    def post(self):
        print('postIndex')
        return 'postIndex'


app.add_url_rule('/', view_func=IndexView.as_view(name='index'))  # name = endpoint
app.add_url_rule('/a', view_func=IndexView2.as_view(name='a'))

if __name__ == '__main__':
    app.run()
