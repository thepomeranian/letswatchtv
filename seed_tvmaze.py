import requests
from app import models, db

def seed():
  
  for x in xrange(0,81):
    print "Seeding TVmaze page", x

    r = requests.get(
      "http://api.tvmaze.com/shows?page=%d" % x)

    response = r.json() 

    for tvshow in response:                   
      schedule = tvshow['schedule']
      days = schedule['days']
      string_days = schedule_days(days)
      externals = tvshow['externals']
      string_genres = ""

      if tvshow['genres']:
        string_genres = stringing_genres(tvshow['genres'])
      else:
        tvshow['genres'] = None

      if tvshow['image']:
        image_urls = tvshow['image']
        tvshow_photos = models.TVShowPhoto(medium_url=image_urls['medium'],
                                           original_url=image_urls['original'])
        add_to_db(tvshow_photos)

      else:
        tvshow['image'] = None
        tvshow_photos = models.TVShowPhoto(medium_url=None,
                                           original_url=None)
        add_to_db(tvshow_photos)


      if tvshow['network']:
        network_info = tvshow['network']
        country_info = network_info['country']
        network = models.Network(network_name=network_info['name'], 
                               country=country_info['name'], 
                               code=country_info['code'], 
                               timezone=country_info['timezone'])
        add_to_db(network)

      else:
        network = models.Network(network_name=None, 
                               country=None, 
                               code=None, 
                               timezone=None)
        add_to_db(network)
        
      external = models.External(tvrage=externals['tvrage'], 
                                 thetvdb=externals['thetvdb'], 
                                 imdb=externals['imdb'])
      add_to_db(external)

      tvshow = models.TVShow(tvshow=tvshow['name'], 
                             type_=tvshow['type'], 
                             language=tvshow['language'],
                             genres=string_genres,
                             status=tvshow['status'],
                             premiered=tvshow['premiered'],
                             schedule_time=schedule['time'],
                             schedule_day=string_days,
                             summary=tvshow['summary'])
      add_to_db(tvshow)


def schedule_days(days):
  length = len(days)
  string_days = ""
  while length > 0:

    if length >= 1:
      string_days = str(days[length - 1]) + " " + string_days 
    else:
      string_days = str(days[length - 1])
      

    length -= 1
  return string_days

def add_to_db(models):
  db.session.add(models)
  db.session.commit()


def stringing_genres(genres):
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