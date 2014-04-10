# image handling API
import sqlite3

images = {}

def add_image(data, user):
#    if images:
#        image_num = max(images.keys()) + 1
#    else:
#        image_num = 0
        
#    images[image_num] = data
#    return image_num

#def get_image(num):
#    return images[num]
    con = sqlite3.connect('MBimageapp.db')
    c = conn.cursor()

    conn.text_factory = bytes
    t = (data, user)
    c.execute("UPDATE imageapp SET picture=? WHERE username=?", t)

    conn.commit()
    conn.close()


def get_image(user):
    conn = sqlite3.connect('MBimageapp.db')
    c = conn.cursor()

    conn.text_factory = str

    t = (user,)
    c.execute('SELECT picture FROM imageapp WHERE username=?', t)

    conn.text_factory = bytes

    image = c.fetchone()[0]

    conn.close()

    return image

def get_latest_image():
    image_num = max(images.keys())
    return images[image_num]
