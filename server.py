#!/usr/bin/env python
import random
import socket
import time
import sys
from urlparse import urlparse
from StringIO import StringIO

from app import make_app
from wsgiref.validate import validator


def handle_connection(conn):
    # Start reading in data from the connection
    req = conn.recv(1)
    count = 0
    env = {}
    while req[-4:] != '\r\n\r\n':
        req += conn.recv(1)

    # Parse the headers we've received
    req, data = req.split('\r\n',1)
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
    env['SERVER_NAME'] = 'Totally Cool Server'
    env['SERVER_PORT'] = conn.getsockname()[0]
    env['wsgi.version'] = (1, 0)
    env['wsgi.errors'] = sys.stderr
    env['wsgi.multithread'] = False
    env['wsgi.multiprocess'] = False
    env['wsgi.run_once'] = False
    env['wsgi.url_scheme'] = 'http'

    def start_response(status, response_headers):
    	conn.send('HTTP/1.0 ')
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
    appl = make_app()
    validator_app = validator(appl)
    result = appl(env, start_response)
    for data in result:
        conn.send(data)

    conn.close()

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.
    

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port

        handle_connection(c)

if __name__ == '__main__':
   main()



