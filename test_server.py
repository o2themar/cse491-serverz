from app import make_app
from webtest import TestApp
from StringIO import StringIO

test_app = TestApp(make_app())


class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r

        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

# Test a basic GET call.

def test_root():
    resp = test_app.get('/')
    assert resp.status == '200 OK'

def test_content():
    resp = test_app.get('/content')
    assert resp.status == '200 OK'

def test_image():
    resp = test_app.get('/image')
    assert resp.status == '200 OK'

def test_file():
    resp = test_app.get('/file')
    assert resp.status == '200 OK'

def test_GET_submit():
    resp = test_app.get('/submit?firstname=Omar&lastname=Ali')
    assert resp.status == '200 OK'
    assert 'Omar Ali' in resp


def test_POST_submit():
    resp = test_app.get('/form')
    print resp
    form = resp.form
    print form
    form['firstname'] = 'Omar'
    form['lastname'] = 'Ali'
    resp2 = form.submit('submit')
    assert resp2.status == '200 OK'
    assert 'Omar Ali' in resp2

def test_404():
    resp = test_app.get('/thislinkisgood',status=404)
    assert resp.status_int == 404
