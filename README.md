LetsWatchTV is your single source of information for TV Shows.

## Local Setup
### Getting started
This local setup assumes that you are using a machine with some type of Unix-based environment.

**Prerequesites**

- Python 2 (we're using 2.7.12)
- Node.js & NPM (we're using 6.x.x)
- virtualenv
- Postgres

**Postgres**

 _Skip this section if you have Postgres installed already._
 
 **Mac**
 On a Mac, it's strongly suggested that you just use [Postgres.app](http://postgresapp.com/). Once you have that installed, you need to add Postgres to your environment:

`export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"`

Doing this before installing Python dependencies can solve a lot of issues.

**Linux**

Fedora & RHEL: `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib`

Debian (Ubuntu): `sudo apt-get install postgresql postgresql-server postgresql-server-dev`

**Python**

1. Create a virtualenv for the application 
  `virtualenv venv`
2. Activate the virtualenv 
  `source venv/bin/activate`
3. Install dependencies `pip install -r requirements.txt`

Now, we have to create our database & migration:

1. Create a new Postgres database called `letswatchtv`
2. `python manage.py db init`
3. `python manage.py db migrate`
4. `python manage.py db upgrade`

**Node/JS**

Install gulp & bower globally if you don't already have them:
`npm install -g gulp bower`

Then install all other dependencies (from `package.json`): 
`npm install`

### Running the app

Assuming dependencies are installed and the virtualenv is active:

1. `python run.py`
2. Open a new terminal window
3. `gulp`

The app should be running on [localhost:5000](http://localhost:5000)!

## Tech Stack
People sometimes ask me: _thepomeranian what kinds of frameworks, libraries, and tools did you use to build this site and what do they do?_

**Python**
- Flask
- Flask Migrate / Alembic
- Flask Login
- Flask-WTF (What The Form)
- SQLAlchemy
- requests / urllib3
- Werkzeug

**Server Side JS**
- npm - Node's package manager for managing js dependencies
- gulp.js - Task automator, used for SASS, JS, and livereload
- bower - Package manager for frontend libraries

**APIs, Libraries, and Frontend**
- SASS - Precompiled CSS library with more power & flexibility
- Twitter API - Fetching various pieces of information from Twitter via their API
- Bootstrap - Frontend framework
- Toastr - toast notification library
- lazyload.js - Lazyloading images
- typeahead.js - Search & typeahead
- Slick carousel - Image carousels
- Isotope / masonry - sorting & filtering