import unittest
from flask_go_to import install_forwarder
from flask import Flask, Response


class GoToTestCase(unittest.TestCase):

    def test_simple_redirect(self):

        app = Flask(__name__)

        rule = '/temp/'
        map = {'google': 'http://google.com'}
        default_url = 'http://default.com'
        install_forwarder(app, rule, path_mapper=map.get, default_url=default_url)
        app = app.test_client()
        rv = app.get('/temp/google', follow_redirects=False)

        self.assertEquals(rv.status_code, 302)
        self.assertEquals(rv.headers.get('Location'), 'http://google.com')

    def test_simple_redirect_no_end_slash(self):

        app = Flask(__name__)

        rule = '/temp'
        map = {'google': 'http://google.com'}
        default_url = 'http://default.com'
        install_forwarder(app, rule, path_mapper=map.get, default_url=default_url)
        app = app.test_client()
        rv = app.get('/temp/google', follow_redirects=False)

        self.assertEquals(rv.status_code, 302)
        self.assertEquals(rv.headers.get('Location'), 'http://google.com')

    def test_simple_redirect_empty_rule(self):

        app = Flask(__name__)

        rule = None
        map = {'google': 'http://google.com'}
        default_url = 'http://default.com'
        install_forwarder(app, rule, path_mapper=map.get, default_url=default_url)
        app = app.test_client()
        rv = app.get('/google', follow_redirects=False)

        self.assertEquals(rv.status_code, 302)
        self.assertEquals(rv.headers.get('Location'), 'http://google.com')

    def test_default_redirect(self):

        app = Flask(__name__)

        rule = '/temp/'
        map = {'google': 'http://google.com'}
        default_url = 'http://default.com'
        install_forwarder(app, rule, path_mapper=map.get, default_url=default_url)
        app = app.test_client()
        rv = app.get('/temp/doesnotexist', follow_redirects=False)

        self.assertEquals(rv.status_code, 302)
        self.assertEquals(rv.headers.get('Location'), 'http://default.com')

    def test_default_redirect_unspecified_default(self):

        app = Flask(__name__)

        rule = '/temp/'
        map = {'google': 'http://google.com'}
        install_forwarder(app, rule, path_mapper=map.get)
        app = app.test_client()
        rv = app.get('/temp/doesnotexist', follow_redirects=False)

        self.assertEquals(rv.status_code, 302)
        self.assertEquals(rv.headers.get('Location'), 'http://localhost/temp/')