#!flask/bin/python
import os
import unittest

from flask import current_app
from sarpi import sarpi, db
from config import basedir

class BasicsTestCase(unittest.TestCase):
    """docstring for BasicsTestCase

    Se Comprueba que la app este creada y que este en modo de prueba(TESTING)

    """

    def setUp(self):
        sarpi.config['TESTING'] = True
        sarpi.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

        self.app_context = sarpi.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])