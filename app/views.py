from app import app, lm, db
from flask import Flask, render_template, redirect, request, url_for, session, jsonify, flash
from flask_login import login_user, logout_user, current_user, login_required
from models import *
from config import *
from forms import *
import datetime
import json
import random


@app.route('/')
def home():
  """Returns homepage of Let's Watch TV"""
  genres = Genre.query.all()
  genre_list = []

  for genre in genres:
    genre_list.append(genre.name)

  random_genre = random.choice(genre_list)
  tvshows = TVShow.query.filter(TVShow.genres.any(name=random_genre)).filter_by(status="Running").all()
  return render_template("index.html",  
                          title="Home",
                          genre=random_genre,
                          tvshows=tvshows)


@app.route('/tvshows')
def tvshows():
  """Returns a result page from search query"""
  tvshows = TVShow.query.all()
  genres  = Genre.query.all()

  return render_template("tvshows/tvshows.html", 
                          title="TVShows",
                          genres=genres, 
                          tvshows=tvshows[:15])


@app.route('/tvshows/<tvshow_id>', methods = ['GET', 'POST'])
def tvshow_details(tvshow_id):
  """Returns details about a particular tvshow and tweets about the show this week"""
  hide           = True
  tvshow_details = TVShow.query.filter_by(id=tvshow_id).one()
  network      = Network.query.filter_by(id=tvshow_details.network_id).one()
  seasons      = Season.query.filter_by(tvshow_id = tvshow_id).all()
  episodes     = Episode.query.filter_by(tvshow_id = tvshow_id).all()
  tvshow_photo = TVShowPhoto.query.filter_by(tvshow_id = tvshow_id).one()
  if not tvshow_details.twitter_handle:
    hide = False

  return render_template("tvshows/tvshow_details.html", 
                          title=tvshow_details.tvshow, 
                          tvshow_name=tvshow_id,
                          network=network.network_name,
                          hide=hide,
                          seasons=seasons,
                          episodes=episodes,
                          tvshow_photo=tvshow_photo,
                          tvshow_details=tvshow_details)


@app.route('/tvshows/<tvshow_id>/add_favorite', methods = ['GET', 'POST'])
def add_favorite(tvshow_id):
  tvshow = TVShow.query.get(tvshow_id)
  current_user.favorite_show(tvshow)
  flash("Added to favorites", 'success')
  db.session.commit()
  return redirect(url_for('tvshow_details',tvshow_id=tvshow_id))


@app.route('/tvshows/<tvshow_id>/remove_favorite', methods = ['GET', 'POST'])
def remove_favorite(tvshow_id):
  tvshow = TVShow.query.get(tvshow_id)
  current_user.unfavorite_show(tvshow)
  flash("Removed from favorites", 'danger')
  db.session.commit()
  return redirect(request.referrer)


@app.route('/tvshows/<tvshow_id>/add_watchlist', methods = ['GET', 'POST'])
def add_watchlist(tvshow_id):
  tvshow = TVShow.query.get(tvshow_id)
  current_user.add_watchlist(tvshow)
  flash("Added to watchlist", 'success')
  db.session.commit()
  return redirect(url_for('tvshow_details',tvshow_id=tvshow_id))


@app.route('/tvshows/<tvshow_id>/remove_watchlist', methods = ['GET', 'POST'])
def remove_watchlist(tvshow_id):
  tvshow = TVShow.query.get(tvshow_id)
  current_user.remove_watchlist(tvshow)
  flash("Removed from watchlist", 'danger')
  db.session.commit()
  return redirect(url_for('tvshow_details',tvshow_id=tvshow_id))


@app.route('/tvshows/<tvshow_id>/seasons')
def season(tvshow_id):
  tvshow_details = TVShow.query.filter_by(id=tvshow_id).one()
  seasons        = Season.query.filter_by(tvshow_id = tvshow_id).all()
  return render_template("tvshows/seasons.html",
                          title=tvshow_details.tvshow, 
                          seasons=seasons)


