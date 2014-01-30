#!/usr/bin/env python
import random
import socket
import time
import urlparse

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
    request_line = request.split('\r\n')[0].split(' ')
    
    http_method = request_line[0]
    
    parsed_url = urlparse.urlparse(request_line[1])
    path = parsed_url[2]
    
    # Message responses
    response_main_message = 'HTTP/1.0 200 OK\t\n' + \
                            'Content-type: text/html\r\n' + \
                            '\r\n' + \
                            '<html><body>' + \
                            '<h1>Hello, world.</h1>' + \
                            'This is aliomar\'s Web server.' + \
                            '<br/><a href="/content">Content</a>' + \
                            '<br/><a href="/file">File</a>' + \
                            '<br/><a href="/image">Image</a>' + \
                            '</body></html>'

    responose_content = 'HTTP/1.0 200 OK\r\n' + \
                        'Content-type: text/html\r\n' + \
                        '\r\n' + \
                        '<html><body><h1>Content</h1>This is aliomar\'s Web server.</body></html>'

    response_file = 'HTTP/1.0 200 OK\r\n' + \
                    'Content-type: text/html\r\n' + \
                    '\r\n' + \
                    '<html><body><h1>File</h1>This is aliomar\'s Web server.</body></html>'

    response_image = 'HTTP/1.0 200 OK\r\n' + \
                     'Content-type: text/html\r\n' + \
                     '\r\n' + \
                     '<html><body><h1>Image</h1>This is aliomar\'s Web server.</body></html>'

    # Separating the links for main page into links for content files and images.
    if http_method == 'POST':

        if path == '/':
        
            handle_index(conn,'')
    
        elif path == '/submit':
        
            handle_submit(conn,request.split('\r\n')[-1])
            
            
    else:
        if path == '/':
            handle_index(conn,'')

        elif path == '/content':
                    
            handle_content(conn,'')
                
        elif path == '/file':
                    
            handle_file(conn,'')
                
        elif path == '/image':
                    
            handle_image(conn,'')
                
        elif path == '/submit':
                    
            handle_submit(conn, parsed_url[4])

        else:
            
            handle_error(conn)

    conn.close()

def handle_index(c, params):
    
    c.send('HTTP/1.0 200 OK\r\n' + \
           'Content-type: text/html\r\n' + \
           '\r\n' + \
           '<h1>Hello, world.</h1>' + \
           'This is aliomar\'s Web server.<br>' + \
           '<a href= /content>Content</a><br>' + \
           '<a href= /file>File</a><br>' + \
           '<a href= /image>Image</a><br>' + \
           'GET Form' + \
           '<form action="/submit" method="GET">\n' + \
           '<p>First Name: <input type="text" name="firstname"></p>\n' + \
           '<p>Last Name: <input type="text" name="lastname"></p>\n' + \
           '<input type="submit" value="Submit">\n\n' + \
           '</form>' + \
           'POST Form' + \
           '<form action="/submit" method="POST">\n' + \
           '<p>First Name: <input type="text" name="firstname"></p>\n' + \
           '<p>Last Name: <input type="text" name="lastname"></p>\n' + \
           '<input type="submit" value="Submit">\n\n' + \
           '</form>')


def handle_content(c, params):
    
    c.send('HTTP/1.0 200 OK\r\n' + \
           'Content-type: text/html\r\n' + \
           '\r\n' + \
           '<h1>Content page</h1>' + \
           'words words words')


def handle_file(c, params):
    
    c.send('HTTP/1.0 200 OK\r\n' + \
           'Content-type: text/html\r\n' + \
           '\r\n' + \
           '<h1>File page</h1>' + \
           'cabinet')


def handle_image(c, params):
    
    c.send('HTTP/1.0 200 OK\r\n' + \
           'Content-type: text/html\r\n' + \
           '\r\n' + \
           '<h1>Image page</h1>' + \
           'imagine that')


def handle_submit(c, params):
    
    namestring = params.split('&')
    
    first_name = namestring[0].split('=')[1]
    last_name = namestring[1].split('=')[1]
    
    c.send('HTTP/1.0 200 OK\r\n' + \
           'Content-type: text/html\r\n' + \
           '\r\n' + \
           'Hello Mr. %s %s.' % (first_name, last_name))

def handle_error(c):
    message = 'Something bad happend. Call IT....'
    c.send('HTTP/1.0 200 OK\r\n' + \
           'Content-type: text/html\r\n' + \
           '\r\n' + \
           message)

if __name__ == '__main__':
    main()
