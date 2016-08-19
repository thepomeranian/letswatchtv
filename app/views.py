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
  """Returns details about a particular tvshow and tweets about the show this week"""
  hide = True
  tvshow_details = TVShow.query.filter_by(id=tvshow_id).one()
  network = Network.query.filter_by(id=tvshow_details.network_id).one()
  print network.network_name

  if not tvshow_details.twitter_handle:
    hide = False
  return render_template("tvshows/tvshow_details.html", 
                          title=tvshow_details.tvshow, 
                          tvshow_name=tvshow_id,
                          network=network.network_name,
                          hide=hide,
                          tvshow_details=tvshow_details)


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


