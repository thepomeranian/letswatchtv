import os

DEBUG = True
CSRF_ENABLED = True
CSRF_SESSION_KEY = "somethingimpossibletoguess" #needs new value
SECRET_KEY = 'yeah, man' #needs new value

_basedir = os.path.abspath(os.path.dirname(__file__))