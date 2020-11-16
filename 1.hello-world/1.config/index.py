"""
不管你使用何种方式载入配置，都可以使用 Flask 对象的 config 属性来操作配置的值。
config 实质上是一个字典的子类，可以像字典一样操作
"""
from flask import Flask

app = Flask(__name__)

# config 配置方式一, 直接配置：
# app.config['TESTING'] = True
# app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
# app.config['ENV'] = 'development'

# config 配置方式二, 使用object：

app.config.from_object('config.Config')


@app.route('/')
def index():
    print('DEBUG:', app.config['DEBUG'])
    print('ENV:', app.config['ENV'])
    print('SECRET_KEY:', app.config['SECRET_KEY'])

    return '<h1>Hello World!</h1>'


if __name__ == '__main__':
    app.run()