@app.route('/tvshows/<tvshow_id>/<season_number>/episodes')
def episode(tvshow_id,season_number):
  tvshow_details = TVShow.query.filter_by(id=tvshow_id).one()
  episodes       = Episode.query.filter_by(tvshow_id = tvshow_id, season_number = season_number).all()
  return render_template("tvshows/episodes.html",
                          title=tvshow_details.tvshow, 
                          episodes=episodes)


@app.route('/tvshows/<tvshow_id>/<season_number>/<episode_number>')
def episode_details(tvshow_id,season_number,episode_number):
  tvshow_details = TVShow.query.filter_by(id=tvshow_id).one()
  episode        = Episode.query.filter_by(tvshow_id = tvshow_id, season_number = season_number, episode_number = episode_number).one()
  return render_template("tvshows/episode_details.html",
                          title=tvshow_details.tvshow, 
                          episode=episode)


@app.route('/about')
def about():
  """Returns a page about Let's Watch TV """

  return render_template("about/about.html")


@app.route('/profile')
def profile():
  """Returns user's homepage/landing page"""

  # user = User.query.filter_by(email=current_user.email).one()
  favorites = current_user.tv_fav
  watchlist = current_user.watchlist


  return render_template("account/profile.html", 
                          title="Home",
                          favorites=favorites,
                          watchlist=watchlist)


@app.route('/register', methods = ['GET', 'POST'])
def register():
  """Checks if the current_user is logged in or render a signup form 
  and add the new user to the database and redirect them to their profile."""

  if current_user.is_authenticated:
    return redirect(url_for('profile'))

  form = SignUpForm(request.form)
  if form.validate_on_submit():
    user            = User()
    form.populate_obj(user)
    user.created_on = datetime.datetime.now()
    user.updated_on = datetime.datetime.now()
    db.session.add(user)
    db.session.commit()
    login_user(user)    
    flash("You're in the club", 'success')
    return redirect(url_for('profile'))

  return render_template('account/register.html', 
                          title='Register', 
                          form=form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
  """Checks if the current_user is logged in, if so, redirect to user's
    homepage. """
  if current_user.is_authenticated:
    return redirect(url_for('profile'))

  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email = form.email.data).first()

    if user is not None and user.valid_password(form.password.data):
      if login_user(user,remember=form.remember_me.data):
        session.permanent            = not form.remember_me.data
        user.created_on              = datetime.datetime.now()
        user.last_logged_in          = datetime.datetime.now()
        db.session.commit()
        flash('Logged in successfully!', category = 'success')

        return redirect(request.args.get('next') or url_for('profile'))

      else:
        flash('This username is disabled', 'danger')

    else:
      flash('Wrong username or password', 'danger')

  return render_template('account/login.html', 
                          title='Login', 
                          form=form)

@app.route('/api/tvshows.json')
def tvshows_json():
  """Returns all tvshows in db as json """
  tvshows = TVShow.query.all()
  output = []
  for show in tvshows:
    genres = []
    for genre in show.genres:
      genres.append(genre.name)

    output.append({
      "id": show.id,
      "tvshow": show.tvshow,
      "show": show.type_,
      "language": show.language,
      "status": show.status,
      "runtime": show.runtime,
      "premiered": show.premiered,
      "scheduled_time": show.schedule_time,
      "scheduled_day": show.schedule_day,
      "twitter": show.twitter_handle,
      "network": show.network_id,
      "summary": show.summary,
      "characters": show.characters,
      "genres": genres
      })

  return json.dumps(output)


@app.route('/logout/')
@login_required
def logout():
  """Logs out user, flashes a message upon completion, and redirects 
    to the homepage"""
  logout_user()
  flash('Logged out successfully', 'success')
  return redirect(url_for('home'))


@lm.user_loader
def load_user(id):
  """Returns the user's unique id from the database, used by Flask-Login"""
  return User.query.get(int(id))


