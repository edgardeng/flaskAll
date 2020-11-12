"""
use werkzeug to build a wsgi server

"""
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple


def hello(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    path = environ['PATH_INFO'][1:] or 'hello'
    return [b'<h1> %s </h1>' % path.encode()]

# @Request.application
# def hello(request):
#     return Response('Hello World')


if __name__ == '__main__':
    run_simple('localhost', 5001, hello)
