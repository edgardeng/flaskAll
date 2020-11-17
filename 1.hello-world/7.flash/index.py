from flask import Flask, flash, get_flashed_messages

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890'


@app.route('/')
def index():
    """
    闪现： 原理基于session

    :return:
    """
    flash('点击了主页')
    flash('点击了主页哦', category='x1')
    return '<h1>Hello World!</h1>'


@app.route('/c')
def count():
    data = get_flashed_messages() # 获取了全部
    return '<h1>Hello   %s</h1>' % data


@app.route('/c2')
def count2():
    data = get_flashed_messages(category_filter='x1') # 其他的也会删除
    return '<h1>Hello   %s</h1>' % data


if __name__ == '__main__':
    app.run(debug=True)
