# -*- coding: utf-8 -*-
from app import db
from sqlalchemy import *
from werkzeug.security import generate_password_hash, check_password_hash

# If you're looking to change the database, change the properties below
# and run `python manage.py db migrate` or `python managepy db upgrade`

#Global variables to use for role management
ROLE_ADMIN = 0
ROLE_USER = 1
ROLE_MANAGER = 2


class User(db.Model):
  """The User Model"""

  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String(120), nullable = False, index = True, unique = True)
  _password = db.Column('password', db.String(120), nullable = False)
  created_on = db.Column(db.DateTime)
  updated_on = db.Column(db.DateTime)
  last_logged_in = db.Column(db.DateTime)
  role = db.Column(db.Integer, default = 1)
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

  def is_admin(self):
    return True if self.role == 0 else False

  def is_active(self):
    return True if self.active is 1 else False

  def is_anonymous(self):
    return False

  def get_id(self):
    return unicode(self.id)

  def get_name(self):
    return self.first_name + " " + self.last_name


class TVShow(db.Model):
  """The TVShow model"""

  __tablename__ = 'tvshows'
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  tvshow = db.Column(db.String(300), nullable=False)
  type_ = db.Column(db.String(300), nullable=False)
  language = db.Column(db.String(300), nullable=False)
  genres = db.Column(db.String(300), nullable=False)
  status = db.Column(db.String(300), nullable=False)
  runtime = db.Integer
  premiered = db.Column(db.String(300), nullable=False)
  schedule_time = db.Column(db.String(20), nullable=False)
  schedule_day = db.Column(db.String(15), nullable=False)
  rating = db.Integer
  twitter_handle = db.Column(db.String(100), nullable=True)
  network_id = db.Column(db.Integer, db.ForeignKey('networks.id'))
  summary = db.Column(db.String(5000), nullable=False)
  
  tvshow_photos = db.relationship('TVShowPhoto', backref='tvshow_photos', lazy=dynamic)
  externals = db.relationship('External', backref='externals', lazy=dynamic)
  tweets = db.relationship('Tweet', backref='tweets', lazy=dynamic)


class Actors(db.Model):
  """The Actors model"""

  __tablename__ = 'actors'
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  first_name = db.Column(db.String(100), nullable=False)
  last_name = db.Column(db.String(150), nullable=False)
  gender = db.Column(db.String(10), nullable=False)
  date_of_birth = db.Column(db.String(100))
  imdb_url = db.Column(db.String(1000))
  horoscope = db.Column(db.String(50))
  height = db.Column(db.String(10))


class TVShowPhoto(db.Model):
  """The TVShowPhoto model"""

  __tablename__ = "tvshow_photos"
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  tvshow = db.Column(db.Integer, db.ForeignKey('tvshow_photos.id'))
  medium_url = db.Column(db.String(1000))
  original_url = db.Column(db.String(1000))

  

class Network(db.Model):
  """The Network model"""

  __tablename__ = 'networks'
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  network_name = db.Column(db.String(100), nullable=False)
  code = db.Integer
  timezone = db.Column(db.String(100))

  tvshows = db.relationship('TVShow', backref='networks', lazy=dynamic)


class External(db.Model):
  """The Externals model"""

  __tablename__ = 'externals'
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  tvshow = db.Column(db.Integer, db.ForeignKey('externals.id'))
  tvrage = db.Column(db.String(100))
  thetvdb = db.Column(db.String(100))
  imdb = db.Column(db.String(100))
  

class Tweet(db.Model):
  """The Tweets model"""

  __tablename__ = 'tweets'
  id = db.Column(db.Integer, autoincrement=True, primary_key=True)
  username = db.Column(db.String(100), nullable=False)
  location = db.Column(db.String(100), nullable=True)
  created_at = db.Column(db.DateTime, nullable=False)
  text = db.Column(db.String(512), nullable=False)
  tvshow = db.Column(db.Integer, db.ForeignKey('tweets'))

