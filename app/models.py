# -*- coding: utf-8 -*-
from app import db
from sqlalchemy import *
from werkzeug.security import generate_password_hash, check_password_hash

# If you're looking to change the database, change the properties below
# and run `python manage.py db migrate` or `python managepy db upgrade`

#Global variables to use for role management
ROLE_ADMIN = 0
ROLE_USER = 1

class User(db.Model):
    '''
    The User Model
    '''
    #__tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), nullable = False, index = True, unique = True)
    _password = db.Column('password', db.String(120), nullable = False)
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)
    last_logged_in = db.Column(db.DateTime)
    active = db.Column(db.SmallInteger, default = 1)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))

    def __repr__(self):
        return '<User %r>' % (self.email)

    def _set_password(self, password):
        self._password = generate_password_hash(password)

    def _get_password(self):
        return self._password

    password = db.synonym('_password', descriptor=property(_get_password, _set_password))

    def valid_password(self, password):
        return check_password_hash(self._password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True if self.active is 1 else False

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)