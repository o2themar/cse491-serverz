#!/usr/bin/env python
import random
import socket
import time

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
    # Display content
    print c.recv(1000)
    c.send('HTTP/1.0 200 OK\r\n')
    c.send("Content-Type: text/html\r\n\r\n")
    c.send('<html><body><h1>Hello, world</h1> this is aliomar''s Web server</body></html>')
    c.close()
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
    data = conn.recv(1000)
    getPost = data.split(' ')[0]
    path = data.split(' ')[1]
    
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
    if getPost == 'POST':
        conn.send("Hello world!")
        conn.close()
        return

    elif path == '/':
        conn.send(response_main_message)
    elif path == '/content':
        conn.send(responose_content)
    elif path == '/file':
        conn.send(response_image)
    elif path == '/image':
        conn.send(response_image)
    else:
        conn.send('<h2>This page does not exist!</h2>')

    conn.close()

if __name__ == '__main__':
    main()
