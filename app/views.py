from app import app, lm, db
from flask import Flask, render_template, redirect, request, url_for, session, jsonify, flash
from flask_login import login_user, logout_user, current_user, login_required
from models import *
from config import *
from forms import *
import datetime


@app.route('/')
def home():
  """Returns homepage of Let's Watch TV"""
  return render_template("index.html", 
                          title="Home")


@app.route('/tvshows')
def tvshows():
  """Returns a result page from search query"""
  tvshows = TVShow.query.all()
  return render_template("tvshows/tvshows.html", 
                          title="Results", 
                          tvshows=tvshows)

@app.route('/tvshows/<tvshow_id>')
def tvshow_details(tvshow_id):
  hide = True
  """Returns details about a particular tvshow and tweets about the show this week"""
  # tweets = Tweets.query.all()
  tvshow_details = TVShow.query.filter_by(id=tvshow_id).all()
  # sample = {"id":250,"url":"http://www.tvmaze.com/shows/250/kirby-buckets","name":"Kirby Buckets","type":"Scripted","language":"English","genres":["Comedy"],"status":"Running","runtime":30,"premiered":"2014-10-20","schedule":{"time":"20:00","days":["Wednesday"]},"rating":{"average":null},"weight":1,"network":{"id":25,"name":"Disney XD","country":{"name":"United States","code":"US","timezone":"America/New_York"}},"webChannel":null,"externals":{"tvrage":37394,"thetvdb":278449,"imdb":"tt3544772"},"image":{"medium":"http://tvmazecdn.com/uploads/images/medium_portrait/1/4600.jpg","original":"http://tvmazecdn.com/uploads/images/original_untouched/1/4600.jpg"},"summary":"The single-camera series that mixes live-action and animation stars Jacob Bertrand as the title character. \"Kirby Buckets\" introduces viewers to the vivid imagination of charismatic 13-year-old Kirby Buckets, who dreams of becoming a famous animator like his idol, Mac MacCallister. With his two best friends, Fish and Eli, by his side, Kirby navigates his eccentric town of Forest Hills where the trio usually find themselves trying to get out of a predicament before Kirby's sister, Dawn, and her best friend, Belinda, catch them. Along the way, Kirby is joined by his animated characters, each with their own vibrant personality that only he and viewers can see.","updated":1469967834,"_links":{"self":{"href":"http://api.tvmaze.com/shows/250"},"previousepisode":{"href":"http://api.tvmaze.com/episodes/855107"},"nextepisode":{"href":"http://api.tvmaze.com/episodes/880557"}}}
  print tvshow_details

  if not tvshow_details[0].twitter_handle:
    hide = False
  return render_template("tvshows/tvshow_details.html", 
                          title=tvshow_details[0].tvshow, 
                          tvshow_name=tvshow_id,
                          hide=hide,
                          tvshow_details=tvshow_details[0])


@app.route('/about')
def about():
  """Returns a page about Let's Watch TV """

  return render_template("about/about.html")


@app.route('/profile')
def profile():
  """Returns user's homepage/landing page"""

  return render_template("account/profile.html", 
                          title="Home")


@app.route('/register', methods = ['GET', 'POST'])
def register():
  """Checks if the current_user is logged in or render a signup form 
  and add the new user to the database and redirect them to their profile."""

  if current_user.is_authenticated:
    return redirect(url_for('profile'))

  form = SignUpForm(request.form)
  if form.validate_on_submit():
    user = User()
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
      if login_user(user, remember = form.remember_me.data):
        session.permanent = not form.remember_me.data
        user.created_on = datetime.datetime.now()
        user.last_logged_in = datetime.datetime.now()
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


