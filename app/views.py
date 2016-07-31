from app import app, lm, db
from flask import Flask, render_template, redirect, request, url_for, session, jsonify, flash
from flask_login import login_user, logout_user, current_user, login_required
from models import *
from config import *
from forms import *
import datetime


@app.route('/')
def home():
  """Returns homepage of Let's Watch TV
  """
  return render_template("index.html", title="Home")


@app.route('/search-results')
def search_results():
  """Returns a result page from search query
  """
  return render_template("results.html", title="Results")


@app.route('/about')
def about_page():
  """Returns a page about Let's Watch TV 
  """
  return render_template("about/about.html")


@app.route('/user_home')
def user_home():
  """Returns user's homepage/landing page
  """
  return render_template("account/home.html", title="Home")


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
  """Gets a signup form and submits it upon successful completion. 

  Checks if current_user is authenticated, if they are, then redirect
    them to the user's homepage

  Creates an instance of SignUpForm from forms.py as form

  Checks if the the entire form is successfully completed and
    checks if the user has already created an account in database

  Creates an instance of User() and calls the method populate_obj
    to insert elements in the form into database

  user.created_on and user.updated_on get a timestamp from datetime
    library

  Adds user to db.session, commit's add, and login's user

  Flash a success message using toastr library

  Redirect to user's homepage
  """
  if current_user.is_authenticated:
    return redirect(url_for('user_home'))

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
    return redirect(url_for('user_home'))

  return render_template('account/signup.html', title='Sign Up', form=form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
  """Checks if the current_user is logged in, if so, redirect to user's
    homepage. Handles user login, remember me, and check authentication

  Create an instance of LoginForm

  Check if the form is properly filled it upon submission
    if so, look for the user by using query method to look in the database
    of users by email address and return the first response

  If the user exists and the user provides the correct password
    Check if the user asked to remember the user, if so, keep the session
    longer (from docs)
  
    --add remember me checkbox

  """
  # Already logged in; return to index
  if current_user.is_authenticated:
    return redirect(url_for('user_home'))

  # Not logged in; show the login form or errors
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email = form.email.data).first()
    if user is not None and user.valid_password(form.password.data):
      if login_user(user, remember = form.remember.data):
        # session['remember_me'] = form.remember_me.data
        session.permanent = not form.remember.data
        user.created_on = datetime.datetime.now()
        user.last_logged_in = datetime.datetime.now()
        db.session.commit()
        flash('Logged in successfully!', category = 'success')
        return redirect(request.args.get('next') or url_for('user_home'))
    # If a user is blocked or if the password is incorrect, flash
    # a danger message
      else:
        flash('This username is disabled', 'danger')
    else:
      flash('Wrong username or password', 'danger')

  return render_template('account/login.html', title='Login', form=form)


@app.route('/logout/')
@login_required
def logout():
  """Logs out user, flashes a message upon completion, and redirects to the homepage
  """
  logout_user()
  flash('Logged out successfully', 'success')
  return redirect(url_for('home'))


@lm.user_loader
def load_user(id):
  """Returns the user's unique id from the database,
    used by Flask-Login
  """
    return User.query.get(int(id))


