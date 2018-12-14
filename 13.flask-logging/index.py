from flask import Flask, request
from logger import Logger

app = Flask(__name__)
log = Logger()


@app.before_request
def before_request():
    msg = request.remote_addr + ' ' + request.method + ' ' + request.url
    log.info(msg)  # log every request
    pass


@app.after_request
def after_request(response):
    msg = request.remote_addr + ' ' + request.method + ' ' + request.url + response.status
    log.info(msg)  # log every request
    return response


@app.route('/')
def index():
    log.debug("logging debug")
    log.info("logging info")
    log.error("logging error")
    return '<h1>Hello World!</h1>'


@app.route('/user')
def user():
    return '<h1>Hello My User!</h1>'


if __name__ == '__main__':
    app.run(debug=True)
