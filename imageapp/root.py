import quixote
from quixote.directory import Directory, export, subdir

from . import html, image
from quixote.util import StaticFile
import os.path
import sqlite3


class RootDirectory(Directory):
    _q_exports = []


    @export(name='')                    # this makes it public.
    def index(self):
        print "User: %s"%(quixote.get_cookie('User'))
        return html.render('index.html')

    @export(name='jquery')
    def jquery(self):
        return open('jquery-1.11.0.min.js').read()

    @export(name='css')
    def css(self):
        response = quixote.get_response()
        response.set_content_type('text/css')
        return html.load_file('style.css')

    @export(name='recent_image')
    def recent_image(self):
        return html.render('recent_image.html')

    @export(name='image_count')
    def image_count(self):
        return image.get_num_images()

    #CSS image loading
    '''
    @export(name='header_bg.jpg'):
        data = html.get_image('header_bg.jpg')
        return data


    @export(name='header2_bg.jpg'):
        data = html.get_image('header2_bg.jpg')
        return data


    @export(name='header.jpg'):
        data = html.get_image('header.jpg')
        return data


    @export(name='content_Bg.jpg'):
        data = html.get_image('content_Bg.jpg')
        return data


    @export(name='border_shadow_r.jpg'):
        data = html.get_image('border_shadow_r.jpg')
        return data


    @export(name='border_shadow_l.jpg'):
        data = html.get_image('border_shadow_l.jpg')
        return data


    @export(name='border.jpg'):
        data = html.get_image('border.jpg')
        return data

    @export(name='bg_content.jpg'):
        data = html.get_image('bg_content.jpg')
        return data

    
'''
    ###########################


    @export(name='login')
    def login(self):
        return html.render('login.html')

    @export(name='do_login')
    def do_login(self):
        request = quixote.get_request()
        print "User: %s Password: %s\n\n"%(request.form['username'], request.form['password'])
        
        conn = sqlite3.connect('images.sqlite')
        c = conn.cursor()

        conn.text_factory = str

        t = (request.form['username'], request.form['password'])
        for row in c.execute('SELECT * FROM users WHERE username=? AND password=?', t):
            if(row[1] == request.form['username']) & (row[2] == request.form['password']):
                request.response.set_cookie('User', row[1])
                conn.close()
                return "<p>Login successful! :) <a href='/'> return to index</a></p>"
        conn.close()

        return "<p>Loging in unsuccessful! <a href='/'> return to index</a></p>"


    @export(name='register')
    def register(self):
        request = quixote.get_request()
        if request.form['password'] == request.form['confirm']:
            conn = sqlite3.connect('images.sqlite')
            c = conn.cursor()

            conn.text_factory = str



            s = "INSERT INTO users VALUES (NULL, '%s', '%s')" % (request.form['username'], request.form['password'])
            
            c.execute(s)
            
            conn.commit()
            conn.close()

            request.response.set_cookie('User', request.form['username'])
            
            return "<p>Account successfully created!<a href='/'> return to index</a></p>"
        else:
            return "<p>Account creation was unsuccessful <a href='/'> return to index</a></p>"

    @export(name='logout')
    def logout(self):
        quixote.get_response().expire_cookie('User', path='/')
        return quixote.redirect("/")


    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        #print dir(the_file)
        #print 'received file with name:', the_file.base_filename
        data = the_file.fp.read()
         
        #image.add_image(data)
        image.add_image(the_file.base_filename, data, quixote.get_cookie("User") )

        the_file.close()
        return quixote.redirect('./')

    @export(name='upload_ajax')
    def upload_ajax(self):
        return html.render('upload_ajax.html')

    @export(name='upload_ajax_receive')
    def upload_ajax_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        #print dir(the_file)
        #print 'received file with name:', the_file.base_filename
        data = the_file.fp.read()

        #image.add_image(data)
        image.add_image(the_file.base_filename, data, quixote.get_cookie("User") )

        response = quixote.get_response()
        response.set_content_type('image/png')
        #return image.get_latest_image()
        user = quixote.get_cookie("User")
        return image.get_image(user)

    @export(name='image')
    def image(self):
        return html.render('image.html')

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        request = quixote.get_request()

        user = quixote.get_cookie("User")
        
        try:
            i = int(request.form['num'])
        except:
            i = -1

        img = image.get_image(user, i)

        filename = img.filename

        if filename.lower() in ('jpg', 'jpeg'):
            response.set_content_type('image/jpeg')
        elif filename.lower() in ('tif', 'tiff'):
            response.set_content_type('image/tiff')
        else:
            response.set_content_type('image/png')
        return img.data
        
    def get_comments(self):
        response = quixote.get_response()
        request = quixote.get_request()

        img = retrieve_image(request)

        all_comments = []
        for comment in img.get_comments():
            print comment
            all_comments.append("""\
                    <comment>
                    <text>%s</text>
                    </comment>
                    """ % (comment))


            xml = """
            <?xml version="1.0"?>
            <comments>
            %s
            </comments>
            """ % ("".join(all_comments))

            return xml

    @export(name='add_comment')
    def add_comment(self):
        response = quixote.get_response()
        request = quixote.get_request()

        img = retrieve_image(request)

        try:
            comment = request.form['comment']
        except:
            return

        img.add_comment(comment)

    @export(name='get_score')
    def get_socre(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            i = int(request.form['num'])
        except:
            i = -1
        print "This is i: " + i
        return image.get_image_score(i)

    @export(name='increment_score')
    def increment_score(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            i = int(request.form['num'])
        except:
            i = -1

        return image.increment_image_score(i)

    @export(name='decrement_score')
    def decrement_score(self):
        response = quixote.get_response()
        request = quixote.get_request()

        try:
            i = int(request.form['num'])
        except:
            i = -1

        return image.decrement_image_score(i)
