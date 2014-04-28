# image handling API
import sqlite3
import sys


class Image:
    filename = ''
    data =''
    score = 0

    def __init__(self, filename, data, score):
        self.filename = filename
        self.data = data
        self.score = score



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
    insert_image(filename, data, user)

def get_image(user, num):
    return retrieve_image(user, num)

def get_latest_image(user):
    return retrieve_image(user, -1)

def insert_image(filename, data, userId):
    db = sqlite3.connect('images.sqlite')

    db.text_factory = bytes

    db.execute('INSERT INTO imageapp1 (userId, filename, score, picture) VALUES (?, ?, ?, ?)', (userId, filename, 1, data))

    db.commit()


def retrieve_image(user, num):
    db = sqlite3.connect('images.sqlite')

    db.text_factory = bytes

    c = db.cursor()

    if num >= 0:
        c.execute('SELECT i, filename, score, picture FROM imageapp1 WHERE i=(?) AND userId=(?)', (num,user))
    else:
        c.execute('SELECT i, filename, score, picture FROM imageapp1 ORDER BY i DESC LIMIT 1')

    try:
        user, filename, score, image = c.fetchone()

        return Image(filename, image, score)
    except:
        pass

def add_comment(i, comment):
    db = sqlite3.connect('images.sqlite')

    if i == -1:
        c = db.cursor()

        c.execute('SELECT i FROM imageapp1 ORDER BY i DESC LIMIT 1')
        try:
            i = c.fetchone()[0]
        except:
            return

    db.execute('INSERT INTO image_comments (imageId, comment) VALUES (?, ?)', (i, comment))
    db.commit()
    return i

def get_comments(i):
    comments = []
    db = sqlite3.connect('images.sqlite')

    c = db.cursor()
    if i == -1:
        c.execute('SELECT i FROM imageapp1 ORDER BY i DESC LIMIT 1')
        try:
            i = c.fetchone()[0]
        except:
            return

    c.execute('SELECT i, comment FROM image_comments WHERE imageId=(?) ORDER BY i DESC', (i,))
    for row in c:
        comments.append(row[1])

    return comments


def get_image_score(i):
    db = sqlite3.connect('images.sqlite')

    c = db.cursor()

    if i >= 0:
        c.execute('SELECT score FROM imageapp1 WHERE i=(?)', (i,))
    else:
        c.execute('SELECT score FROM imageapp1 ORDER BY i DESC LIMIT 1')


    val = int(c.fetchone()[0])
    print val
    return val



def increment_image_score(i):
    db = sqlite3.connect('images.sqlite')

    if i < 0:
        i = get_num_images()

    db.execute('UPDATE imageapp1 SET score = score + 1 WHERE i=(?)', (i,))
    db.commit()
    return int(i+1)

def decrement_image_score(i):
    db = sqlite3.connect('images.sqlite')

    if i < 0:
        i = get_num_images()

    db.execute('UPDATE imageapp1 SET score = score - 1 WHERE i=(?)', (i,))
    db.commit()
    return int(i-1)

def get_num_images():
    db =- sqlite3.connect('images.sqlite')
    c = db.cursor()
    c.execute('SELECT i FROM imageapp1 ORDER BY i DESC LIMIT 1')
    try:
        return int(c.fetchone()[0])
    except:
        return 0




