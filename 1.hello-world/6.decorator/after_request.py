from flask import Flask, before_render_template, render_template

app = Flask(__name__)

"""
before_request_funcs = [x1,x2]
"""


@app.before_first_request
def func_before_first_request():
    print('func_before_first_request') # 第一次请求


@app.errorhandler(404)
def not_found(error):
    print('not_found:', error)
    return '<h2>404</h2>'


@app.before_request
def view_before():
    print('view_before')
    return 'view_before return 不要烦我'  # 在before_request 返回了，直接走after_request_funcs 不走view func


@app.before_request
def view_before2():
    print('view_before2')


"""
after_request_funcs = [x1, x2]
读取时， after_request.reverse
"""


@app.after_request
def view_after(response):
    print('view_after', response)
    return response  # 必须接收response 并返回response


# TypeError: view_after() takes 0 positional arguments but 1 was given

@app.after_request
def view_after2(response):
    print('view_after2', response)
    return response


#
# @before_render_template
# def template_before():
#     print('view_before')


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/t')
def t():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
