# image handling API
import sqlite3

class Image:
    filename = ''
    data =''
    comments = []
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data
        self.comments =[]

    def add_comment(self, comment):
        self.comments.append(comment)

    def get_comments(self):
        return self.comments


images = {}

def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""
    SELECT COUNT(*)
    FROM sqlite_master
    WHERE name = ?
    """, (tablename, ))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True

    dbcur.close()
    return False

def add_image(filename, data, user):
    conn = sqlite3.connect('images.sqlite')
    c = conn.cursor()
    conn.text_factory = bytes
    t = (data, user)
    c.execute("UPDATE imageapp1 SET picture=? WHERE username=?", t)

    conn.commit()
    conn.close()


def get_image(user):
    conn = sqlite3.connect('images.sqlite')
    c = conn.cursor()

    conn.text_factory = str

    t = (user,)
    c.execute('SELECT picture FROM imageapp1 WHERE username=?', t)

    conn.text_factory = bytes

    image = c.fetchone()[0]

    conn.close()

    return image

def get_latest_image(user):
   # image_num = max(images.keys())
    conn = sqlite3.connect('images.sqlite')
    print 'This is the user: '+ user
    c = conn.cursor()
    conn.text_factory = str
    
    t = (user,) 
    c.execute('SELECT picture FROM imageapp1 WHERE username=?', t)

    conn.text_factory = bytes
    image = c.fetchone()[0]
    conn.close()
    return image
