#!/usr/bin/env python
import random
import socket
import time
import urlparse



#global header
header = 'HTTP/1.0 200 OK\r\n' + \
         'Content-type: text/html\r\n' + \
         '\r\n'

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
        
def handle_connection(conn):
    # Receiving the data to be processed
    request = conn.recv(1000)
    

        
    if len(request):
        f_line = request.splitlines()[0].split(' ')
        method = f_line[0]
        url = urlparse.urlparse(f_line[1])
        loc = url[2]
        if method == 'POST':
            if loc == '/submit':
                handle_submit(conn, request.split('\r\n')[-1])
            else:
                handle_post(conn, '')
        else:
            if loc == '/':
                handle_index(conn, '')
            elif loc == '/content':
                handle_content(conn, '')
            elif loc == '/file':
                handle_file(conn, '')
            elif loc == '/image':
                handle_image(conn, '')
            elif loc == '/form':
                handle_form(conn, '')
            elif loc == '/submit':
                handle_submit(conn, url[4])
    else:
        handle_error(conn)

    conn.close()

def handle_index(c, params):
    c.send(header + \
           '<h1>/home</h1>' + \
           '<ul>' + \
           '<li><a href="./content">content</a></li>' + \
           '<li><a href="./file">file</a></li>' + \
           '<li><a href="./image">image</a></li>' + \
           '<li><a href="./form">form</a></li>' + \
           '</ul>')


def handle_content(c, params):
    
    c.send(header + '<h1>/content<\h1>')


def handle_file(c, params):
    
    c.send(header + '<h1>/file<\h1>')


def handle_image(c, params):
    
    c.send(header + '<h1>/image<\h1>')


def handle_form(c, params):
    c.send(header + '<h1>/form</h1>' + \
           "<form action='submit' method='GET'>" + \
           "first name: <input type='text' name='firstname'></br>" + \
           "last name: <input type='text' name='lastname'></br>" + \
           "<input type='submit' value=Submit'></br>" + \
           "</form>")

def handle_error(c):
    message = 'Something bad happend. Call IT....'
    c.send(header + \
           message)


def handle_post(c, params):
    conn.send(header + '<h1>handling post</h1>')

def handle_submit(c, params):
    q = params.split('&')
    firstname = q[0].split('=')[1]
    lastname = q[1].split('=')[1]
    c.send(header + "<p>Hello Mr. %s %s.<\p>" % (firstname, lastname))


if __name__ == '__main__':
    main()
