import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
# Se usan para el login
from flask.ext.login import LoginManager
# from flask.ext.mail import Mail
from config import basedir

# Crea un objeto de clase Flask
sarpi = Flask(__name__)

#Para que la sarpi lea el archivo de confifuracion
sarpi.config.from_object('config')

#Base de datos
db = SQLAlchemy(sarpi)

# Flask-Login
lm = LoginManager()
lm.init_app(sarpi)
lm.session_protection = 'strong'
lm.login_view = 'login'

# archivo de error cuando sarpi no esta en modo debug
if not sarpi.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/sarpi.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    sarpi.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    sarpi.logger.addHandler(file_handler)
    sarpi.logger.info('SARpi')

from sarpi import views, models