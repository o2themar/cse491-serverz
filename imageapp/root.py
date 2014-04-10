import quixote
from quixote.directory import Directory, export, subdir

from . import html, image


#Change later to using SQLite
global users
users = dict()


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

        if request.form['username'] in users.keys():
            if users[request.form['username']] == request.form['password']:
                print "request.form['username'] = %s"%(request.form['username'])
                request.response.set_cookie('User', request.form['username'])
                return "<p>Login successful! :) <a href='/'> return to index</a></p>"
        return "<p>Loging unsuccessful! <a href='/'> return to index</a></p>"

    @export(name='register')
    def register(self):
        request = quixote.get_request()
        if request.form['password'] == request.form['confirm']:
            users[request.form['username']] = request.form['password']
            
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
        image.add_image(data, quixote.get_cookie("User") )

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
        image.add_image(data, quixote.get_cookie("User") )

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
        img = image.get_latest_image()
        return img
