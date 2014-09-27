#!flask/bin/python
import os
import unittest

from flask import session
from sarpi import sarpi, db
from sarpi.models import Pet, PetWeight, Schedule, Owner
from config import basedir

class SarpiClientTestCase(unittest.TestCase):

    def setUp(self):
        sarpi.config['TESTING'] = True
        sarpi.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
        sarpi.config['CSRF_ENABLED'] = False
        sarpi.config['WTF_CSRF_ENABLED'] = False

        self.app_context = sarpi.app_context()
        self.app_context.push()
        db.create_all()

        self.client = sarpi.test_client()
        self.db = db

        self.owner = Owner(username = 'testname', password = 'default', name = 'TestCase', email = 'test@example.com')
        self.db.session.add(self.owner)
        self.db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        """Redirecting to /login ya que no esta logeado aun"""
        response = self.client.get('/index')
        self.assertTrue(b'Redirecting...' in response.data)

    # Funciones para probar el login
    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    #Prueba del login
    def test_login_success_message(self):
        """Exitoso login, se verifica con el mensage de Loggen en el home"""
        response = self.login('testname', 'default')
        self.assertTrue(b'Logged in successfully.' in response.data)

    def test_login_wrong(self):
        """Fallo el login, ya que la clave o usuario esta mala/no existe"""
        response = self.login('testname', 'nopassword')
        self.assertTrue(b'no existe' in response.data)

    def test_logout_success(self):
        """Un exitoso logout deberia remover el owner de la session y redirije al usuario al page de login"""
        with self.client as c:
            self.login('testname', 'default')
            response = self.logout()
            self.assertTrue('username' not in session)
            self.assertTrue(b'SARpi - Sign In' in response.data)

