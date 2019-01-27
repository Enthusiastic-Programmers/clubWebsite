from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
import join
import mimetypes

static_files = {'/about.html', '/contact.html', '/faq.html', '/index.html', '/join.html'}
def serve_file(environ, start_response):
    if environ['REQUEST_METHOD'] != "GET":
        yield from common.error_page(environ, start_response, "Bad request", code="405 Method Not Allowed")
        return
    try:
        with open('.' + environ['PATH_INFO'], 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        yield b'404 Not Found'
    else:
        start_response('200 OK', [('Content-Type', mimetypes.guess_type(environ['PATH_INFO'])[0] )])
        yield data

def application(environ, start_response):
    try:
        path = environ['PATH_INFO']
        if path == '/join':
            yield from join.application(environ, start_response)
        elif path in static_files or path.startswith('/stylesheets/') or path.startswith('/images/'):
            yield from serve_file(environ, start_response)
        else:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            yield b'404 Not Found'

    except Exception as e:
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')] )
        yield b'500 Internal Server Error'
        raise

server = WSGIServer(('127.0.0.1', 8080), application)
print('Started httpserver on port ' , 8080)
server.serve_forever()
