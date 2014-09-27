#!flask/bin/python
import unittest

# Modulo para lanzar los tests creados en la carpeta de tests
if __name__ == '__main__':
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)