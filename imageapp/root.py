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
        for row in c.execute('SELECT * FROM imageapp1 WHERE username=? AND password=?', t):
            if(row[0] == request.form['username']) & (row[1] == request.form['password']):
                request.response.set_cookie('User', row[0])
                conn.close()
                return "<p>Login successful! :) <a href='/'> return to index</a></p>"
        conn.close()

        return "<p>Loging unsuccessful! <a href='/'> return to index</a></p>"

    @export(name='register')
    def register(self):
        request = quixote.get_request()
        if request.form['password'] == request.form['confirm']:
            conn = sqlite3.connect('images.sqlite')
            c = conn.cursor()

            conn.text_factory = str

            s = "INSERT INTO imageapp1 VALUES ('%s', '%s', 'NULL')" % (request.form['username'], request.form['password'])

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
        response.set_content_type('image/png')
        user = quixote.get_cookie("User")
        img = image.get_image(user)
        return img

    @export(name='get_comments')
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

        def retrieve_image(request):
            try:
                img = image.get_image(int(request.form['num']))
            except:
                img = image.get_latest_image()

            return img
