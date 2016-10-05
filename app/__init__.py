import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_wtf.csrf import CsrfProtect
from raven.contrib.flask import Sentry

# App
app = Flask(__name__)
app.config.from_object('app.config')

# Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

# Login
lm = LoginManager()
lm.init_app(app)

# Forms
CsrfProtect(app)

# Sentry
sentry = Sentry(app, dsn='http://c18a9e8fafe3457fada05ea16b9494c1:4cdfd4140ad641699222f8eaede781b0@45.79.160.130:9001/5')

from app import models, views