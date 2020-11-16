"""
路由原理 与 路由设置

"""
from flask import Flask, url_for

app = Flask(__name__)


# 路由设置方式一， 使用装饰器
@app.route('/', methods=['GET'], endpoint='index')
def index():
    """
    1. route装饰器 本质是调用了Flask对象的add_url_rule函数
    2. def add_url_rule(self, rule, endpoint=None, view_func=None, **options)，主要做了以下4件事情：
        1) endpoint默认取view函数名称
        2) 提供默认的 http方法（HEAD, OPTION）
        3) 创建url_rule_class对象（url_rule_class默认为werkzeug.routing.Rule类, 路由关系），并添加到url_map中（werkzeug.routing.Map对象，视图映射）
        4) 将endpoint和view_func保存到view_functions字典中
    3. @app.route和app.add_url_rule参数：
        1) rule,                       URL规则
        2) view_func,                  视图函数名称
        3) defaults=None,              默认值,当URL中无参数，函数需要参数时，使用defaults={'k':'v'}为函数提供参数
        4) endpoint=None,              名称，用于反向生成URL，即： url_for('名称')
        5) methods=None,               允许的请求方式，如：["GET","POST"]
        6) strict_slashes=None,        对URL最后的 / 符号是否严格要求，(=False 访问 ~/index/ 或 ~/index均可)
        7) redirect_to=None,           重定向到指定地址
        8) subdomain=None,             子域名访问
    :return:
    """
    print(url_for('index'))  # 反向生成 url_for 返回 endpoint 对应的url
    return '<h1>Hello World!</h1>'


def other():
    return '<h1>other!</h1>'


# 路由设置方式二：使用add_url_rule函数
app.add_url_rule('/other', view_func=other)

"""

"""





if __name__ == '__main__':
    app.run()



"""
@app.route('/user/<username>')
@app.route('/post/<int:post_id>')
@app.route('/post/<float:post_id>')
@app.route('/post/<path:path>')
@app.route('/login', methods=['GET', 'POST'])

常用路由系统有以上五种，所有的路由系统都是基于一下对应关系来处理：
 
DEFAULT_CONVERTERS = {
    'default':          UnicodeConverter,
    'string':           UnicodeConverter,
    'any':              AnyConverter,
    'path':             PathConverter,
    'int':              IntegerConverter,
    'float':            FloatConverter,
    'uuid':             UUIDConverter,
}
"""

@app.route('/user/<username>')
def user(username):
    return f'<h1> {username}! </h1>'


if __name__ == '__main__':
    app.run(debug=True)
