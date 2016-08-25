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
                             status=tvshow_obj['status'],
                             premiered=tvshow_obj['premiered'],
                             schedule_time=schedule['time'],
                             schedule_day=string_days,
                             network_id=network.id,
                             summary=tvshow_obj['summary'])
      add_to_db(tvshow)

      print tvshow_obj['name']
      
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

      if externals['imdb']:
        
        r2 = requests.get("http://api.tvmaze.com/lookup/shows?imdb=%s" % externals['imdb'])

        response2 = r2.json() 

        tv_result           = models.TVShow.query.filter_by(id=tvshow.id).one()
        tv_result.genres      = response2['genres']
        tv_result.runtime = response2['runtime']
        db.session.commit()

        api_show_id = response2['id']

        r3 = requests.get("http://api.tvmaze.com/shows/%d/seasons" % api_show_id)

        seasons = r3.json() 
  
        for season in seasons:
          season_photos = season['image']
   
          if not season_photos:
            photos = None
          else:
            photos = season_photos['original']

          season_model = models.Season(tvshow_id=tvshow.id,
                                      season_number=season['number'],
                                      total_episodes=season['episodeOrder'],
                                      premiere_date=season['premiereDate'],
                                      end_date=season['endDate'],
                                      season_photo=photos)

          add_to_db(season_model)

        r4 = requests.get("http://api.tvmaze.com/shows/%d/episodes" % api_show_id)
        
        episodes = r4.json()

        for episode in episodes:
          if not episode['image']:
            episode_images = None
          else:
            episode_images = episode['image']
            episode_image = episode_images['original']

          episode_model = models.Episode(tvshow_id=tvshow.id,
                                        episode_name=episode['name'],
                                         season_number=episode['season'],
                                         episode_number=episode['number'],
                                         airdate=episode['airdate'],
                                         airtime=episode['airtime'],
                                         airstamp=episode['airstamp'],
                                         runtime=episode['runtime'],
                                         image=episode_image,
                                         summary=episode['summary'])
        
          add_to_db(episode_model)

        r5 = requests.get("http://api.tvmaze.com/shows/%d/cast" % api_show_id)

        all_cast_info = r5.json()

        actor_list = []
        character_list = []

        for cast_info in all_cast_info:
          
          actor_info = cast_info['person']
          name = actor_info['name']
          actor_list.append(name)

          character_info = cast_info['character']
          name = character_info['name']
          character_list.append(name)

        tv_result           = models.TVShow.query.filter_by(id=tvshow.id).one()
        tv_result.cast      = actor_list
        tv_result.characters = character_list
        db.session.commit()

      elif not externals['imdb'] and externals['thetvdb']:
        r2 = requests.get("http://api.tvmaze.com/lookup/shows?thetvdb=%d" % externals['thetvdb'])

        response2 = r2.json() 
        tv_result           = models.TVShow.query.filter_by(id=tvshow.id).one()
        tv_result.genres      = response2['genres']
        tv_result.runtime = response2['runtime']
        db.session.commit()

        api_show_id = response2['id']
        
        r3 = requests.get("http://api.tvmaze.com/shows/%d/seasons" % api_show_id)
        
        seasons = r3.json() 


        for season in seasons:

          season_photos = season['image']

          if not season_photos:
            photos = None
          else:
            photos = season_photos['original']
            
          season_model = models.Season(tvshow_id=tvshow.id,
                                      season_number=season['number'],
                                      total_episodes=season['episodeOrder'],
                                      premiere_date=season['premiereDate'],
                                      end_date=season['endDate'],
                                      season_photo=photos)

          add_to_db(season_model)

        r4 = requests.get("http://api.tvmaze.com/shows/%d/episodes" % api_show_id)
        
        episodes = r4.json()

        for episode in episodes:
          if not episode['image']:
            episode_images = None
          else:
            episode_images = episode['image']
            episode_image = episode_images['medium']

          episode_model = models.Episode(tvshow_id=tvshow.id,
                                        episode_name=episode['name'],
                                         season_number=episode['season'],
                                         episode_number=episode['number'],
                                         airdate=episode['airdate'],
                                         airtime=episode['airtime'],
                                         airstamp=episode['airstamp'],
                                         runtime=episode['runtime'],
                                         image=episode_image,
                                         summary=episode['summary'])
        
        add_to_db(episode_model)

        r5 = requests.get("http://api.tvmaze.com/shows/%d/cast" % api_show_id)

        all_cast_info = r5.json()

        actor_list = []
        character_list = []

        for cast_info in all_cast_info:
          
          actor_info = cast_info['person']
          name = actor_info['name']
          actor_list.append(name)

          character_info = cast_info['character']
          name = character_info['name']
          character_list.append(name)

        tv_result           = models.TVShow.query.filter_by(id=tvshow.id).one()
        tv_result.cast      = actor_list
        tv_result.characters = character_list
        db.session.commit()

      elif not externals['imdb'] and not externals['thetvdb'] and externals['tvrage']:
        r2 = requests.get("http://api.tvmaze.com/lookup/shows?tvrage=%d" % externals['tvrage'])

        response2 = r2.json() 
        tv_result         = models.TVShow.query.filter_by(id=tvshow.id).one()
        tv_result.genres  = response2['genres']
        tv_result.runtime = response2['runtime']
        db.session.commit()

        api_show_id = response2['id']

        r3 = requests.get("http://api.tvmaze.com/shows/%d/seasons" % api_show_id)

        seasons = r3.json() 

        for season in seasons:
          season_photos = season['image']

          if not season_photos:
            photos = None
          else:
            photos = season_photos['medium']
            
          season_model = models.Season(tvshow_id=tvshow.id,
                                      season_number=season['number'],
                                      total_episodes=season['episodeOrder'],
                                      premiere_date=season['premiereDate'],
                                      end_date=season['endDate'],
                                      season_photo=photos)
          add_to_db(season_model)

        r4 = requests.get("http://api.tvmaze.com/shows/%d/episodes" % api_show_id)
        
        episodes = r4.json()

        for episode in episodes:
          if not episode['image']:
            episode_images = None
          else:
            episode_images = episode['image']
            episode_image = episode_images['medium']

          episode_model = models.Episode(tvshow_id=tvshow.id,
                                        episode_name=episode['name'],
                                         season_number=episode['season'],
                                         episode_number=episode['number'],
                                         airdate=episode['airdate'],
                                         airtime=episode['airtime'],
                                         airstamp=episode['airstamp'],
                                         runtime=episode['runtime'],
                                         image=episode_image,
                                         summary=episode['summary'])
        
        add_to_db(episode_model)

        r5 = requests.get("http://api.tvmaze.com/shows/%d/cast" % api_show_id)

        all_cast_info = r5.json()

        actor_list = []
        character_list = []

        for cast_info in all_cast_info:
          
          actor_info = cast_info['person']
          name = actor_info['name']
          actor_list.append(name)

          character_info = cast_info['character']
          name = character_info['name']
          character_list.append(name)

        tv_result           = models.TVShow.query.filter_by(id=tvshow.id).one()
        tv_result.cast      = actor_list
        tv_result.characters = character_list
        db.session.commit()

      else:
        pass
     
      

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