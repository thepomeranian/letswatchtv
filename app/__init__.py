import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_wtf.csrf import CsrfProtect

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

from app import models, views