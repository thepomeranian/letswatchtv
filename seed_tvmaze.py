import requests
from app import models, db

for x in xrange(0,81):
  print "Seeding TVmaze page", x

  r = requests.get(
    "http://api.tvmaze.com/shows?page=%d" % x)

  response = r.json() 

  for tvshow in response:                   
    schedule = tvshow['schedule']
    days = schedule['days']

    length = len(days)
    string_days = ""
    while length > 0:

      if length >= 1:
        string_days = str(days[length - 1]) + " " + string_days 
      else:
        string_days = str(days[length - 1])
        break

      length -= 1

    genres = tvshow['genres']

    if tvshow['image']:
      image_urls = tvshow['image']
      # print image_urls['medium']
      # print image_urls['original']

      tvshow_photos = models.TVShowPhoto(medium_url=image_urls['medium'],
                                         original_url=image_urls['original'])
      db.session.add(tvshow_photos)
      db.session.commit()

    else:
      tvshow['image'] = None
      tvshow_photos = models.TVShowPhoto(medium_url=None,
                                         original_url=None)
      db.session.add(tvshow_photos)
      db.session.commit()

    if tvshow['network']:
      network_info = tvshow['network']
    #   print network_info['name']
      country_info = network_info['country']
    #   print country_info['name']
    #   print country_info['code']
    #   print country_info['timezone']
      network = models.Network(network_name=network_info['name'], 
                             country=country_info['name'], 
                             code=country_info['code'], 
                             timezone=country_info['timezone'])
      db.session.add(network)
      db.session.commit()
    else:
      network = models.Network(network_name=None, 
                             country=None, 
                             code=None, 
                             timezone=None)
      db.session.add(network)
      db.session.commit()
      

    externals = tvshow['externals']
    # print externals['tvrage']
    # print externals['thetvdb']
    # print externals['imdb']
    
    length = len(genres)
    string_genres = ""

    while length > 0:

      if length >= 1:
        string_genres = str(genres[length - 1]) + " " + string_genres 
      else:
        string_genres = str(genres[length - 1])
        break

      length -= 1


    if not genres:
      string_genres = "None"

    # print string_genres
    # print string_days
    # print schedule['time']
    # print tvshow['name'], tvshow['type'], tvshow['language'], tvshow['genres'], tvshow['status'],tvshow['premiered'] ,tvshow['summary']

    # print tvshow['name']
    tvshow = models.TVShow(tvshow=tvshow['name'], 
                           type_=tvshow['type'], 
                           language=tvshow['language'],
                           genres=string_genres,
                           status=tvshow['status'],
                           premiered=tvshow['premiered'],
                           schedule_time=schedule['time'],
                           schedule_day=string_days,
                           summary=tvshow['summary'])
    db.session.add(tvshow)
    db.session.commit()

    external = models.External(tvrage=externals['tvrage'], 
                               thetvdb=externals['thetvdb'], 
                               imdb=externals['imdb'])
    db.session.add(external)
    db.session.commit()

