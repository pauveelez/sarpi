#!flask/bin/python
import os
import unittest

# from flask import session
from sarpi import sarpi, db
# from sarpi.models import Pet, PetWeight, Schedule, Owner
from config import basedir

class SarpiClientTestCase(unittest.TestCase):

    def setUp(self):
        sarpi.config['TESTING'] = True
        sarpi.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
        # sarpi.config['CSRF_ENABLED'] = False
        # sarpi.config['WTF_CSRF_ENABLED'] = False

        self.app_context = sarpi.app_context()
        self.app_context.push()
        db.create_all()

        self.client = sarpi.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_page_not_found(self):
        """Las paginas que no existen se redirigen a 404 template"""
        response = self.client.get('/a-page-which-doesnt-exist')
        self.assertTrue(b'Page Not Found' in response.data)

    def test_sign_in_page_loads(self):
        """La pagina de login carga perfecto"""
        response = self.client.get('/login')
        self.assertTrue(b'SARpi - Sign In' in response.data)