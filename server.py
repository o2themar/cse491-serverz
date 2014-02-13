#!/usr/bin/env python
import random
import socket
import time

from wsgiref.simple_server import make_server

from app import make_app

def main():
    the_wsgi_app = make_app()

    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    httpd = make_server('', port, the_wsgi_app)
    print "Serving at http://%s:%d/..." % (host, port,)
    httpd.serve_forever()

if __name__ == "__main__":
    main()

