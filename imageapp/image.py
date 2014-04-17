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

def add_image(filename, data, user):
#    if images:
#        image_num = max(images.keys()) + 1
#    else:
#        image_num = 0
        
#    images[image_num] = data
#    return image_num

#def get_image(num):
#    return images[num]
    conn = sqlite3.connect('images.sqlite')
    c = conn.cursor()
    image = Image(filename, data)
    conn.text_factory = bytes
    t = (image, user)
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

def get_latest_image():
    image_num = max(images.keys())
    return images[image_num]
