# __init__.py is the top level file in a Python package.
import os
import sqlite3
from quixote.publish import Publisher
import quixote

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image

IMAGE_DB_FILE = 'images.sqlite'

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 
def setup():                            # stuff that should be run once.
    html.init_templates()
     
    if not os.path.exists(IMAGE_DB_FILE):
        create_database()

    some_data = open('imageapp/dice.png', 'rb').read()
    image.add_image('imageapp/dice.png', some_data, None)



def create_database():
    print 'creating database'
    db = sqlite3.connect('images.sqlite')
    c = db.cursor()
    c.execute('CREATE TABLE users (i INTEGER PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))')
    c.execute('CREATE TABLE imageapp1 (i INTEGER PRIMARY KEY, userId INTEGER, filename VARCHAR(255), score INTGER, picture BLOB, FOREIGN KEY (userId) REFERENCES users(i))')
    c.execute('CREATE TABLE image_comments (i INTEGER PRIMARY KEY, imageId INTEGER, comment TEXT, FOREIGN KEY (imageId) REFERENCES imageapp1(i))')
    db.commit()
    db.close()

def rerieve_all_images():
    db = sqlite3.connect('images.sqlite')

    db.text_factory = bytes

    c = db.cursor()

    for row in c.execute('SELECT * FROM imageapp1 ORDER BY i DESC'):
        open(row[1], 'w').write(row[2])

def teardown():                         # stuff that should be run once.
    pass

def retrieve_all_images():
    db = sqlite3.connect('images.sqlite')

    db.text_factor = bytes

    c = db.cursor()

    for row in c.execute('SELECT * FROM imageapp1 ORDER BY i DESC'):
        open(row[1], 'w').write(row[2])

