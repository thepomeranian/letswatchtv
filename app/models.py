# -*- coding: utf-8 -*-
from app import db
from sqlalchemy import *
from werkzeug.security import generate_password_hash, check_password_hash

# If you're looking to change the database, change the properties below
# and run `python manage.py db migrate` or `python managepy db upgrade`

#Global variables to use for role management
ROLE_ADMIN   = 0
ROLE_USER    = 1
ROLE_MANAGER = 2


class User(db.Model):
  """The User Model"""

  __tablename__  = 'users'
  id             = db.Column(db.Integer, primary_key = True)
  email          = db.Column(db.String(120), nullable = False, index = True, unique = True)
  _password      = db.Column('password', db.String(120), nullable = False)
  created_on     = db.Column(db.DateTime)
  updated_on     = db.Column(db.DateTime)
  last_logged_in = db.Column(db.DateTime)
  role           = db.Column(db.Integer, default = 1)
  active         = db.Column(db.SmallInteger, default = 1)
  first_name     = db.Column(db.String(120))
  last_name      = db.Column(db.String(120))

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

genre_association_table=db.Table('genre_association_table', 
  db.Column('tvshow_id', db.Integer, db.ForeignKey('tvshows.id')),
  db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'))
  )


actor_association_table=db.Table('actor_association_table', 
  db.Column('tvshow_id', db.Integer, db.ForeignKey('tvshows.id')),
  db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'))
  )


class TVShow(db.Model):
  """The TVShow model"""

  __tablename__  = 'tvshows'
  id             = db.Column(db.Integer, autoincrement=True, primary_key=True)
  tvshow         = db.Column(db.String(300))
  type_          = db.Column(db.String(300))
  language       = db.Column(db.String(300))
  status         = db.Column(db.String(300))
  runtime        = db.Column(db.Integer)
  premiered      = db.Column(db.String(300))
  schedule_time  = db.Column(db.String(100))
  schedule_day   = db.Column(db.String(200))
  twitter_handle = db.Column(db.String(150))
  network_id     = db.Column(db.Integer, db.ForeignKey('networks.id'))
  summary        = db.Column(db.String(10000))
  characters     = db.Column(db.String(100000))
  
  tvshow_photos  = db.relationship('TVShowPhoto', backref='tvshow_photo', lazy="dynamic")
  seasons        = db.relationship('Season', backref='seasons', lazy='dynamic')
  episodes       = db.relationship('Episode', backref='episodes', lazy='dynamic')
  externals      = db.relationship('External', backref='externals', lazy='dynamic')
  tweets         = db.relationship('Tweets', backref='tweets', lazy='dynamic')
  genres         = db.relationship('Genre', secondary=genre_association_table, backref='genres', lazy="dynamic")
  cast           = db.relationship('Actor', secondary=actor_association_table, backref='cast', lazy="dynamic")
  
  
class Actor(db.Model):
  """The Actor model"""

  __tablename__ = 'actors'
  id            = db.Column(db.Integer, autoincrement=True, primary_key=True)
  name          = db.Column(db.String(1000), nullable=False)
  gender        = db.Column(db.String(10))
  date_of_birth = db.Column(db.String(100))
  imdb_url      = db.Column(db.String(1000))
  horoscope     = db.Column(db.String(50))
  height        = db.Column(db.String(10))
  image         = db.Column(db.String(1000))


class Genre(db.Model):
  """The Genre model"""
  __tablename__ = 'genres'
  id            = db.Column(db.Integer, autoincrement=True, primary_key=True)
  name = db.Column(db.String(500))




class Season(db.Model):
  """The Season model"""
  __tablename__  = 'seasons'
  id             = db.Column(db.Integer, autoincrement=True, primary_key=True)
  tvshow_id      = db.Column(db.Integer, db.ForeignKey('tvshows.id'))
  season_number  = db.Column(db.Integer)
  total_episodes = db.Column(db.Integer)
  premiere_date  = db.Column(db.String(30))
  end_date       = db.Column(db.String(30))
  season_photo   = db.Column(db.String(2000))


class Episode(db.Model):
  """The Episode model"""
  __tablename__  = 'episodes'
  id             = db.Column(db.Integer, autoincrement=True, primary_key=True)
  tvshow_id      = db.Column(db.Integer, db.ForeignKey('tvshows.id'))
  episode_name   = db.Column(db.String(2000))
  season_number  = db.Column(db.Integer)
  episode_number = db.Column(db.Integer)
  airdate        = db.Column(db.String(30))
  airtime        = db.Column(db.String(30))
  airstamp       = db.DateTime
  runtime        = db.Column(db.Integer)
  image          = db.Column(db.String(2000))
  summary        = db.Column(db.String(10000))


class TVShowPhoto(db.Model):
  """The TVShowPhoto model"""
  
  __tablename__ = "tvshow_photos"
  id            = db.Column(db.Integer, autoincrement=True, primary_key=True)
  tvshow_id     = db.Column(db.Integer, db.ForeignKey('tvshows.id'))
  medium_url    = db.Column(db.String(2000))
  original_url  = db.Column(db.String(2000))


class Network(db.Model):
  """The Network model"""

  __tablename__ = 'networks'
  id            = db.Column(db.Integer, autoincrement=True, primary_key=True)
  network_name  = db.Column(db.String(300))
  country       = db.Column(db.String(300))
  code          = db.Column(db.String(5))
  timezone      = db.Column(db.String(300))
  
  tvshows       = db.relationship('TVShow', backref='tvshows', lazy='dynamic')


class External(db.Model):
  """The Externals model"""

  __tablename__ = 'externals'
  id            = db.Column(db.Integer, autoincrement=True, primary_key=True)
  tvshow_id     = db.Column(db.Integer, db.ForeignKey('tvshows.id'))
  tvrage        = db.Column(db.String(100))
  thetvdb       = db.Column(db.String(100))
  imdb          = db.Column(db.String(100))
  

class Tweets(db.Model):
  """The Tweets model"""

  __tablename__ = 'tweets'
  id            = db.Column(db.Integer, autoincrement=True, primary_key=True)
  username      = db.Column(db.String(100))
  location      = db.Column(db.String(100))
  created_at    = db.Column(db.DateTime)
  text          = db.Column(db.String(2000))
  tvshow_id     = db.Column(db.Integer, db.ForeignKey('tvshows.id'))

