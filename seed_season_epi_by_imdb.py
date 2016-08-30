import requests
from app import models, db


def get_or_create(session, model, **kwargs):
  """Checks db for same entry, if duplicate entry does not exist, insert a new entry"""
  instance = session.query(model).filter_by(**kwargs).first()
  if instance:
      return instance
  else:
      instance = model(**kwargs)
      session.add(instance)
      session.commit()
      return instance


def seed_by_imdb():
  imdb_id = TVShow.query.filter_by(id=tvshow_id).one()








def seed():
  """Seeds db using the request library and TVmaze API"""
  resp_count = 0
  for x in xrange(0,81):
    print "Seeding TVmaze page", x
    r = requests.get(
      "http://api.tvmaze.com/shows?page=%d" % x)

    response = r.json() 

    for tvshow_obj in response:    
      resp_count += 1
      print resp_count               
      schedule      = tvshow_obj['schedule']
      days          = schedule['days']
      string_days   = schedule_days(days)
      externals     = tvshow_obj['externals']
      string_genres = ""

      if tvshow_obj['genres']:
        string_genres = stringing_genres(tvshow_obj['genres'])

      else:
        tvshow_obj['genres'] = None

      if tvshow_obj['network']:
        network_info = tvshow_obj['network']
        country_info = network_info['country']
        network      = get_or_create(db.session, models.Network,
                               network_name=network_info['name'], 
                               country=country_info['name'], 
                               code=country_info['code'], 
                               timezone=country_info['timezone'])

      tvshow = models.TVShow(tvshow=tvshow_obj['name'], 
                             type_=tvshow_obj['type'], 
                             language=tvshow_obj['language'],
                             genres=string_genres,
                             status=tvshow_obj['status'],
                             premiered=tvshow_obj['premiered'],
                             schedule_time=schedule['time'],
                             schedule_day=string_days,
                             network_id=network.id,
                             summary=tvshow_obj['summary'])
      add_to_db(tvshow)

      if tvshow_obj['image']:
        image_urls = tvshow_obj['image']
        tvshow_photos = models.TVShowPhoto(tvshow_id=tvshow.id,
                                           medium_url=image_urls['medium'],
                                           original_url=image_urls['original'])
        add_to_db(tvshow_photos)

      else:
        tvshow_obj['image'] = None
        tvshow_photos = models.TVShowPhoto(tvshow_id=tvshow.id,
                                           medium_url=None,
                                           original_url=None)
        add_to_db(tvshow_photos)

      external = models.External(tvshow_id=tvshow.id,
                                 tvrage=externals['tvrage'], 
                                 thetvdb=externals['thetvdb'], 
                                 imdb=externals['imdb'])
      add_to_db(external)
      

def schedule_days(days):
  """Changes list to printed string"""
  # Combine with stringing genres if time allows
  length      = len(days)
  string_days = ""
  while length > 0:

    if length >= 1:
      string_days = str(days[length - 1]) + " " + string_days 
    else:
      string_days = str(days[length - 1])
      

    length -= 1
  return string_days


def add_to_db(models):
  """Add transaction and commit"""
  db.session.add(models)
  db.session.commit()


def stringing_genres(genres):
  """Changes list to printed string"""
  # Combine with schedule days if time allows
  length = len(genres)
  string_genres = ""

  while length > 0:

    if length >= 1:
      string_genres = str(genres[length - 1]) + " " + string_genres 
    else:
      string_genres = str(genres[length - 1])
      
    
    length -= 1
  return string_genres

seed()