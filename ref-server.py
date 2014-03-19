#! /usr/bin/env python
import socket
import random

# here is the code needed to create a WSGI application interface to
# a Quixote app:

from wsgiref.simple_server import make_server

from refapp import make_app

the_wsgi_app = make_app()



host = socket.getfqdn() # Get local machine name
port = random.randint(8000, 9999)
p.is_thread_safe = True # hack...
httpd = make_server('', port, wsgi_app)
print "Serving at http://%s:%d/..." % (host, port,)
httpd.serve_forever()
