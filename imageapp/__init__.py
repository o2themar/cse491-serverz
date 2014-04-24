# __init__.py is the top level file in a Python package.
import os
import sqlite3
from quixote.publish import Publisher

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
    c.execute('CREATE TABLE imageapp1 (username TEXT, password TEXT, picture BLOB, comment TEXT)')
    db.commit()
    db.close()


def teardown():                         # stuff that should be run once.
    pass
