import os

DEBUG = True
CSRF_ENABLED = True
CSRF_SESSION_KEY = "somethingimpossibletoguess" #needs new value
SECRET_KEY = 'yeah, man' #needs new value

_basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", 'postgresql://localhost/letswatchtv')
SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True