#!/user/bin/env python
import random
import argparse
import socket
import time
import sys
import Cookie
import imageapp
import quixote
import quixote.demo.altdemo


#from quixote.demo.altdemo import create_publisher
from urlparse import urlparse
from StringIO import StringIO

from app import make_app
from wsgiref.validate import validator

def handle_connection(conn, application):
    # Start reading in data from the connection
    req = conn.recv(1)
    count = 0
    env = {}
    while req[-4:] != '\r\n\r\n':
        req += conn.recv(1)

    # Parse the headers we've received
    req, data = req.split('\r\n', 1)
    headers = {}
    for line in data.split('\r\n')[:-2]:
        k, v = line.split(': ', 1)
        headers[k.lower()] = v

    # Parse out the path and related info
    path = urlparse(req.split(' ', 3)[1])
    env['REQUEST_METHOD'] = 'GET'
    env['PATH_INFO'] = path[2]
    env['QUERY_STRING'] = path[4]
    env['CONTENT_TYPE'] = 'text/html'
    env['CONTENT_LENGTH'] = '0'
    env['SCRIPT_NAME'] = ''
    env['SERVER_NAME'] = 'Omar\'s server'
    env['SERVER_PORT'] = conn.getsockname()[0]
    env['wsgi.version'] = (1, 0)
    env['wsgi.errors'] = sys.stderr
    env['wsgi.multithread'] = False
    env['wsgi.multiprocess'] = False
    env['wsgi.run_once'] = False
    env['wsgi.url_scheme'] = 'http'
    env['HTTP_COOKIE'] = headers['cookie']

    def start_response(status, response_headers):
        conn.send('HTTP/1.0')
        conn.send(status)
        conn.send('\r\n')
        for pair in response_headers:
            key, header = pair
            conn.send(key + ': ' + header + '\r\n')
        conn.send('\r\n')

    content = ''
    if req.startswith('POST '):
            env['REQUEST_METHOD'] = 'POST'
            env['CONTENT_LENGTH'] = headers['content-length']
            env['CONTENT_TYPE'] = headers['content-type']
            print headers['content-length']

            while len(content) < int(headers['content-length']):
                content += conn.recv(1)

    env['wsgi.input'] = StringIO(content)
    #validator_app = validator(appl)
    result = application(env, start_response)
    for data in result:
        conn.send(data)

    conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-A", help="What application to run")
    parser.add_argument("-p", help="What port to use", type=int)
    args = parser.parse_args()

    if not args.A:
        print "Plese specify an app with -A"
        return -1
    if args.p:
        port = args.p
    else:
        port = random.randint(8000, 9999)

    if args.A == "image":
        imageapp.setup()
        p = imageapp.create_publisher()
        wsgi_app = quixote.get_wsgi_app()
    elif args.A == "altdemo":
        p = quixote.demo.altdemo.create_publisher()
        wsgi_app = quixote.get_wsgi_app()
    elif args.A == "myapp":
        wsgi_app = make_app()
    else:
        print "App not found"
        return -1

    s = socket.socket()      # Create a socket object
    host = socket.getfqdn()  # Get Local machine name
    s.bind((host, port))     # Bind to the port


    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5) # Now wait for client connection.


    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client,
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port

        handle_connection(c, wsgi_app)

if __name__ == '__main__':
    main()

